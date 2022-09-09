"""
Read in a json file with conference information and create the repository that
will host the poster gallery: Landing page with all the posters in a table.
Individual pages for each poster with all their info.  Directory structure for
browsing.
"""

import argparse
import http.client
import json
import pathlib as pl
import re
import subprocess as sp

from datetime import date
from os.path import getsize as getfilesize
from typing import Any, Callable, Dict, List, Optional
from urllib.parse import quote as urlquote

from latex2svg.latex2svg import latex2svg


POSTER_SERVER = "posters.bc.g-node.org"
POSTER_REPO = "BernsteinConference/posters"
MAIN_REPO_IMAGES = "BernsteinConference/main/raw/master/img"
VIDEO_ICON_URL = f"/{MAIN_REPO_IMAGES}/play.png"
TOPIC_COLOURS = {
    "Networks, dynamical systems": "yellow",
    "Data analysis, machine learning, neuroinformatics": "blue",
    "Learning, plasticity and memory": "red",
    "Sensory processing and perception": "green",
    "Attention, reward, decision making": "orange",
    "Behaviour and cognition": "lightblue",
    "Brain disease, network dysfunction and intervention": "turquoise",
    "Single neurons, biophysics": "grey",
    "Motor control, movement, navigation": "purple",
    "Neurotechnology": "salmon",
    "Other": "darkblue",
}
SESSION_TIMES = {
    "I": "Wed, Sep 14, 16:30 CEST",
    "II": "Wed, Sep 14, 18:10 CEST",
    "III": "Thu, Sep 15, 12:45 CEST",
    "IV": "Thu, Sep 15, 14:25 CEST"
}
ITEM_TYPES = {
    "I": "Invited Talk",
    "C": "Contributed Talk",
    "P": "Poster",
}
INDEX_TEXT = {
    "posters": "Posters can be sorted either by topic or the poster session in which "
               "they are presented. To facilitate the overview and sorting of the many "
               "posters, they have been assigned to different color-coded topics.",
    "invited": "Video links of invited talks will appear successively in the repository. "
               "We only record talks for which we have the speakers’ consent. "
               "Please note, these links must not be published anywhere else.",
    "contributed": "Video links of contributed talks will appear successively in the "
                   "repository. We only record talks for which we have the speakers’ "
                   "consent. Please note, these links must not be published anywhere "
                   "else.",
    "workshops": "Video links of workshop talks will appear successively in the "
                 "repository. We only record talks for which we have the speakers’ "
                 "consent. Please note, these links must not be published anywhere else.",
    "exhibition": "Here you will find information about the Bernstein Conference "
                  "exhibitors. They inform about their services and products, "
                  "and supply supplemental material."
}
# List[int] - use NEW abstract numbers
WITHDRAWN = []
# List[int] - WARNING: these PDF links will not appear on the landing page
MISSING_PDF = [21,22,23,24,25,27,28,30,32,34,36,37,38,39,41,42,43,44,46,47,48,50,51,52,55,56,58,59,60,62,67,68,70,71,72,74,75,76,77,78,79,80,82,83,84,85,86,87,88,90,91,93,96,98,99,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,117,118,119,120,121,122,123,124,126,127,129,130,131,132,133,134,135,136,137,138,139,140,141,142,144,145,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,173,174,175,176,177,179,180,181,182,184,185,186,187,188,189,190,191,193,194,195,196,197,198,200,202,203,204,205,206,207,208,209,210,211,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,229,230,231,232,233,234,235,236,237,238,241,243,244,245,246,247,248,249,250,252,253,254,255,256,257,258,259,260,261,262,263,264,266,267,268,269,270,271,273,274,275,277,279,280,281,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,301,302,304,305,306,307,309,313]
WORKSHOP_RECORD_MSG = {
    "recording": "Video recording will be available",
    "no recording": "Video recording will not be made available",
    "waiting": "",
}
# Special handling for the invited talks info line: if required adjust talk numbers
# and 'Keynote' / 'Braitenberg award' texts where the INVITED_TALKS_ADJUST variable
# is used.
INVITED_TALKS_ADJUST = True

USE_VIMEO_PLUGIN = False
VIMEO_PLAYER_SCRIPT = '<div style="padding:56.25% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/{}?h={}&amp;badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen style="position:absolute;top:0;left:0;width:100%;height:100%;" title="{}"></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>'

# Add an on-site poster number to all landing pages listing or showing individual posters
# Required to also display the Poster enumeration used at the site of the conference.
ONSITE_POSTER_NUMBER = True


def run_cmd(*args) -> str:
    """
    Runs a terminal command and returns feedback in case of any error.
    """
    err = ""
    ret = sp.run(args, check=False, stdout=sp.PIPE, stderr=sp.PIPE)
    if ret.returncode:
        cmd_str = " ".join(str(arg) for arg in args)
        err = f"Command {cmd_str} failed"
        err += f"{str(ret.stdout)}\n"
        err += f"{str(ret.stderr)}\n"

    return err


