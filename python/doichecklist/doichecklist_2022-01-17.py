#!/usr/bin/env python3

"""doichecklist

doichecklist prints a checklist for DOI registrations
to an output file in the same directory.

Usage: doichecklist [--config CONFIG_FILE]

Options:
    --config CONFIG_FILE    yaml file
    -h --help               Show this screen.
    --version               Show version.
"""

import os
import sys

from datetime import datetime
from uuid import uuid4

import requests

from docopt import docopt
from yaml import load as y_load
from yaml import SafeLoader


# Default configuration struct containing non problematic test values
CONF = {
        # Entries required for every DOI request
        # Paste basic information from the corresponding issue on
        #   https://gin.g-node.org/G-Node/DOIMetadata
        # Automated registration [id] from "10.12751/g-node.[id]"
        "reg_id": "__ID__",
        # Repository owner
        "repo_own": "__OWN__",
        # Repository name
        "repo": "__REPO__",
        # Date issued from doi.xml; Format YYYY-MM-DD
        "reg_date": "__DATE__",
        # DOI requestee email address
        "email": "__MAIL__",
        # DOI requestee full name
        "user_full_name": "__USER_FULL__",
        # Entries that are usually handled automatically via repo datacite entry
        # DOI request title; usually handled automatically via repo datacite entry
        "title": "__TITLE__",
        # Author citation list; usually handled automatically via repo datacite entry
        "citation": "__CITATION__",
        # Entries that are set once and remain unchanged for future DOI requests
        # User working on the DOI server
        "server_user": "__SERVER_USER__",
        # Full name of the person handling the registration; used in email template texts
        "admin_name": "__FIRST LAST__",
        # Local staging dir to create index and keyword pages
        "dir_local_stage": "__DIR_LOCAL_STAGE__",
        # Full ssh access name of the server hosting the GIN server instance
        "gin_server": "__GIN.SERVER__",
        # Full ssh access name of the server hosting the DOI server instance
        "doi_server": "__DOI.SERVER__",
        # DOI Server repo preparation directory
        "dir_doi_prep": "__DIR_DOI_PREP__",
        # DOI Server root doi hosting directory
        "dir_doi": "__DIR_DOI__"
}


def text_pre_fork():
    text_block = f"""

-[ ] manually fork repository to the 'doi' gin user
    - log on to gin.g-node.org using the "doi" user
    - fork https://gin.g-node.org/{CONF["repo_own"]}/{CONF["repo"]}"""

    return text_block


def text_pre_fork_upload(screen_id):
    dir_path = f"""{CONF["dir_doi_prep"]}/10.12751/g-node.{CONF["reg_id"]}/{CONF["repo"].lower()}"""
    logfile = f"""{CONF["repo_own"].lower()}-{CONF["repo"].lower()}.log"""

    text_block = f"""

-[ ] log on to the DOI server ({CONF["doi_server"]}) and move to {CONF["dir_doi_prep"]}
- Make sure all information has been properly downloaded to the staging directory and
  all annex files are unlocked and the content is present:
    -[ ] {CONF["dir_doi_prep"]}/annexcheck {dir_path}
    -[ ] find {CONF["dir_doi_prep"]}/10.12751/g-node.{CONF["reg_id"]} -type l -print
    -[ ] grep annex.objects $(find {CONF["dir_doi_prep"]}/10.12751/g-node.{CONF["reg_id"]} -type f -size -100c -print)
    -[ ] check that the content size of the repository and the created zip file matches
    -[ ] if there still are symlinks present or the content size does not match up, the zip
         file does not contain all required data. Run the next steps - the script will
         download all missing information and upload to the DOI fork. When recreating the
         zip file, all files will be manually unlocked first.
-[ ] fetch git and annex content and upload annex content to the DOI fork repo.
     use screen to avoid large down- and uploads to be interrupted.
     use CTRL+a+d to switch out of screen sessions without interruption.
     use either the logfile or 'htop' to check on the status of the download/upload.
    - screen -S {screen_id}
    - sudo su root
    - ./doiforkupload {dir_path} > {logfile}
-[ ] after detaching from the session, check the log file until the upload starts to avoid
     any security check issues.
     Also read the commit hash comparison line to check if the content of the repo has
     been changed after the DOI request has been submitted.
     tail -f {logfile}
-[ ] if a) the logfile contains the line "repo was not at the DOI request state" the
     repository was changed after the DOI request and the uploaded archive content will
     most likely differ from the zip file content. If b) the 'tree' command showed symlinks or 
     missing content, the zip file will also not contain the file content for all files.
       In this case use the 'makezip' bash script to recreate the zip file and 
     copy it to the the DOI hosting folder.
-[ ] once the upload is done, check that the git tag has been created on the DOI fork repository at
     https://gin.g-node.org/doi/{CONF["repo"]}."""

    return text_block


