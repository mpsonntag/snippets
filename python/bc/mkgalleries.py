"""
Read in a json file with conference information and create the repository that
will host the poster gallery: Landing page with all the posters in a table.
Individual pages for each poster with all their info.  Directory structure for
browsing.
"""

import json
import argparse
import re
import http.client
import pathlib as pl
import subprocess as sp

from datetime import date
from typing import Any, Callable, Dict, List, Optional
from urllib.parse import quote as urlquote

from latex2svg.latex2svg import latex2svg


POSTER_SERVER = "posters.bc.g-node.org"
GALLERY_SERVER = "https://bc.g-node.org"
POSTER_REPO = "BernsteinConference/posters"
VIDEO_ICON_URL = f"{GALLERY_SERVER}/img/play.png"
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
}
SESSION_TIMES = {
    "I": "Wed, Sep 22, 14:15 CEST",
    "II": "Wed, Sep 22, 18:00 CEST",
    "III": "Thu, Sep 23, 14:15 CEST",
    "IV": "Thu, Sep 23, 18:00 CEST"
}
ITEM_TYPES = {
    "I": "Invited Talk",
    "C": "Contributed Talk",
    "P": "Poster",
}
INDEX_TEXT = {
    "posters": "Posters can be sorted either by topic or the poster session in which "
               "they are presented. To facilitate the overview and sorting of the many "
               "posters, they have been assigned to 10 different color-coded topics.",
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
# use NEW abstract numbers
WITHDRAWN = [65]
WORKSHOP_RECORD_MSG = {
    "recording": "Video recording will be available",
    "no recording": "Video recording will not be made available",
    "waiting": "",
}


def run_cmd(*args):
    ret = sp.run(args, check=False, stdout=sp.PIPE, stderr=sp.PIPE)
    if ret.returncode:
        cmd_str = " ".join(str(arg) for arg in args)
        print(f"Command {cmd_str} failed")
        print(ret.stdout)
        print(ret.stderr)


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
    return f"{GALLERY_SERVER}/img/BC_Header_{section}.jpg"


def make_sorter(key_name: str, apply: Callable = None) -> Callable:
    def sorter(row):
        sort_val = row[key_name]
        if apply:
            return apply(sort_val)
        return sort_val

    return sorter


def md_table_row(values: List[str]) -> str:
    return "| " + " | ".join(values) + " |"


def make_infoline(item: Dict[str, str], omit: Optional[str] = None) -> str:
    topic = item["topic"]
    session = item["session"]
    abs_no = item["abstract_number"]
    item_type = ITEM_TYPES[item["short"]]

    infoline = f"**{item_type} {abs_no}**"
    if topic and omit != "topic":
        topic_link = ""
        if item["short"] == "P":
            topic_link = topic_filename(topic)
        colour = TOPIC_COLOURS[topic]
        icon_url = f"/{POSTER_REPO}/raw/master/banners/icon-{colour}.png"
        infoline += f" | [![{topic}]({icon_url}) {topic}](/wiki/{topic_link})"

    if omit != "session":
        session_link = session_filename(session)
        infoline += f" | [{item_type} session {session}](/wiki/{session_link})"

    return f"{infoline}  \n"


def make_list_item(item: Dict[str, str], omit: Optional[str] = None) -> str:
    page = urlquote(f"/wiki/{item_filename(item)}")
    title = item["title"]
    authors = item["authors"]

    title_line = f"**[{title}]({page})**  \n"
    author_line = f"{authors}  \n"
    info_line = make_infoline(item, omit)

    return title_line + author_line + info_line


def create_thumbnail(pdf_path: pl.Path) -> pl.Path:
    """
    Creates a gif thumbnail for a PDF poster and returns the path of the new
    file.  The new file is created in a subdirectory of the PDF path called
    "thumbnails".
    """
    gif_name = pdf_path.name[:-3] + "gif"
    thumb_dir = pdf_path.parent.joinpath("thumbnails")
    thumb_dir.mkdir(exist_ok=True)
    thumb_path = thumb_dir.joinpath(gif_name)

    run_cmd("convert", "-delay", "100", pdf_path, "-thumbnail", "x120", thumb_path)

    return thumb_path


def download_pdfs(data: List[Dict[str, str]], target_dir: pl.Path):
    """
    Downloads posters and video URLs from upload service.
    """
    conn = http.client.HTTPSConnection(POSTER_SERVER, timeout=60)
    poster_dir = target_dir.joinpath("posters")
    poster_dir.mkdir(parents=True, exist_ok=True)
    missing = ""

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
        if idx and not idx % 100:
            print(f" {idx}")
        uuid = item["id"]
        number = item["abstract_number"]
        if pdf_path := download(uuid, number, "pdf"):
            print("•", end="", flush=True)
            create_thumbnail(pdf_path)
        else:
            print(".", end="", flush=True)
            # collect all missing PDFs
            missing += f"{uuid} - {number}\n"
        download(uuid, number, "url")
    print()

    return missing


def create_equation_images(data: List[Dict[str, str]], target_dir: Dict[str, pl.Path],
                           create: bool):
    for item in data:
        text = texify(item, target_dir, create)
        item["abstract"] = text


def read_local_url(fname: str, target_dir: pl.Path) -> str:
    poster_dir = target_dir.joinpath("posters")
    url_file = poster_dir.joinpath(f"{fname}.url")
    if not url_file.exists():
        return ""

    with open(url_file, "rb") as ufp:
        return ufp.read().decode()


def sanitize_tex(eqn: str) -> str:
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
    short = item["short"] if item["short"] in ITEM_TYPES.keys() else "P"

    eqn_dir = target_dir[short].joinpath("equations")
    eqn_dir.mkdir(exist_ok=True)
    if match := re.findall(r"\${1,2}.*?\${1,2}", text):
        print(f"Handling equation image for {item['short']}/{item['abstract_number']}")
        for idx, group in enumerate(match):
            img_basename = f"{number}-{idx}"
            if create:
                sanitized = sanitize_tex(group)
                svg = latex2svg(sanitized)["svg"]
                svg_path = eqn_dir.joinpath(f"{img_basename}.svg")
                with open(svg_path, "w") as svgfile:
                    svgfile.write(svg)
                png_path = eqn_dir.joinpath(f"{img_basename}.png")
                run_cmd("convert", f"{svg_path}", f"{png_path}")
            url = f"/raw/master/equations/{img_basename}.png"
            text = text.replace(group, f"![]({url})")

    return text


def make_landing_page(item: Dict[str, str], target_dir: pl.Path)\
        -> Optional[pl.Path]:

    title = item["title"]
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
    with open(filename, "w") as poster_page:
        poster_page.write(f"# {title}\n\n")
        poster_page.write(f"_{authors}_\n\n")

        if item["short"] == "P":
            poster_page.write(make_infoline(item) + "\n\n")
            poster_page.write(f"[![Poster]({poster_thumb_url})]({poster_url}) ")

        if video_url:
            poster_page.write(f"[![Video]({VIDEO_ICON_URL})]({video_url})")

        poster_page.write("\n\n")

        if time:
            curr_txt = f"**Session time**: {time} | [Hopin roundtable]({hopin_url})\n\n"
            poster_page.write(curr_txt)

        poster_page.write("## Abstract\n\n")
        poster_page.write(text)
        poster_page.write("\n\n---\n\n")

        poster_page.write(f"{copy_item}\n")
        poster_page.write(f"{cit_item}\n\n")

    return filename


def write_topic_index(data: List[Dict[str, str]], filepath: pl.Path):
    topic_posters: Dict[str, List[Dict[str, str]]] = {
        topic: list() for topic in TOPIC_COLOURS
    }
    for item in data:
        topic = item["topic"]
        if not topic:
            topic = "Other"
        topic_posters[topic].append(item)

    with open(filepath, "w") as topics_file:
        topics_file.write("# Poster topics\n\n")
        for topic, colour in TOPIC_COLOURS.items():
            topics_file.write('<div class="banner">\n')

            topic_url = urlquote(topic_filename(topic))
            topics_file.write(f'<a href="{topic_url}">')

            image_url = f"/{POSTER_REPO}/raw/master/banners/{colour}.png"
            top_img = f'<img width=300 alt="Topic: {topic}" src="{image_url}"/>\n'
            topics_file.write(top_img)
            topics_file.write(f'<div class="title">{topic}</div>\n')

            num_posters = len(topic_posters[topic])
            topics_file.write(f'<div class="text">{num_posters} Posters</div></a>')

            topics_file.write("</div>")

    # One page per topic with listing
    for topic, items in topic_posters.items():
        topic_fname = topic_filename(topic)
        filepath = filepath.parent.joinpath(topic_fname).with_suffix(".md")
        list_content: List[str] = list()
        for item in items:
            list_item = make_list_item(item, omit="topic")
            list_content.append(list_item)

        with open(filepath, "w") as topic_file:
            colour = TOPIC_COLOURS[topic]
            image_url = f"/{POSTER_REPO}/raw/master/banners/{colour}-wide.png"
            topic_file.write(f'<img height=150 width=1000 alt="Topic: {topic}" '
                             f'src="{image_url}"/>\n')
            topic_file.write(f"# Poster topic: {topic}\n\n")
            topic_file.write("\n".join(list_content) + "\n")


def write_session_index(data: List[Dict[str, str]], filepath: pl.Path):
    session_posters: Dict[str, List[Dict[str, str]]] = dict()
    for item in data:
        session = item["session"]
        if not session:
            continue
        if session not in session_posters:
            session_posters[session] = list()
        session_posters[session].append(item)

    with open(filepath, "w") as sessions_file:
        sessions_file.write("# Poster Sessions\n")
        for session in session_posters:
            sessions_file.write(f"## Session {session}\n")

            num_posters = len(session_posters[session])
            sessions_file.write(f"{num_posters} posters  \n")

            time = SESSION_TIMES[session]
            sessions_file.write(f"**Time:** {time}  \n")

            session_url = urlquote(session_filename(session))
            curr = f"[Browse Session {session} posters](wiki/{session_url})\n<br/><br/>\n"
            sessions_file.write(curr)

    # one page per session with listing
    for session, items in session_posters.items():
        fname = session_filename(session)
        filepath = filepath.parent.joinpath(fname).with_suffix(".md")

        list_content: List[str] = list()
        for item in items:
            list_item = make_list_item(item, omit="session")
            list_content.append(list_item)

        with open(filepath, "w") as session_file:
            session_file.write(f"# Posters in Session {session}\n\n")
            session_file.write("\n".join(list_content) + "\n")


def make_poster_index(data: List[Dict[str, str]], target_dir: pl.Path):
    list_content: List[str] = list()
    for item in data:
        list_content.append(make_list_item(item))

    list_fname = "List.md"
    list_path = target_dir.joinpath(list_fname)
    with open(list_path, "w") as list_file:
        list_file.write("\n".join(list_content))

    index_links: Dict[str, str] = dict()
    index_links["Browse all posters"] = list_fname

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
    with open(home_path, "w") as home_file:
        home_file.write(f"![Posters]({head_img})\n\n")
        home_file.write(head_text + "\n\n")

        for name, fname in index_links.items():
            link = f"/wiki/{fname[:-3]}"
            home_file.write(f"## [{name}]({link})\n\n")


def make_landing_pages(data: List[Dict[str, str]], target_dir: pl.Path):
    print(f"Creating {len(data)} landing pages")
    for idx, item in enumerate(data):
        if idx and not idx % 100:
            print(f" {idx}")
        print(".", end="", flush=True)
        make_landing_page(item, target_dir)
    print()


def make_talks_index(data: List[Dict[str, str]], target_dir: pl.Path):
    home_fname = "Home.md"
    list_content: List[str] = list()

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

    with open(list_path, "w") as list_file:
        list_file.write(f"![{key.capitalize()} talks]({head_img})\n\n")
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


def make_workshop_pages(data: List[Dict[str, str]], target_dir: pl.Path):
    home_fname = "Home.md"

    workshops: Dict[str, Dict[str, Any]] = dict()
    for item in data:
        num = item["workshop number"]
        name = item["workshop name"]
        organisers = item["organisers"]
        url = item["info url"]
        if num not in workshops:
            workshops[num] = dict()
            workshops[num]["name"] = name
            workshops[num]["organisers"] = organisers
            workshops[num]["url"] = url
            workshops[num]["talks"] = list()

        workshops[num]["talks"].append({
            "title": item["talk title"],
            "speakers": item["speakers"],
            "recording": item["recording status"],
            "videourl": item["recording url"],
        })

    list_content: List[str] = list()
    for num, ws_item in workshops.items():
        name = ws_item["name"]
        organisers = ws_item["organisers"]
        url = ws_item["url"]
        ntalks = len(ws_item["talks"])
        entry = f"**[{name}](wiki/Workshop{num})**  \n"
        entry += f"{organisers}  \n"
        entry += f"**Workshop {num}** | {ntalks} talks\n\n"
        list_content.append(entry)

        content = list()
        content.append(f"# {name}\n\n")
        content.append(f"Organizers: {organisers}   \n")
        content.append(f"**[Workshop {num} abstract and schedule]({url})**\n\n")

        for idx, talk in enumerate(ws_item["talks"]):
            title = talk["title"]
            speakers = talk["speakers"]
            rec_status = talk["recording"]
            content.append(f"{idx+1}. {title}  \n")
            content.append(f"{speakers}  \n")

            if vid_url := talk["videourl"]:
                content.append(f"[Video recording]({vid_url})\n")
            elif rec_msg := WORKSHOP_RECORD_MSG[rec_status]:
                content.append(f"*{rec_msg}*\n")

            content.append("\n")

        fname = f"Workshop{num}.md"
        file_path = target_dir.joinpath(fname)
        print(f"Creating landing page {file_path}")
        with open(file_path, "w") as ws_file:
            ws_file.write("".join(content))

    list_path = target_dir.joinpath(home_fname)
    head_text = INDEX_TEXT["workshops"]
    head_img = section_header("workshops")
    print(f"Creating file {list_path} ...")
    with open(list_path, "w") as list_file:
        list_file.write(f"![Workshops]({head_img})\n\n")
        list_file.write(head_text + "\n\n")
        list_file.write("\n".join(list_content))


def make_exhibition_pages(data: List[Dict[str, str]], target_dir: pl.Path):
    home_fname = "Home.md"
    list_content: List[str] = list()

    idx = 0
    for item in data:
        idx = idx + 1
        company = item["company_name"]
        logo = item["logo"]
        website = item["website"]
        headline = item["headline"]
        desc = item["description"]
        hopin = item["hopin"]

        # List page content
        entry = f"**[{company}](wiki/Exhibition{idx})**  \n"
        entry += f"{headline}\n\n\n"
        list_content.append(entry)

        # Landing page content
        content = list()
        if logo:
            content.append(f"![](/raw/master/img/{logo})\n")

        content.append(f"# {company}\n\n")

        # special bullet point handling for the mathworks description
        if company.lower() == "mathworks":
            desc = desc.replace(" o ", "\n- ")

        content.append(f"{desc}\n\n")
        content.append("<div class='ui dividing header'></div>")
        content.append(f"\n\n")

        if website:
            content.append(f"For more information visit the [exhibitor website]("
                           f"{website}).\n\n")

        if hopin:
            content.append(f"If you have any questions, discuss them with "
                           f"moderators at the [exhibitor booth on Hopin]({hopin}).\n")

        # handle materials list
        materials = list(filter(lambda cur: cur.startswith("material_"), data[0].keys()))
        mat_content = list()
        for mat in materials:
            if item[mat]:
                mat_list = f"- ![{item[mat]}](/raw/master/materials/{item[mat]})\n"
                mat_content.append(mat_list)

        if mat_content:
            content.append("## Exhibition materials\n")
            content.append("For your convenience you can access the following "
                           "exhibition materials\n\n")
            content.extend(mat_content)

        fname = f"Exhibition{idx}.md"
        file_path = target_dir.joinpath(fname)
        print(f"Creating landing page {file_path}")
        with open(file_path, "w") as exhib_file:
            exhib_file.write("".join(content))

    list_path = target_dir.joinpath(home_fname)
    head_text = INDEX_TEXT["exhibition"]
    head_img = section_header("exhibition")
    print(f"Creating file {list_path} ...")
    with open(list_path, "w") as list_file:
        list_file.write(f"![Exhibition]({head_img})\n\n")
        list_file.write(head_text + "\n\n")
        list_file.write("\n".join(list_content))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", dest="download", action="store_true",
                        help="Download new files from upload service")
    parser.add_argument("--render-equations", dest="equations", action="store_true",
                        help="Create pngs for LaTeX equations in abstracts")
    parser.add_argument("--workshops", dest="workshops", action="store_true",
                        help="Create workshop pages instead of posters")
    parser.add_argument("--exhibition", dest="exhibition", action="store_true",
                        help="Create exhibition pages instead of posters")
    parser.add_argument("jsonfile", help="JSON file with the poster data")
    parser.add_argument("targetdir",
                        help="Directory in which to create galleries")
    args = parser.parse_args()

    workshops = args.workshops
    exhibition = args.exhibition

    download = args.download
    equations = args.equations
    json_file = args.jsonfile
    target_dir = pl.Path(args.targetdir)
    with open(json_file) as jfp:
        data = json.load(jfp)

    target_dir.mkdir(parents=True, exist_ok=True)
    # Specific handling of workshops
    if workshops:
        # Sanity check to avoid writing invalid workshop galleries
        # Field "workshop number" is 'workshops' specific.
        print("Creating workshop pages ...")
        if not data or "workshop number" not in data[0].keys():
            print(f"'{json_file}' does not seem to be a valid WORKSHOPS file ...")
            print("Aborting ...")
            return

        workshops_dir = target_dir.joinpath("workshops")
        workshops_dir.mkdir(parents=True, exist_ok=True)

        make_workshop_pages(data, workshops_dir)
        return

    # Specific handling of exhibition
    if exhibition:
        # Sanity check to avoid writing invalid exhibition galleries
        # Field "company_name" is 'exhibition' specific.
        print("Creating exhibition pages ...")
        if not data or "company_name" not in data[0].keys():
            print(f"'{json_file}' does not seem to be a valid EXHIBITION file ...")
            print("Aborting ...")
            return

        exhib_dir = target_dir.joinpath("exhibition")
        exhib_dir.mkdir(parents=True, exist_ok=True)

        make_exhibition_pages(data, exhib_dir)
        return

    # Sanity check to avoid writing invalid poster galleries
    # Field "abstract_number" is 'poster' specific.
    if not data or "abstract_number" not in data[0].keys():
        print(f"'{json_file}' does not seem to be a valid POSTERS file ...")
        print("Aborting ...")
        return

    posters_dir = target_dir.joinpath("posters")
    posters_dir.mkdir(parents=True, exist_ok=True)
    invtalks_dir = target_dir.joinpath("invitedtalks")
    invtalks_dir.mkdir(parents=True, exist_ok=True)
    contribtalks_dir = target_dir.joinpath("contributedtalks")
    contribtalks_dir.mkdir(parents=True, exist_ok=True)

    if download:
        print("Downloading posters and URLs ...")
        amiss = download_pdfs(data, posters_dir)
        print("Done ...")
        print(f"PDFs missing:\n{amiss}")

    # Hack to deal with equations for all posters and talk types
    equation_dirs = {"P": posters_dir, "C": contribtalks_dir, "I": invtalks_dir}
    create_equation_images(data, equation_dirs, equations)

    poster_data = list(filter(lambda item: item["short"] == "P", data))
    poster_data = sorted(poster_data,
                         key=make_sorter("abstract_number", apply=int))
    print("Filtering poster data ...")
    poster_data = filter_withdrawn(poster_data)
    print("Creating poster index ...")
    make_poster_index(poster_data, posters_dir)
    print("Creating poster landing pages ...")
    make_landing_pages(poster_data, posters_dir)

    invited_data = list(filter(lambda item: item["short"] == "I", data))
    contrib_data = list(filter(lambda item: item["short"] == "C", data))

    if invited_data:
        print("Creating invited talks index ...")
        make_talks_index(invited_data, invtalks_dir)
        print("Creating invited talks landing pages ...")
        make_landing_pages(invited_data, invtalks_dir)
    else:
        print("WARNING: could not find invited talks")

    if contrib_data:
        print("Creating contributed talks index ...")
        make_talks_index(contrib_data, contribtalks_dir)
        print("Creating contributed talks landing pages ...")
        make_landing_pages(contrib_data, contribtalks_dir)
    else:
        print("WARNING: could not find contributed talks")


if __name__ == "__main__":
    main()