def item_filename(item: Dict[str, str]) -> str:
    """
    Returns the filename that should be used for the poster (without
    extension).
    """
    item_type = ITEM_TYPES[item["short"]]
    fname_prefix = item_type.split(" ")[0]

    return fname_prefix + item["abstract_number"]


def session_filename(session: str) -> str:
    """
    Returns the filename that should be used for the session (without
    extension).
    """
    return f"Session-{session}"


def topic_filename(topic: str) -> str:
    """
    Returns the filename that should be used for the topic (without extension).
    """
    # Remove commas and replace spaces with '-'.
    return topic.replace(",", "").replace(" ", "-")


def section_header(section: str) -> str:
    """
    Returns a markdown image string.
    """
    return f"/{MAIN_REPO_IMAGES}/BC_Header_{section}.jpg"


def make_sorter(key_name: str, apply: Callable = None) -> Callable:
    """
    Returns a sorter function that applies a sort mechanism to a specific column.
    :param key_name: name of the column used in sorting
    :param apply: sort mechanism applied
    """
    def sorter(row):
        sort_val = row[key_name]
        if apply:
            return apply(sort_val)
        return sort_val

    return sorter


def md_table_row(values: List[str]) -> str:
    """
    Returns all values in a list as a single string formatted as a markdown table.
    """
    return "| " + " | ".join(values) + " |"


def make_infoline(item: Dict[str, str], omit: Optional[str] = None) -> str:
    """
    Returns a single markdown formatted line.
    :param item: dictionary containing a single poster item.
    :param omit: Exclude information from the markdown line.
                 Valid content is "topic" and "session".
    """
    topic = item["topic"]
    session = item["session"]
    abs_no = item["abstract_number"]
    item_type = ITEM_TYPES[item["short"]]
    info_content = f'{item_type} {item["poster_board_number"]}'

    info_line = f"**{info_content.strip()}**"
    # Add the additional compound on-site poster number to the info line
    if item["short"] == "P" and ONSITE_POSTER_NUMBER and omit != "session":
        info_line = f'**Session {item["session"]} / {info_content.strip()}**'

    # omitting when topic == Award is an unwise hack to circumvent Award being used
    # as a non-supported topic in the BCOS spreadsheet
    if topic and omit != "topic" and topic != "Award":
        topic_link = ""
        if item["short"] == "P":
            topic_link = topic_filename(topic)
        colour = TOPIC_COLOURS[topic]
        icon_url = f"/{POSTER_REPO}/raw/master/banners/icon-{colour}.png"
        info_line += f" | [![{topic}]({icon_url}) {topic}](/wiki/{topic_link})"

    if omit != "session":
        session_link = session_filename(session)
        info_line += f" | [{item_type} session {session}](/wiki/{session_link})"

    # An unwise hack to enable special categories within invited talks
    # and adjust the talk numbers accordingly.
    if item["short"] == "I" and INVITED_TALKS_ADJUST:
        if abs_no == "311":
            info_line = "**Award**"

    return f"{info_line}  \n"


def make_list_item(item: Dict[str, str], omit: Optional[str] = None) -> str:
    """
    Returns multiple markdown formatted lines containing poster wiki link, title, author
    and additional information.
    :param item: dictionary containing a single poster item.
    :param omit: Leads to information excluded from the info line;
                 valid entries are "session" and "topic".
    """
    page = urlquote(f"/wiki/{item_filename(item)}")
    title = item["title"]
    authors = item["authors"]

    title_line = f"**[{title}]({page})**  \n"
    author_line = f"{authors}  \n"
    info_line = make_infoline(item, omit)

    return title_line + author_line + info_line


def create_thumbnail(pdf_path: pl.Path) -> str:
    """
    Creates a gif thumbnail for a PDF poster and returns the path of the new
    file.  The new file is created in a subdirectory of the PDF path called
    "thumbnails".
    """
    gif_name = pdf_path.name[:-3] + "gif"
    thumb_dir = pdf_path.parent.joinpath("thumbnails")
    thumb_dir.mkdir(exist_ok=True)
    thumb_path = thumb_dir.joinpath(gif_name)

    return run_cmd("convert", "-delay", "100", pdf_path, "-thumbnail", "x120", thumb_path)