def text_pre_fork_sync(screen_id):
    logfile = f"""{CONF["repo_own"].lower()}-{CONF["repo"].lower()}.log"""

    text_block = f"""

-[ ] log on to the DOI server ({CONF["doi_server"]}) and move to {CONF["dir_doi_prep"]}
-[ ] fetch git and annex content and upload annex content to the DOI fork repo.
     use screen to avoid large down- and uploads to be interrupted.
     use CTRL+a+d to switch out of screen sessions without interruption.
     use either the logfile or 'htop' to check on the status of the download/upload.
    - screen -S {screen_id}
    - sudo su root
    - ./syncannex {CONF["repo_own"]}/{CONF["repo"]} > {logfile}"""

    return text_block


def text_pre_git_tag():
    text_block = f"""

- create release tag on the DOI repository; run all commands using `gin git ...` 
  to avoid issues with local git annex or other logged git users.
    -[ ] cd {CONF["dir_doi_prep"]}/{CONF["repo"].lower()}
    -[ ] check that "doi" is the set origin: sudo gin git remote -v
    -[ ] sudo gin git tag 10.12751/g-node.{CONF["reg_id"]}
    -[ ] sudo gin git push --tags origin"""
    return text_block


def text_pre_cleanup(screen_id, full_doi=False):
    logfiles = f"""{CONF["repo_own"].lower()}-{CONF["repo"].lower()}*.log"""
    dir_path = f"""{CONF["dir_doi_prep"]}/10.12751/g-node.{CONF["reg_id"]}"""
    if full_doi:
        dir_path = f"""{CONF["dir_doi_prep"]}/{CONF["repo"].lower()}"""

    text_block = f"""

- cleanup directory once tagging is done
    -[ ] sudo rm {dir_path} -r
    -[ ] sudo mv {CONF["dir_doi_prep"]}/{logfiles} /home/{CONF["server_user"]}/logs/
    -[ ] cleanup screen session: screen -XS {screen_id} quit"""

    return text_block


def print_part_pre_doi(fip):
    """
    Print pre-registration block to file

    :param fip: filepointer
    """
    text_block = f"""# Part 1 - pre registration

## Base request information
-[ ] check if the following information is correct; re-run script otherwise with updated config

    DOI request
    - Repository: {CONF["repo_own"]}/{CONF["repo"]}
    - User: ({CONF["user_full_name"]})
    - Email address: {CONF["email"]}
    - DOI XML: {CONF["doi_server"]}:/data/doi/10.12751/g-node.{CONF["reg_id"]}/doi.xml
    - DOI target URL: https://doi.gin.g-node.org/10.12751/g-node.{CONF["reg_id"]}

    - Request Date (as in doi.xml): {CONF["reg_date"]}

"""
    low_repo_own = CONF["repo_own"].lower()
    low_repo = CONF["repo"].lower()
    fip.write(text_block)

    fip.write("## Base pre-registration checks")

    text_block = f"""
-[ ] GIN server ({CONF["gin_server"]}) check annex content
    - /gindata/annexcheck /gindata/gin-repositories/{low_repo_own}/{low_repo}.git"""
    fip.write(text_block)

    text_block = f"""

- check the datacite content at 
  https://gin.g-node.org/{CONF["repo_own"]}/{CONF["repo"]}
    -[ ] repo is eligible to be published via GIN DOI
    -[ ] the repo name is sufficiently unique to avoid clashes when 
         forking to the DOI GIN user.
    -[ ] resourceType e.g. Dataset fits the repository
    -[ ] title is useful and has no typos
    -[ ] automated issues are all addressed
"""
    fip.write(text_block)


