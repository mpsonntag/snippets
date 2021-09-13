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
    #"Other": "darkblue",
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
    "posters": "Posters can be sorted either by topic or the poster session in which they are presented. To facilitate the overview and sorting of the many posters, they have been assigned to 10 different color-coded topics.",
    "invited": "Video links of invited talks will appear successively in the repository. We only record talks for which we have the speakers’ consent. Please note, these links must not be published anywhere else.",
    "contributed": "Video links of contributed talks will appear successively in the repository. We only record talks for which we have the speakers’ consent. Please note, these links must not be published anywhere else.",
    "workshops": "Video links of workshop talks will appear successively in the repository. We only record talks for which we have the speakers’ consent. Please note, these links must not be published anywhere else.",
    "exhibition": "Here you will find information about the Bernstein Conference exhibitors. They inform about their services and products, and supply supplemental material."
}
# use NEW abstract numbers
WITHDRAWN = [65]
WORKSHOP_RECORD_MSG = {
    "recording": "Video recording will be available",
    "no recording": "Video recording will not be made available",
    "waiting": "",
}


def runcmd(*args):
    ret = sp.run(args, check=False, stdout=sp.PIPE, stderr=sp.PIPE)
    if ret.returncode:
        cmdstr = " ".join(str(arg) for arg in args)
        print(f"Command {cmdstr} failed")
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
    # remove commas and replace spaces with -
    return topic.replace(",", "").replace(" ", "-")


def section_header(section: str) -> str:
    return f"{GALLERY_SERVER}/img/BC_Header_{section}.jpg"


def make_sorter(keyname: str, apply: Callable = None) -> Callable:
    def sorter(row):
        sortval = row[keyname]
        if apply:
            return apply(sortval)
        return sortval

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
        topiclink = ""
        if item["short"] == "P":
            topiclink = topic_filename(topic)
        colour = TOPIC_COLOURS[topic]
        icon_url = f"/{POSTER_REPO}/raw/master/banners/icon-{colour}.png"
        infoline += f" | [![{topic}]({icon_url}) {topic}](/wiki/{topiclink})"
    if omit != "session":
        sessionlink = session_filename(session)
        infoline += f" | [{item_type} session {session}](/wiki/{sessionlink})"
    return f"{infoline}  \n"


def make_list_item(item: Dict[str, str], omit: Optional[str] = None) -> str:
    page = urlquote(f"/wiki/{item_filename(item)}")
    title = item["title"]
    authors = item["authors"]
    titleline = f"**[{title}]({page})**  \n"
    authorline = f"{authors}  \n"
    infoline = make_infoline(item, omit)
    return titleline + authorline + infoline


def create_thumbnail(pdfpath: pl.Path) -> pl.Path:
    """
    Creates a gif thumbnail for a PDF poster and returns the path of the new
    file.  The new file is created in a subdirectory of the PDF path called
    "thumbnails".
    """
    gifname = pdfpath.name[:-3] + "gif"
    thumbdir = pdfpath.parent.joinpath("thumbnails")
    thumbdir.mkdir(exist_ok=True)
    thumbpath = thumbdir.joinpath(gifname)
    runcmd("convert", "-delay", "100", pdfpath, "-thumbnail", "x120", thumbpath)
    return thumbpath


def download_pdfs(data: List[Dict[str, str]], targetdir: pl.Path):
    """
    Downloads posters and video URLs from upload service.
    """
    conn = http.client.HTTPSConnection(POSTER_SERVER, timeout=60)
    poster_dir = targetdir.joinpath("posters")
    poster_dir.mkdir(parents=True, exist_ok=True)

    def download(uuid: str, fname: str, extension: str) -> Optional[pl.Path]:
        nonlocal conn
        try:
            conn.request("GET", f"/uploads/{uuid}.{extension}")
            resp = conn.getresponse()
        except http.client.RemoteDisconnected:
            conn = http.client.HTTPSConnection(POSTER_SERVER, timeout=60)
            return download(uuid, fname, extension)
        pdfdata = resp.read()
        if resp.status == http.client.NOT_FOUND:
            return None
        if resp.status != http.client.OK:
            print(f"Unexpected error: [{resp.status}] {resp.reason}")
            return None

        fpath = poster_dir.joinpath(f"{fname}.{extension}")
        with open(fpath, "wb") as fp:
            fp.write(pdfdata)
        return fpath

    for idx, item in enumerate(data):
        if idx and not idx % 100:
            print(f" {idx}")
        uuid = item["id"]
        number = item["abstract_number"]
        if pdfpath := download(uuid, number, "pdf"):
            print("•", end="", flush=True)
            create_thumbnail(pdfpath)
        else:
            print(".", end="", flush=True)
        download(uuid, number, "url")
    print()