def download_pdfs(data: List[Dict[str, str]], target_dir: pl.Path):
    """
    Downloads posters and video URLs from upload service.
    """
    conn = http.client.HTTPSConnection(POSTER_SERVER, timeout=60)
    poster_dir = target_dir.joinpath("posters")
    poster_dir.mkdir(parents=True, exist_ok=True)
    # collect and return missing or empty PDFs
    missing = ""
    # collect thumbnail creation errors and display them after
    # all posters have been handled.
    thumb_err = ""

    def download(uuid: str, fname: str, extension: str) -> Optional[pl.Path]:
        nonlocal conn
        try:
            conn.request("GET", f"/uploads/{uuid}.{extension}")
            resp = conn.getresponse()
        except http.client.RemoteDisconnected:
            conn = http.client.HTTPSConnection(POSTER_SERVER, timeout=60)
            return download(uuid, fname, extension)

        pdf_data = resp.read()

        if resp.status == http.client.NOT_FOUND:
            return None

        if resp.status != http.client.OK:
            print(f"Unexpected error: [{resp.status}] {resp.reason}")
            return None

        f_path = poster_dir.joinpath(f"{fname}.{extension}")
        with open(f_path, "wb") as new_file:
            new_file.write(pdf_data)
        return f_path

    for idx, item in enumerate(data):
        # PDF download is only useful for posters ("P"); ignore other categories
        if item["short"] != "P":
            continue

        if idx and not idx % 100:
            print(f" {idx}")

        uuid = item["id"]
        number = item["abstract_number"]

        # default to the all-is-well info_rune
        info_rune = "•"
        if pdf_path := download(uuid, number, "pdf"):
            # create thumbnail only if downloaded PDF has content
            if getfilesize(pdf_path) == 0:
                info_rune = "0"
                missing += f"{uuid} - {number} - PDF file issue\n"
            # create thumbnail and report in case of an issue
            elif err := create_thumbnail(pdf_path):
                info_rune = "x"
                thumb_err += f"{err}\n"
        else:
            info_rune = "."
            missing += f"{uuid} - {number}\n"

        print(info_rune, end="", flush=True)
        download(uuid, number, "url")

    print(f"\n{thumb_err}")

    return missing


def create_equation_images(data: List[Dict[str, str]], target_dir: Dict[str, pl.Path],
                           create: bool):
    """
    Replaces Latex formatted content within the abstract texts of poster items.
    If specified, the Latex formatted content is also converted to and saved as images.
    :param data: list containing a dictionary of poster items.
    :param target_dir: directory to create equation images in.
    :param create: if this is True, the equation images will be created.
                   If this is False, only the Latex occurrences in the abstract
                   text is replaced.
    """
    print("Creating equation images. NOTE: make sure a full Latex installation is available")
    for item in data:
        text = texify(item, target_dir, create)
        item["abstract"] = text


def read_local_url(fname: str, target_dir: pl.Path) -> str:
    """
    Open a local file and return its content.
    :param fname: file name to be opened.
    :param target_dir: directory where the file can be found.
    :return: file content.
    """
    poster_dir = target_dir.joinpath("posters")
    url_file = poster_dir.joinpath(f"{fname}.url")
    if not url_file.exists():
        return ""

    with open(url_file, "rb") as ufp:
        return ufp.read().decode()


def sanitize_tex(eqn: str) -> str:
    """
    Returns sanitized common greek alphabet letters.
    :param eqn: Latex formatted text
    """
    eqn = eqn.replace("σ", r"\sigma").replace("β", r"\beta").replace("λ", r"\lambda")
    eqn = eqn.replace("ζ", r"\zeta")
    eqn = eqn.replace(r"\tag{1}", "(1)")

    return eqn


def texify(item: Dict[str, str], target_dir: Dict[str, pl.Path], create: bool) -> str:
    """
    Replace LaTeX math snippets with images.
    """
    number = item["abstract_number"]
    text = item["abstract"]
    short = item["short"] if item["short"] in ITEM_TYPES else "P"

    eqn_dir = target_dir[short].joinpath("equations")
    eqn_dir.mkdir(exist_ok=True)
    if match := re.findall(r"\${1,2}.*?\${1,2}", text):
        print(f"Handling equation image for {item['short']}/{item['abstract_number']}")
        for idx, group in enumerate(match):
            img_basename = f"{number}-{idx}"
            url = f"/raw/master/equations/{img_basename}.png"
            text = text.replace(group, f"![]({url})")

            if create:
                sanitized = sanitize_tex(group)
                svg = latex2svg(sanitized)["svg"]
                svg_path = eqn_dir.joinpath(f"{img_basename}.svg")
                with open(svg_path, "w", encoding="utf-8") as svg_file:
                    svg_file.write(svg)

                png_path = eqn_dir.joinpath(f"{img_basename}.png")
                if err := run_cmd("convert", f"{svg_path}", f"{png_path}"):
                    print(f"\n{err}")

    return text