def print_part_pre_doi_semi(fip):
    """
    Print semi automatic DOI pre-registration block to file

    :param fip: filepointer
    """
    text_block = """
## Semi-automated DOI or DOI update
- use this section if there are no technical or other issues with the DOI request 
  and skip the 'Full DOI' section.
- also use this section if there were no issues and an update to an existing DOI has
  been requested. The 'doiforkupload' script does both initial upload and update."""
    fip.write(text_block)

    text_block = f"""

- on the DOI server ({CONF["doi_server"]}) check the DOI directory content
    -[ ] zip file created in {CONF["dir_doi"]}/10.12751/g-node.{CONF["reg_id"]}
    -[ ] check zip file content
         unzip -vl {CONF["dir_doi"]}/10.12751/g-node.{CONF["reg_id"]}/10.12751_g-node.{CONF["reg_id"]}.zip
    -[ ] note zip size

-[ ] remove {CONF["dir_doi"]}/10.12751/g-node.{CONF["reg_id"]}/.htaccess

- access https://doi.gin.g-node.org/10.12751/g-node.{CONF["reg_id"]}
    -[ ] check landing page in general
    -[ ] check title, license name
    -[ ] check all links that should work at this stage
    -[ ] check zip download and compare size on server with size in `doi.xml`"""
    fip.write(text_block)

    text_block = text_pre_fork()
    fip.write(text_block)

    screen_id = f"{CONF['repo_own'].lower()}-{str(uuid4())[0:5]}"
    text_block = text_pre_fork_upload(screen_id)
    fip.write(text_block)

    text_block = text_pre_cleanup(screen_id)
    fip.write(text_block)

    text_block = f"""

-[ ] Check link to archive repo on the DOI landing page works:
     https://doi.gin.g-node.org/10.12751/g-node.{CONF["reg_id"]}

-[ ] issue comment on https://gin.g-node.org/G-Node/DOImetadata/issues
     New publication request: {CONF["repo_own"].lower()}/{CONF["repo"].lower()} (10.12751/g-node.{CONF["reg_id"]})

     This repository is prepared for the DOI registration.
"""
    fip.write(text_block)


def print_part_pre_doi_full(fip):
    """
    Print optional full DOI pre-registration block to file.

    :param fip: filepointer
    """
    text_block = """
## Full DOI
- This usually has to be done when
  a) the semi-automated process has failed or
  b) the user requested changes but needs to keep the originally issued DOI"""
    fip.write(text_block)

    text_block = text_pre_fork()
    fip.write(text_block)

    screen_id = f"{CONF['repo_own'].lower()}-{str(uuid4())[0:5]}"
    text_block = text_pre_fork_sync(screen_id)
    fip.write(text_block)

    zip_log = f"{CONF['repo_own'].lower()}-{CONF['repo'].lower()}_zip.log"
    file_name = f"10.12751_g-node.{CONF['reg_id']}.zip"
    zip_file = f"{CONF['dir_doi']}/10.12751/g-node.{CONF['reg_id']}/{file_name}"

    text_block = f"""

-[ ] create DOI zip file
    - screen -r {screen_id}
    - sudo ./makezip {CONF["repo"].lower()} > {zip_log}

-[ ] make sure there is no zip file in the target directory left 
     from the previous registration process.

-[ ] sudo mv {CONF["repo"].lower()}.zip {zip_file}"""
    fip.write(text_block)

    text_block = text_pre_git_tag()
    fip.write(text_block)

    text_block = text_pre_cleanup(screen_id, True)
    fip.write(text_block)

    text_block = f"""

-[ ] edit {CONF["dir_doi"]}/10.12751/g-node.{CONF["reg_id"]}/doi.xml file to reflect
     any changes in the repo datacite.yml file.
    - include the actual size of the zip file
    - check proper title and proper license
    - any added or updated funding or reference information
    - any changes to the 'resourceType'"""
    fip.write(text_block)

    text_block = f"""

- remove the .htaccess file
- create the DOI landing page in the local staging directory and move it to the DOI server
    -[ ] cd {CONF["dir_local_stage"]}
    -[ ] gindoid make-html https://doi.gin.g-node.org/10.12751/g-node.{CONF["reg_id"]}/doi.xml
    -[ ] scp {CONF["dir_local_stage"]}/10.12751/g-node.{CONF["reg_id"]}/index.html {CONF["server_user"]}@{CONF["doi_server"]}:/home/{CONF["server_user"]}/staging
    - move to the DOI server staging directory
    -[ ] sudo chown root:root index.html
    -[ ] sudo mv index.html {CONF["dir_doi"]}/10.12751/g-node.{CONF["reg_id"]}/index.html"""
    fip.write(text_block)

    text_block = f"""

- https://doi.gin.g-node.org/10.12751/g-node.{CONF["reg_id"]}
    -[ ] check page access, size, title, license name
    -[ ] check all links that should work at this stage
    -[ ] check zip download and suggested size"""
    fip.write(text_block)

    text_block = f"""

-[ ] issue comment on https://gin.g-node.org/G-Node/DOImetadata/issues
     New publication request: {CONF["repo_own"].lower()}/{CONF["repo"].lower()} (10.12751/g-node.{CONF["reg_id"]})

     This repository is prepared for the DOI registration.
"""
    fip.write(text_block)