def create_equation_images(data: List[Dict[str, str]], targetdir: Dict[str, pl.Path],
                           create: bool):

    for item in data:
        text = texify(item, targetdir, create)
        item["abstract"] = text


def read_local_url(fname: str, targetdir: pl.Path) -> str:
    poster_dir = targetdir.joinpath("posters")
    urlfile = poster_dir.joinpath(f"{fname}.url")
    if not urlfile.exists():
        return ""

    with open(urlfile, "rb") as ufp:
        return ufp.read().decode()


def sanitize_tex(eqn: str) -> str:
    eqn = eqn.replace("σ", r"\sigma").replace("β", r"\beta").replace("λ", r"\lambda")
    eqn = eqn.replace("ζ", r"\zeta")
    eqn = eqn.replace(r"\tag{1}", "(1)")
    return eqn


def texify(item: Dict[str, str], targetdir: Dict[str, pl.Path], create: bool) -> str:
    """
    Replace LaTeX math snippets with images.
    """
    number = item["abstract_number"]
    text = item["abstract"]
    short = item["short"] if item["short"] in ITEM_TYPES.keys() else "P"

    eqndir = targetdir[short].joinpath("equations")
    eqndir.mkdir(exist_ok=True)
    if match := re.findall(r"\${1,2}.*?\${1,2}", text):
        print(f"Handling equation image for {item['short']}/{item['abstract_number']}")
        for idx, group in enumerate(match):
            imgbasename = f"{number}-{idx}"
            if create:
                sanitized = sanitize_tex(group)
                svg = latex2svg(sanitized)["svg"]
                svgpath = eqndir.joinpath(f"{imgbasename}.svg")
                with open(svgpath, "w") as svgfile:
                    svgfile.write(svg)
                pngpath = eqndir.joinpath(f"{imgbasename}.png")
                runcmd("convert", f"{svgpath}", f"{pngpath}")
            url = f"/raw/master/equations/{imgbasename}.png"
            text = text.replace(group, f"![]({url})")

    return text