def make_landing_page(item: Dict[str, str], target_dir: pl.Path)\
        -> Optional[pl.Path]:
    """
    Writes a poster landing page and returns its file name.
    :param item: dictionary containing a poster item.
    :param target_dir: directory to save the file to.
    :return: name of the created file.
    """
    title = item["title"]
    # use apostrophe that is properly rendered by markdown
    title = title.replace("’", "'")

    authors = item["authors"]
    number = item["abstract_number"]
    text = item["abstract"]
    time = item["time"]

    vimeo_video_url = item["vimeo link"]
    user_video_url = read_local_url(number, target_dir)
    # send video url to BCOS directly; put in spreadsheet
    bcos_video_url = item["individual video link"]

    hopin_url = item["link hopin"]

    cit_list = item["citation"]
    doi_item = item["doi"]

    if not title:
        item_id = item["id"]
        print(f"Poster with ID {item_id} has no title")
        return None

    # Video handling: Use vimeo over user URL; if no URL use BCOS video as backup
    video_url = vimeo_video_url if vimeo_video_url else user_video_url
    if not video_url:
        video_url = bcos_video_url

    if not hopin_url:
        hopin_url = "https://hopin.to"

    poster_url = f"/src/master/posters/{number}.pdf"
    poster_thumb_url = (f"/{POSTER_REPO}/raw/master/posters/thumbnails/"
                        f"{number}.gif")

    # Handle citation
    year = date.today().year
    doi_item = f" doi: [{doi_item}](https://doi.org/{doi_item})" if doi_item else ""
    copy_item = f"__Copyright:__ © ({year}) {cit_list}\n" if cit_list else ""
    cit_item = f"__Citation:__ {cit_list} ({year}) {title}. " \
               f"Bernstein Conference {year}.{doi_item}"

    file_basename = item_filename(item)
    filename = target_dir.joinpath(f"{file_basename}.md")
    with open(filename, "w", encoding="utf-8") as poster_page:
        if item["short"] == "C":
            poster_page.write("[Contributed Talks](wiki)\n")
        elif item["short"] == "I":
            poster_page.write("[Invited Talks](wiki)\n")
        else:
            poster_page.write(
                '[All posters](wiki/List) | [Topics](wiki/Topics) | [Sessions](wiki/Sessions)\n')
        poster_page.write('<div class="ui dividing header"></div>\n\n')

        poster_page.write(f"# {title}\n\n")
        poster_page.write(f"_{authors.strip()}_\n\n")

        if item["short"] == "P":
            poster_page.write(make_infoline(item) + "\n\n")
            # do not add poster PDF links if the PDF is missing
            if int(number) not in MISSING_PDF:
                poster_page.write(f"[![Poster]({poster_thumb_url})]({poster_url}) ")

        if video_url:
            vid_text = f"[![Video]({VIDEO_ICON_URL})]({video_url})"
            # replacing normal video link with embedded player
            vimsplit = video_url.replace("https://vimeo.com/", "")
            vimsplit = vimsplit.split("/")
            if len(vimsplit) == 2 and USE_VIMEO_PLUGIN:
                vim_vid_id = vimsplit[0]
                vim_vid_hash = vimsplit[1]
                vim_auth = authors.strip().split(",")[0]
                vim_vid_title = f"{vim_auth.strip()}, {title.strip()}"
                vid_text = VIMEO_PLAYER_SCRIPT.format(vim_vid_id, vim_vid_hash,
                                                      vim_vid_title)
            # table hack to enable "no video" notice for Contributed and Invited talks
            if item["short"] in ["C", "I"] and video_url == "no recording":
                vid_text = "Video recording will not be made available\n\n"
            poster_page.write(vid_text)

        poster_page.write("\n\n")

        if time:
            curr_txt = f"**Session time**: {time} | [Hopin roundtable]({hopin_url})\n\n"
            poster_page.write(curr_txt)

        poster_page.write("## Abstract\n\n")
        poster_page.write(f"{text}\n\n")
        poster_page.write("<div class='ui dividing header'></div>")
        poster_page.write(f"{copy_item}\n")
        poster_page.write(f"{cit_item}\n\n")

    return filename


def write_topic_index(data: List[Dict[str, str]], filepath: pl.Path):
    """
    Creates poster topic index file and one file per topic listing all
    Posters within each topic.
    :param data: list containing a dictionary of poster items.
    :param filepath: directory to save the files to.
    """
    topic_posters: Dict[str, List[Dict[str, str]]] = {
        topic: [] for topic in TOPIC_COLOURS
    }
    for item in data:
        topic = item["topic"]
        if not topic:
            topic = "Other"
        topic_posters[topic].append(item)

    with open(filepath, "w", encoding="utf-8") as topics_file:
        topics_file.write(
            '[All posters](wiki/List) | [Topics](wiki/Topics) | [Sessions](wiki/Sessions)\n')
        topics_file.write('<div class="ui dividing header"></div>\n')

        topics_file.write("# Poster topics\n\n")
        for topic, colour in TOPIC_COLOURS.items():
            # Support default poster category "Other",
            # but display it only if there are actual posters.
            num_posters = len(topic_posters[topic])
            if num_posters > 0:
                topics_file.write('<div class="banner">\n')

                topic_url = urlquote(topic_filename(topic))
                topics_file.write(f'<a href="{topic_url}">')

                image_url = f"/{POSTER_REPO}/raw/master/banners/{colour}.png"
                top_img = f'<img width=300 alt="Topic: {topic}" src="{image_url}"/>\n'
                topics_file.write(top_img)
                topics_file.write(f'<div class="title">{topic}</div>\n')

                topics_file.write(f'<div class="text">{num_posters} Posters</div></a>')

                topics_file.write("</div>")

    # One page per topic with listing
    for topic, items in topic_posters.items():
        topic_fname = topic_filename(topic)
        filepath = filepath.parent.joinpath(topic_fname).with_suffix(".md")
        list_content: List[str] = []
        for item in items:
            list_item = make_list_item(item, omit="topic")
            list_content.append(list_item)

        with open(filepath, "w", encoding="utf-8") as topic_file:
            colour = TOPIC_COLOURS[topic]
            image_url = f"/{POSTER_REPO}/raw/master/banners/{colour}-wide.png"

            topic_file.write(
                '[All posters](wiki/List) | [Topics](wiki/Topics) | [Sessions](wiki/Sessions)\n')
            topic_file.write('<div class="ui dividing header"></div>\n')

            topic_file.write(f'<img height=150 width=1000 alt="Topic: {topic}" '
                             f'src="{image_url}"/>\n')
            topic_file.write(f"# Poster topic: {topic}\n\n")
            topic_file.write("\n".join(list_content) + "\n")