def print_part_post_doi(fip):
    """
    Print post-registration block to file.

    :param fip: filepointer
    """
    from_dir = f"{CONF['dir_local_stage']}/keywords"
    to_server = f"{CONF['server_user']}@{CONF['doi_server']}:/home/{CONF['server_user']}/staging"

    text_block = f"""
# Part 2 - post registration
- re-create and deploy keywords if required
  -[ ] make sure github.com/G-Node/gin-doi is locally built and the `gindoid` executable available
  -[ ] gin get G-Node/DOImetadata to local staging directory
  -[ ] create empty "keywords" directory and run the following from it
  -[ ] {CONF["dir_local_stage"]}/gindoid make-keyword-pages {CONF["dir_local_stage"]}/DOImetadata/*.xml
  -[ ] scp -r {from_dir} {to_server}"""
    fip.write(text_block)

    text_block = f"""
  -[ ] connect to DOI server ({CONF["doi_server"]})
  -[ ] sudo chown -R root:root /home/{CONF["server_user"]}/staging/keywords
  -[ ] sudo mv {CONF["dir_doi"]}/keywords {CONF["dir_doi"]}/keywords_
  -[ ] sudo mv /home/{CONF["server_user"]}/staging/keywords/ {CONF["dir_doi"]}
  -[ ] check landing page and keywords online: https://doi.gin.g-node.org
  -[ ] sudo rm {CONF["dir_doi"]}/keywords_ -r"""
    fip.write(text_block)

    text_block = f"""

-[ ] connect to DOI server ({CONF["doi_server"]}) and update `{CONF["dir_doi"]}/index.html`; 
     make sure there are no unintentional line breaks!
                        <tr>
                            <td><a href="https://doi.org/10.12751/g-node.{CONF["reg_id"]}">{CONF["title"]}</a>
                            <br>{CONF["citation"]}</td>
                            <td>{CONF["reg_date"]}</td>
                            <td><a href="https://doi.org/10.12751/g-node.{CONF["reg_id"]}" class ="ui grey label">10.12751/g-node.{CONF["reg_id"]}</a></td>
                        </tr>

-[ ] update `{CONF["dir_doi"]}/urls.txt`: https://doi.gin.g-node.org/10.12751/g-node.{CONF["reg_id"]}"""
    fip.write(text_block)

    text_block = f"""

-[ ] git commit all changes in {CONF["dir_doi"]}
    - sudo git add 10.12751/g-node.{CONF["reg_id"]}/
    - sudo git commit -m "New dataset: 10.12751/g-node.{CONF["reg_id"]}"

-[ ] commit keyword and index page changes
    - sudo git add keywords/
    - sudo git add index.html
    - sudo git add urls.txt
    - sudo git commit -m "Update index and keyword pages"

-[ ] set zip to immutable
    sudo chattr +i {CONF["dir_doi"]}/10.12751/g-node.{CONF["reg_id"]}/10.12751_g-node.{CONF["reg_id"]}.zip

-[ ] cleanup any leftover directories from previous versions 
     of this dataset in the {CONF["dir_doi"]}/10.12751/ and 
    {CONF["dir_doi_prep"]}/10.12751/ directories.

-[ ] email to user (check below)"""
    fip.write(text_block)

    text_block = f"""

-[ ] close all related issues on https://gin.g-node.org/G-Node/DOImetadata/issues
     New publication request: {CONF["repo_own"].lower()}/{CONF["repo"].lower()} (10.12751/g-node.{CONF["reg_id"]})

    Publication finished and user informed.
"""
    fip.write(text_block)