def make_landing_page(item: Dict[str, str], targetdir: pl.Path)\
        -> Optional[pl.Path]:
    title = item["title"]
    authors = item["authors"]
    # session = item["session"]
    # topic = item["topic"]
    number = item["abstract_number"]
    text = item["abstract"]
    time = item["time"]
    vimeo_video_url = item["vimeo link"]
    hopin_url = item["link hopin"]
    user_video_url = read_local_url(number, targetdir)
    bcos_video_url = item["individual video link"]  # sent to bcos directly; put in spreadsheet
    cit_list = item["citation"]
    doi_item = item["doi"]

    # if vimeo_video_url and user_video_url:
    #     print("Warning: Video URLs found in both sources:")
    #     print(f"User URL:  {vimeo_video_url}")
    #     print(f"Vimeo URL: {user_video_url}")
    #     print("Using vimeo URL")

    video_url = vimeo_video_url if vimeo_video_url else user_video_url
    if not video_url:
        video_url = bcos_video_url

    if not hopin_url:
        hopin_url = "https://hopin.to"

    if not title:
        item_id = item["id"]
        print(f"Poster with ID {item_id} has no title")
        return None

    file_basename = item_filename(item)
    filename = targetdir.joinpath(f"{file_basename}.md")

    poster_url = f"/src/master/posters/{number}.pdf"
    poster_thumb_url = (f"/{POSTER_REPO}/raw/master/posters/thumbnails/"
                        f"{number}.gif")

    year = date.today().year
    doi_item = f" doi: [{doi_item}](https://doi.org/{doi_item})" if doi_item else ""
    copy_item = f"__Copyright:__ © ({year}) {cit_list}\n" if cit_list else ""
    cit_item = f"__Citation:__ {cit_list} ({year}) {title}. " \
               f"Bernstein Conference {year}.{doi_item}"

    with open(filename, "w") as posterpage:
        posterpage.write(f"# {title}\n\n")
        posterpage.write(f"_{authors}_\n\n")
        if item["short"] == "P":
            posterpage.write(make_infoline(item) + "\n\n")
            posterpage.write(f"[![Poster]({poster_thumb_url})]({poster_url}) ")
        if video_url:
            posterpage.write(f"[![Video]({VIDEO_ICON_URL})]({video_url})")
        posterpage.write("\n\n")
        if time:
            posterpage.write(f"**Session time**: {time} | "
                             f"[Hopin roundtable]({hopin_url})\n\n")
        posterpage.write("## Abstract\n\n")
        posterpage.write(text)
        posterpage.write("\n\n---\n\n")

        posterpage.write(f"{copy_item}\n")
        posterpage.write(f"{cit_item}\n\n")

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

    with open(filepath, "w") as topicsfile:
        topicsfile.write("# Poster topics\n\n")
        for topic, colour in TOPIC_COLOURS.items():
            topicsfile.write('<div class="banner">\n')
            topicurl = urlquote(topic_filename(topic))
            topicsfile.write(f'<a href="{topicurl}">')
            imageurl = f"/{POSTER_REPO}/raw/master/banners/{colour}.png"
            topicsfile.write(f'<img width=300 alt="Topic: {topic}" '
                             f'src="{imageurl}"/>\n')
            topicsfile.write(f'<div class="title">{topic}</div>\n')
            nposters = len(topic_posters[topic])
            topicsfile.write(f'<div class="text">{nposters} Posters</div></a>')
            topicsfile.write("</div>")

    # one page per topic with listing
    for topic, items in topic_posters.items():
        topic_fname = topic_filename(topic)
        filepath = filepath.parent.joinpath(topic_fname).with_suffix(".md")
        list_content: List[str] = list()
        for item in items:
            list_item = make_list_item(item, omit="topic")
            list_content.append(list_item)
        with open(filepath, "w") as topicfile:
            colour = TOPIC_COLOURS[topic]
            imageurl = f"/{POSTER_REPO}/raw/master/banners/{colour}-wide.png"
            topicfile.write(f'<img height=150 width=1000 alt="Topic: {topic}" '
                            f'src="{imageurl}"/>\n')
            topicfile.write(f"# Poster topic: {topic}\n\n")
            topicfile.write("\n".join(list_content) + "\n")


def write_session_index(data: List[Dict[str, str]], filepath: pl.Path):
    session_posters: Dict[str, List[Dict[str, str]]] = dict()
    for item in data:
        session = item["session"]
        if not session:
            continue
        if session not in session_posters:
            session_posters[session] = list()
        session_posters[session].append(item)

    with open(filepath, "w") as sessionsfile:
        sessionsfile.write("# Poster Sessions\n")
        for session in session_posters:
            sessionurl = urlquote(session_filename(session))
            sessionsfile.write(f"## Session {session}\n")
            nposters = len(session_posters[session])
            sessionsfile.write(f"{nposters} posters  \n")
            time = SESSION_TIMES[session]
            sessionsfile.write(f"**Time:** {time}  \n")
            sessionsfile.write(f"[Browse Session {session} posters]"
                               f"(wiki/{sessionurl})\n<br/><br/>\n")

    # one page per session with listing
    for session, items in session_posters.items():
        sessfname = session_filename(session)
        filepath = filepath.parent.joinpath(sessfname).with_suffix(".md")
        list_content: List[str] = list()
        for item in items:
            list_item = make_list_item(item, omit="session")
            list_content.append(list_item)
        with open(filepath, "w") as sessionfile:
            sessionfile.write(f"# Posters in Session {session}\n\n")
            sessionfile.write("\n".join(list_content) + "\n")