def write_session_index(data: List[Dict[str, str]], filepath: pl.Path):
    """
    Creates poster session index file and one file per session listing all
    Posters within each session.
    :param data: list containing a dictionary of poster items.
    :param filepath: directory to save the files to.
    """
    session_posters: Dict[str, List[Dict[str, str]]] = {}
    for item in data:
        session = item["session"]
        if not session:
            continue
        if session not in session_posters:
            session_posters[session] = []
        session_posters[session].append(item)

    # sort session index by roman letters
    session_content = {}
    for session, items in session_posters.items():
        num_posters = len(items)
        time = SESSION_TIMES[session]
        session_url = urlquote(session_filename(session))

        curr = f"## Session {session}\n"
        curr = f"{curr}{num_posters} posters\n"
        curr = f"{curr}**Time:** {time}\n"
        curr = f"{curr}[Browse Session {session} posters](wiki/{session_url})\n<br/><br/>\n"
        session_content[session] = curr

    with open(filepath, "w", encoding="utf-8") as sessions_file:
        sessions_file.write(
            '[All posters](wiki/List) | [Topics](wiki/Topics) | [Sessions](wiki/Sessions)\n')
        sessions_file.write('<div class="ui dividing header"></div>\n')

        sessions_file.write("# Poster Sessions\n")
        session_roman_order = ["I", "II", "III", "IV"]
        if len(session_roman_order) != len(SESSION_TIMES):
            print("WARNING: Session number mismatch between scheduled sessions and index page")
        for sess_num in session_roman_order:
            if sess_num in session_content:
                sessions_file.write(session_content[sess_num])
            else:
                print(f"WARNING: could not find Session {sess_num}; "
                      f"omitting in 'Poster by session' listing page")

    # one page per session with listing
    for session, items in session_posters.items():
        fname = session_filename(session)
        filepath = filepath.parent.joinpath(fname).with_suffix(".md")

        sorted_list = []
        for item in items:
            list_item = make_list_item(item, omit="session")
            board_num = item["poster_board_number"]
            if board_num:
                board_num = int(item["poster_board_number"])
            else:
                print(f'WARNING: empty board number for abstract {item["id"]}')
            sorted_list.append((board_num, list_item))

        sorted_list = sorted(sorted_list)
        list_content: List[str] = []
        for i in sorted_list:
            list_content.append(i[1])

        with open(filepath, "w", encoding="utf-8") as session_file:
            session_file.write(
                '[All posters](wiki/List) | [Topics](wiki/Topics) | [Sessions](wiki/Sessions)\n')
            session_file.write('<div class="ui dividing header"></div>\n')

            session_file.write(f"# Posters in Session {session}\n\n")
            session_file.write("\n".join(list_content) + "\n")


def make_poster_index(data: List[Dict[str, str]], target_dir: pl.Path):
    """
    Creates the main poster landing page and a page listing all posters.
    :param data: list containing a dictionary of poster items.
    :param target_dir: directory to save the files to.
    """
    # create a list sorted by a) roman numeral session number and b) poster board number
    sorted_content = []
    for item in data:
        curr_item_text = make_list_item(item)
        board_num = item["poster_board_number"]
        if board_num:
            board_num = int(item["poster_board_number"])
        else:
            print(f'WARNING: empty board number for abstract {item["id"]}')

        sorted_content.append((item["session"], board_num, curr_item_text))

    sorted_content = sorted(sorted_content)
    list_content: List[str] = []
    for i in sorted_content:
        list_content.append(i[2])

    list_fname = "List.md"
    list_path = target_dir.joinpath(list_fname)
    with open(list_path, "w", encoding="utf-8") as list_file:
        list_file.write(
            '[All posters](wiki/List) | [Topics](wiki/Topics) | [Sessions](wiki/Sessions)\n')
        list_file.write('<div class="ui dividing header"></div>\n')

        list_file.write("\n".join(list_content))

    index_links = {"Browse all posters": list_fname}

    topics_fname = "Topics.md"
    topics_path = target_dir.joinpath(topics_fname)
    write_topic_index(data, topics_path)
    index_links["Browse posters by Topic"] = topics_fname

    sessions_fname = "Sessions.md"
    sessions_path = target_dir.joinpath(sessions_fname)
    write_session_index(data, sessions_path)
    index_links["Browse posters by Session"] = sessions_fname

    home_fname = "Home.md"
    home_path = target_dir.joinpath(home_fname)
    head_img = section_header("posters")
    head_text = INDEX_TEXT["posters"]
    with open(home_path, "w", encoding="utf-8") as home_file:
        home_file.write(f"[![Posters]({head_img})](/wiki)\n\n")
        home_file.write(head_text + "\n\n")

        for name, fname in index_links.items():
            link = f"/wiki/{fname[:-3]}"
            home_file.write(f"## [{name}]({link})\n\n")