def print_part_ready_email(fip):
    """
    Print DOI registration ready email block to file.

    :param fip: filepointer
    """
    # a bit nasty but I think good enough
    cite_year = datetime.now().strftime("%Y")

    text_block = f"""
# Part 3 - eMail to user
-[ ] make sure the publication reference text does apply, remove otherwise

{CONF["email"]}

CC: gin@g-node.org

Subject: DOI registration complete - {CONF["repo_own"]}/{CONF["repo"]}

Dear {CONF["user_full_name"]},

Your dataset with title
  {CONF["title"]}

has been successfully registered.

The DOI for the dataset is
  https://doi.org/10.12751/g-node.{CONF["reg_id"]}

Please always reference the dataset by its DOI (not the link to the
repository) and cite the dataset as
  {CONF["citation"]} ({cite_year})
  {CONF["title"]}
  G-Node. https://doi.org/10.12751/g-node.{CONF["reg_id"]}

If this is data supplementing a publication and if you haven't done so already, we kindly request that you:
- include the new DOI of this dataset in the publication as a reference, and
- update the datacite file of the registered dataset to reference the publication, including its DOI, once it is known.

The latter will result in a link in the Datacite database to your publication and will increase its discoverability.

Best regards,
  {CONF["admin_name"]}
  German Neuroinformatics Node
"""
    fip.write(text_block)


def run():
    owner = CONF["repo_own"].lower()
    if len(CONF["repo_own"]) > 5:
        owner = owner[0:5]
    repo_name = CONF["repo"].lower()
    if len(CONF["repo"]) > 10:
        repo_name = repo_name[0:15]

    c_date = datetime.now().strftime("%Y%m%d")
    out_file = f"{c_date}_{CONF['reg_id'].lower()}-{owner}-{repo_name}.md"
    print(f"-- Writing to file {out_file}")
    with open(out_file, "w", encoding="utf-8") as fip:
        print_part_pre_doi(fip)
        print_part_pre_doi_semi(fip)
        print_part_pre_doi_full(fip)
        print_part_post_doi(fip)
        print_part_ready_email(fip)

    print(f"-- Finished writing file {out_file}")


def update_conf(conf):
    for val in conf:
        if val in CONF:
            CONF[val] = conf[val]
        else:
            print(f"-- WARN: ignoring unknown config field '{val}'")


def update_conf_from_file(conf_file):
    with open(conf_file, "r", encoding="utf-8") as fip:
        conf = y_load(fip, Loader=SafeLoader)

    update_conf(conf)


def parse_repo_datacite():
    """
    Tries to access the request repository datacite file and parse the 'title'
    and the 'citation' from the files authors list.
    If the file cannot be accessed or there are any issues the script continues
    since both title and citation are not essential for the checklist.

    :return: struct to update the main config
    """
    print(f"-- Loading datacite file for '{CONF['repo_own']}/{CONF['repo']}'")
    base_url = "https://gin.g-node.org"
    datacite_url = f"{base_url}/{CONF['repo_own']}/{CONF['repo']}/raw/master/datacite.yml"
    res = requests.get(datacite_url)

    # Return with an error message but continue the script on an access error
    if res.status_code != 200:
        msg = f"-- ERROR: Status code ({res.status_code}); could not access datacite file.\n"
        msg += "          Make sure to fill in 'title' and 'citation' in the checklist."
        print(msg)
        return {}

    datacite = y_load(res.text, Loader=SafeLoader)

    doi_conf = {}

    # Handle title
    title = datacite["title"] if "title" in datacite else ""
    if title:
        doi_conf["title"] = title

    # Handle citation
    if "authors" in datacite:
        cit = []
        for creator in datacite["authors"]:
            lan = creator["lastname"] if "lastname" in creator else ""
            fin = ""
            if "firstname" in creator:
                for init in creator["firstname"].split():
                    fin = f"{fin}{init[0]}"

            if lan or fin:
                cit.append(" ".join([lan, fin.strip()]).strip())
        doi_conf["citation"] = ", ".join(cit)

    return doi_conf


def parse_args(args):
    parser = docopt(__doc__, argv=args, version="0.1.0")
    if parser['--config']:
        conf_file = parser['--config']
        if not os.path.isfile(conf_file):
            print(f"-- ERROR: Cannot open config file '{conf_file}'")
            sys.exit(-1)

        update_conf_from_file(conf_file)
    elif os.path.isfile("conf.yaml"):
        print("-- Using local 'conf.yaml' file")
        update_conf_from_file("conf.yaml")


if __name__ == "__main__":
    if sys.version_info.major < 3 or (sys.version_info.major > 2 and sys.version_info.minor < 6):
        print("-- ERROR: invalid Python version. Use Python 3.6+ to run this script")
        sys.exit(-1)

    if sys.argv[1:]:
        parse_args(sys.argv[1:])
    elif os.path.isfile("conf.yaml"):
        print("-- Using local 'conf.yaml' file")
        update_conf_from_file("conf.yaml")
    else:
        print("-- Using script default config")

    # Update 'title' and 'citation' from repo datacite
    update_conf(parse_repo_datacite())

    run()