def make_poster_index(data: List[Dict[str, str]], targetdir: pl.Path):
    list_content: List[str] = list()
    for item in data:
        # list
        list_content.append(make_list_item(item))

    index_links: Dict[str, str] = dict()
    list_fname = "List.md"
    list_path = targetdir.joinpath(list_fname)
    with open(list_path, "w") as listfile:
        listfile.write("\n".join(list_content))
    index_links["Browse all posters"] = list_fname

    topics_fname = "Topics.md"
    topics_path = targetdir.joinpath(topics_fname)
    write_topic_index(data, topics_path)
    index_links["Browse posters by Topic"] = topics_fname

    sessions_fname = "Sessions.md"
    sessions_path = targetdir.joinpath(sessions_fname)
    write_session_index(data, sessions_path)
    index_links["Browse posters by Session"] = sessions_fname

    home_fname = "Home.md"
    home_path = targetdir.joinpath(home_fname)
    head_img = section_header("posters")
    head_text = INDEX_TEXT["posters"]
    with open(home_path, "w") as homefile:
        homefile.write(f"![Posters]({head_img})\n\n")
        homefile.write(head_text + "\n\n")

        for name, fname in index_links.items():
            link = f"/wiki/{fname[:-3]}"
            homefile.write(f"## [{name}]({link})\n\n")


def make_landing_pages(data: List[Dict[str, str]], targetdir: pl.Path):
    print(f"Creating {len(data)} landing pages")
    for idx, item in enumerate(data):
        if idx and not idx % 100:
            print(f" {idx}")
        print(".", end="", flush=True)
        make_landing_page(item, targetdir)
    print()


def make_talks_index(data: List[Dict[str, str]], targetdir: pl.Path):
    home_fname = "Home.md"
    list_content: List[str] = list()

    for item in data:
        list_content.append(make_list_item(item, omit="session"))
    list_path = targetdir.joinpath(home_fname)

    key = ""
    if data[0]["short"] == "C":
        key = "contributed"
    elif data[0]["short"] == "I":
        key = "invited"
    head_img = section_header(key)
    head_text = INDEX_TEXT[key]
    with open(list_path, "w") as listfile:
        listfile.write(f"![{key.capitalize()} talks]({head_img})\n\n")
        listfile.write(head_text + "\n\n")
        listfile.write("\n".join(list_content))