def make_landing_pages(data: List[Dict[str, str]], target_dir: pl.Path):
    """
    Walks through all poster items and calls the function to create their
    landing pages. Writes the progress to the command line.
    :param data: list containing a dictionary of poster items.
    :param target_dir: directory to save the files to.
    """
    print(f"Creating {len(data)} landing pages")
    for idx, item in enumerate(data):
        if idx and not idx % 100:
            print(f" {idx}")
        print(".", end="", flush=True)
        make_landing_page(item, target_dir)
    print()


def make_talks_index(data: List[Dict[str, str]], target_dir: pl.Path):
    """
    Creates the contributed and invited talks index pages
    :param data: list containing a dictionary of contributed or invited talk items.
    :param target_dir: directory to save the files to.
    """
    home_fname = "Home.md"
    list_content: List[str] = []

    for item in data:
        list_content.append(make_list_item(item, omit="session"))
    list_path = target_dir.joinpath(home_fname)

    key = ""
    if data[0]["short"] == "C":
        key = "contributed"
    elif data[0]["short"] == "I":
        key = "invited"

    head_img = section_header(key)
    head_text = INDEX_TEXT[key]

    with open(list_path, "w", encoding="utf-8") as list_file:
        list_file.write(f"[![{key.capitalize()} talks]({head_img})](/wiki)\n\n")
        list_file.write(head_text + "\n\n")
        list_file.write("\n".join(list_content))


def filter_withdrawn(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Poster numbers for withdrawn entries are filtered out here.
    """
    for entry in data[:]:
        if int(entry["abstract_number"]) in WITHDRAWN:
            print(f"REMOVE withdrawn {entry['title']}")
            data.remove(entry)

    return data


def make_workshop_page(workshops: Dict[str, Dict[str, Any]], target_dir: pl.Path):
    """
    Creates workshop item landing page.
    :param workshops: dictionary containing workshop dictionary items.
    :param target_dir: directory to save the file to.
    """
    for num, ws_item in workshops.items():
        name = ws_item["name"]
        organisers = ws_item["organisers"]
        url = ws_item["url"]

        content = [f"# {name}\n\n",
                   f"Organizers: {organisers}   \n",
                   f"**[Workshop {num} abstract and schedule]({url})**\n\n"]

        for idx, talk in enumerate(ws_item["talks"]):
            title = talk["title"]
            speakers = talk["speakers"]
            rec_status = talk["recording"]
            content.append(f"{idx+1}. {title}  \n")
            content.append(f"{speakers}  \n")

            # if videourl has been provided and looks like a valid link
            if (vid_url := talk["videourl"]).startswith("http"):
                content.append(f"[Video recording]({vid_url})\n")
            elif rec_msg := WORKSHOP_RECORD_MSG[rec_status]:
                content.append(f"*{rec_msg}*\n")

            content.append("\n")

        fname = f"Workshop{num}.md"
        file_path = target_dir.joinpath(fname)
        print(f"Creating landing page {file_path}")
        with open(file_path, "w", encoding="utf-8") as ws_file:
            ws_file.write("".join(content))


def make_workshop_pages(data: List[Dict[str, str]], target_dir: pl.Path):
    """
    Creates the workshop main and item pages.
    :param data: list containing a dictionary of workshop items.
    :param target_dir: directory to save the files to.
    """
    # Prepare workshop items
    workshops: Dict[str, Dict[str, Any]] = {}
    for item in data:
        num = item["workshop number"]
        name = item["workshop name"]
        organisers = item["organisers"]
        url = item["info url"]
        if num not in workshops:
            workshops[num] = {}
            workshops[num]["name"] = name
            workshops[num]["organisers"] = organisers
            workshops[num]["url"] = url
            workshops[num]["talks"] = []

        workshops[num]["talks"].append({
            "title": item["talk title"],
            "speakers": item["speakers"],
            "recording": item["recording status"],
            "videourl": item["recording url"],
        })

    # Create landing pages
    make_workshop_page(workshops, target_dir)

    # Create workshops index page
    list_content: List[str] = []
    for num, ws_item in workshops.items():
        entry = f'**[{ws_item["name"]}](wiki/Workshop{num})**  \n'
        entry += f'{ws_item["organisers"]}  \n'
        entry += f'**Workshop {num}** | {len(ws_item["talks"])} talks\n\n'
        list_content.append(entry)

    list_path = target_dir.joinpath("Home.md")
    head_text = INDEX_TEXT["workshops"]
    head_img = section_header("workshops")
    print(f"Creating file {list_path} ...")
    with open(list_path, "w", encoding="utf-8") as list_file:
        list_file.write(f"[![Workshops]({head_img})](/wiki)\n\n")
        list_file.write(head_text + "\n\n")
        list_file.write("\n".join(list_content))


def handle_exhibition_desc(company: str, desc: str) -> str:
    """
    Handles exhibition description special formatting needs.
    Returns the updated description.
    :param company: company name
    :param desc: company description
    """
    if company.lower() == "mathworks":
        desc = desc.replace(" o ", "\n- ")

    if company.lower() == "simulation and data lab neuroscience":
        desc = desc.replace("\n•", "\n- ")

    return desc


def make_exhibition_page(item: Dict[str, str], target_dir: pl.Path, idx: int):
    """
    Creates exhibition item landing page.
    :param item: exhibition dictionary item.
    :param target_dir: directory to save the file to.
    :param idx: Index of the current exhibition item.
    """
    company = item["company_name"]
    logo = item["logo"]
    headline = item["headline"]
    website = item["website"]
    desc = item["description"]
    hopin = item["hopin"]

    content = []
    if logo:
        image_url = f"/BernsteinConference/Exhibition/raw/master/img/{logo}"
        content.append(f'<img height=100 alt="Exhibition: {company}" '
                       f'src="{image_url}"/>\n')

    content.append(f"# {company}\n\n")
    content.append(f"\n\n{headline}\n\n")

    desc = handle_exhibition_desc(company, desc)

    content.append(f"{desc}\n\n")
    content.append("<div class='ui dividing header'></div>")
    content.append("\n\n")

    if website:
        content.append(f"For more information visit the [exhibitor website]("
                       f"{website}).\n\n")

    if hopin:
        content.append(f"If you have any questions, discuss them with "
                       f"moderators at the [exhibitor booth on Hopin]({hopin}).\n")

    # handle materials list
    materials = list(filter(lambda cur: cur.startswith("material_"), item.keys()))
    mat_content = []
    mat_links = []
    for mat in materials:
        if curr := item[mat]:
            # links and material items might not come in order
            if curr.startswith("http"):
                mat_links.append(f"- [{curr}]({curr})\n")
            else:
                mat_item = f"- [{curr}](/src/master/materials/{curr})\n"
                mat_content.append(mat_item)

    if mat_content or mat_links:
        content.append("## Exhibition materials\n")
        if mat_content:
            content.append("For your convenience you can access the following "
                           "exhibition material\n\n")
            content.extend(mat_content)
        if mat_links:
            pre_space = "\n\n" if mat_content else ""
            content.append(f"{pre_space}The following link list refers to additional "
                           f"external resources\n\n")
            content.extend(mat_links)

    file_path = target_dir.joinpath(f"Exhibition{idx}.md")
    print(f"Creating landing page {file_path}")
    with open(file_path, "w", encoding="utf-8") as exhib_file:
        exhib_file.write("".join(content))


def handle_exhibition_data(data: List[Dict[str, str]], target_dir: pl.Path):
    """
    Creates the exhibition main and item pages.
    :param data: list containing a dictionary of exhibition items.
    :param target_dir: directory to save the files to.
    """
    list_content: List[str] = []

    idx = 0
    for item in data:
        idx = idx + 1
        company = item["company_name"]
        headline = item["headline"]

        # List page content
        entry = f"**[{company}](wiki/Exhibition{idx})**  \n"
        entry += f"{headline}\n\n\n"
        list_content.append(entry)

        # Create exhibition item landing page
        make_exhibition_page(item, target_dir, idx)

    list_path = target_dir.joinpath("Home.md")
    print(f"Creating file {list_path} ...")
    with open(list_path, "w", encoding="utf-8") as list_file:
        list_file.write(f'[![Exhibition]({section_header("exhibition")})](/wiki)\n\n')
        list_file.write(f'{INDEX_TEXT["exhibition"]}\n\n')
        list_file.write("\n".join(list_content))


def handle_poster_data(data: List[Dict[str, str]], posters_dir: pl.Path):
    """
    Filters a list for poster specific items and creates index and landing pages.
    :param data: list containing poster dictionary items.
    :param posters_dir: directory to save the files to.
    """
    poster_data = list(filter(lambda item: item["short"] == "P", data))
    poster_data = sorted(poster_data, key=make_sorter("abstract_number", apply=int))

    print("Filtering poster data ...")
    poster_data = filter_withdrawn(poster_data)
    print("Creating poster index ...")
    make_poster_index(poster_data, posters_dir)
    print("Creating poster landing pages ...")
    make_landing_pages(poster_data, posters_dir)


def handle_talks_data(data: List[Dict[str, str]], target_dir: pl.Path,
                      filter_string: str, msg: str):
    """
    Filters a list for talk specific items and creates index and landing pages.
    :param data: list containing talks dictionary items.
    :param target_dir: directory to save the files to.
    :param filter_string: valid entries: "C", "I"
    :param msg: String displayed in command line print.
    """
    filtered_data = list(filter(lambda item: item["short"] == filter_string, data))
    filtered_data = sorted(filtered_data, key=make_sorter("abstract_number", apply=int))
    if filtered_data:
        print(f"Creating {msg} talks index ...")
        make_talks_index(filtered_data, target_dir)
        print(f"Creating {msg} talks landing pages ...")
        make_landing_pages(filtered_data, target_dir)
    else:
        print(f"WARNING: could not find {msg} talks")


def content_check(data: List[Dict[str, str]], check: str,
                  json_file: str, msg: str) -> bool:
    """
    Checks whether a dictionary contains a column specific to expected data and returns
    a corresponding boolean value. This avoids writing files of an invalid gallery type.
    :param data: list containing poster dictionary items.
    :param check: name of the column that is supposed to be found in the dictionary items.
    :param json_file: name of the file containing the data
    :param msg: String displayed in command line print.
    :return: True if the column was found in the data, False otherwise.
    """
    if not data or check not in data[0].keys():
        print(f"'{json_file}' does not seem to be a valid {msg} file ...")
        print("Aborting ...")
        return False
    return True


def main():
    """
    Handles the command line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", dest="download", action="store_true",
                        help="Download new files from upload service")
    parser.add_argument("--single-download", dest="sdl", type=str,
                        help="Download single abstract files providing the abstract UUID")
    parser.add_argument("--render-equations", dest="equations", action="store_true",
                        help="Create pngs for LaTeX equations in abstracts")
    parser.add_argument("--workshops", dest="workshops", action="store_true",
                        help="Create workshop pages instead of posters")
    parser.add_argument("--exhibition", dest="exhibition", action="store_true",
                        help="Create exhibition pages instead of posters")
    parser.add_argument("--conferenceinfo", dest="confinfo", action="store_true",
                        help="Create conference info pages instead of posters")
    parser.add_argument("jsonfile", help="JSON file providing the input data")
    parser.add_argument("targetdir", help="Directory in which to create galleries")
    args = parser.parse_args()

    workshops = args.workshops
    exhibition = args.exhibition
    confinfo = args.confinfo

    download = args.download
    sdl = args.sdl
    equations = args.equations

    target_dir = pl.Path(args.targetdir)
    target_dir.mkdir(parents=True, exist_ok=True)

    json_file = args.jsonfile
    with open(json_file, encoding="utf-8") as jfp:
        data = json.load(jfp)

    # Specific handling of workshops
    if workshops:
        if not content_check(data, "workshop number", json_file, "WORKSHOP"):
            return

        workshops_dir = target_dir.joinpath("workshops")
        workshops_dir.mkdir(parents=True, exist_ok=True)

        make_workshop_pages(data, workshops_dir)
        return

    # Specific handling of exhibition
    if exhibition:
        if not content_check(data, "company_name", json_file, "EXHIBITION"):
            return

        exhib_dir = target_dir.joinpath("exhibition")
        exhib_dir.mkdir(parents=True, exist_ok=True)

        handle_exhibition_data(data, exhib_dir)
        return

    # Specific handling of conference information
    if confinfo:
        print("-- handling conference information")
        print("-- not implemented as of yet")
        return

    # Sanity check to avoid writing invalid poster galleries.
    if not content_check(data, "abstract_number", json_file, "POSTERS"):
        return

    posters_dir = target_dir.joinpath("posters")
    posters_dir.mkdir(parents=True, exist_ok=True)
    invtalks_dir = target_dir.joinpath("invitedtalks")
    invtalks_dir.mkdir(parents=True, exist_ok=True)
    contribtalks_dir = target_dir.joinpath("contributedtalks")
    contribtalks_dir.mkdir(parents=True, exist_ok=True)

    # enable the download of single abstract files (PDF and URL)
    if sdl:
        filtered_data = list(filter(lambda item: item["id"] == sdl, data))
        print(f"Download files for abstract {sdl} ...")
        _ = download_pdfs(filtered_data, posters_dir)
        print("Done ...")
        return

    if download:
        print("Downloading posters and URLs ...")
        amiss = download_pdfs(data, posters_dir)
        print("Done ...\n")
        miss_num = amiss.count("\n")
        print(f"{miss_num} PDFs missing:\n{amiss}")

    # Hack to deal with equations for all posters and talk types
    equation_dirs = {"P": posters_dir, "C": contribtalks_dir, "I": invtalks_dir}
    create_equation_images(data, equation_dirs, equations)

    print("")
    handle_poster_data(data, posters_dir)
    handle_talks_data(data, invtalks_dir, "I", "invited")
    handle_talks_data(data, contribtalks_dir, "C", "contributed")


if __name__ == "__main__":
    main()