def filter_withdrawn(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Poster numbers for withdrawn entries are filtered out here.
    """
    for entry in data[:]:
        if int(entry["abstract_number"]) in WITHDRAWN:
            print(f"REMOVE withdrawn {entry['title']}")
            data.remove(entry)

    return data


def make_workshop_pages(data: List[Dict[str, str]], targetdir: pl.Path):
    workshops: Dict[str, Dict[str, Any]] = dict()
    home_fname = "Home.md"
    list_content: List[str] = list()

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

    for num, ws in workshops.items():
        name = ws["name"]
        organisers = ws["organisers"]
        url = ws["url"]
        ntalks = len(ws["talks"])
        entry = f"**[{name}](wiki/Workshop{num})**  \n"
        entry += f"{organisers}  \n"
        entry += f"**Workshop {num}** | {ntalks} talks\n\n"
        list_content.append(entry)

        content = list()
        content.append(f"# {name}\n\n")
        content.append(f"Organizers: {organisers}   \n")
        content.append(f"**[Workshop {num} abstract and schedule]({url})**\n\n")

        for idx, talk in enumerate(ws["talks"]):
            title = talk["title"]
            speakers = talk["speakers"]
            recstatus = talk["recording"]
            content.append(f"{idx+1}. {title}  \n")
            content.append(f"{speakers}  \n")
            if vidurl := talk["videourl"]:
                content.append(f"[Video recording]({vidurl})\n")
            elif recmsg := WORKSHOP_RECORD_MSG[recstatus]:
                content.append(f"*{recmsg}*\n")
            content.append("\n")

        fname = f"Workshop{num}.md"
        file_path = targetdir.joinpath(fname)
        print(f"Creating landing page {file_path}")
        with open(file_path, "w") as wsfile:
            wsfile.write("".join(content))

    list_path = targetdir.joinpath(home_fname)
    head_text = INDEX_TEXT["workshops"]
    head_img = section_header("workshops")
    print(f"Creating file {list_path} ...")
    with open(list_path, "w") as listfile:
        listfile.write(f"![Workshops]({head_img})\n\n")
        listfile.write(head_text + "\n\n")
        listfile.write("\n".join(list_content))


def make_exhibition_pages(data: List[Dict[str, str]], targetdir: pl.Path):
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
        content.append(f"{desc}\n")
        content.append("<div class='ui dividing header'></div>")

        if website:
            content.append(f"For more information visit the [exhibitor website]({website}).\n\n")

        if hopin:
            content.append(f"If you have any questions, discuss them with "
                           f"moderators at the [exhibitor booth on Hopin]({hopin}).\n")

        # handle materials list
        materials = list(filter(lambda mat: mat.startswith("material_"), data[0].keys()))
        mat_content = list()
        for mat in materials:
            if item[mat]:
                mat_content.append(f"- ![{item[mat]}](/raw/master/materials/{item[mat]})\n")

        if mat_content:
            content.append("## Exhibition materials\n")
            content.append("For your convenience you can access the following "
                           "exhibition materials\n\n")
            content.extend(mat_content)

        fname = f"Exhibition{idx}.md"
        file_path = targetdir.joinpath(fname)
        print(f"Creating landing page {file_path}")
        with open(file_path, "w") as exhib_file:
            exhib_file.write("".join(content))

    list_path = targetdir.joinpath(home_fname)
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
    jsonfile = args.jsonfile
    targetdir = pl.Path(args.targetdir)
    with open(jsonfile) as jfp:
        data = json.load(jfp)

    targetdir.mkdir(parents=True, exist_ok=True)
    # Specific handling of workshops
    if workshops:
        # Sanity check to avoid writing invalid workshop galleries
        # Field "workshop number" is 'workshops' specific.
        print("Creating workshop pages ...")
        if not data or "workshop number" not in data[0].keys():
            print(f"'{jsonfile}' does not seem to be a valid WORKSHOPS file ...")
            print("Aborting ...")
            return

        workshopsdir = targetdir.joinpath("workshops")
        workshopsdir.mkdir(parents=True, exist_ok=True)

        make_workshop_pages(data, workshopsdir)
        return

    # Specific handling of exhibition
    if exhibition:
        # Sanity check to avoid writing invalid exhibition galleries
        # Field "company_name" is 'exhibition' specific.
        print("Creating exhibition pages ...")
        if not data or "company_name" not in data[0].keys():
            print(f"'{jsonfile}' does not seem to be a valid EXHIBITION file ...")
            print("Aborting ...")
            return

        exhib_dir = targetdir.joinpath("exhibition")
        exhib_dir.mkdir(parents=True, exist_ok=True)

        make_exhibition_pages(data, exhib_dir)
        return

    # Sanity check to avoid writing invalid poster galleries
    # Field "abstract_number" is 'poster' specific.
    if not data or "abstract_number" not in data[0].keys():
        print(f"'{jsonfile}' does not seem to be a valid POSTERS file ...")
        print("Aborting ...")
        return

    postersdir = targetdir.joinpath("posters")
    postersdir.mkdir(parents=True, exist_ok=True)
    invtalksdir = targetdir.joinpath("invitedtalks")
    invtalksdir.mkdir(parents=True, exist_ok=True)
    contribtalksdir = targetdir.joinpath("contributedtalks")
    contribtalksdir.mkdir(parents=True, exist_ok=True)

    if download:
        print("Downloading posters and URLs")
        download_pdfs(data, postersdir)
        print("Done")

    # Hack to deal with equations for all posters and talk types
    equation_dirs = {"P": postersdir, "C": contribtalksdir, "I": invtalksdir}
    create_equation_images(data, equation_dirs, equations)

    posterdata = list(filter(lambda item: item["short"] == "P", data))
    posterdata = sorted(posterdata,
                        key=make_sorter("abstract_number", apply=int))
    print("Filtering poster data ...")
    posterdata = filter_withdrawn(posterdata)
    print("Creating poster index ...")
    make_poster_index(posterdata, postersdir)
    print("Creating poster landing pages ...")
    make_landing_pages(posterdata, postersdir)

    inviteddata = list(filter(lambda item: item["short"] == "I", data))
    contribdata = list(filter(lambda item: item["short"] == "C", data))

    if inviteddata:
        print("Creating invited talks index ...")
        make_talks_index(inviteddata, invtalksdir)
        print("Creating invited talks landing pages ...")
        make_landing_pages(inviteddata, invtalksdir)
    else:
        print("WARNING: could not find invited talks")

    if contribdata:
        print("Creating contributed talks index ...")
        make_talks_index(contribdata, contribtalksdir)
        print("Creating contributed talks landing pages ...")
        make_landing_pages(contribdata, contribtalksdir)
    else:
        print("WARNING: could not find contributed talks")


if __name__ == "__main__":
    main()
