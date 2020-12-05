"""create_registration_script

create_registration_script prints a checklist for DOI registrations.

Usage: create_registration_script [--config CONFIG_FILE] [--doi]

Options:
    --config CONFIG_FILE    yaml file
    --doi                   fetch 'title', 'date' and 'citation' from doi.gin.g-node.org.
                            The doi.xml file has to be accessible.
                            Overrules config file entries.
    -h --help               Show this screen.
    --version               Show version.
"""

import os
import requests
import sys

from datetime import datetime
from uuid import uuid4

from docopt import docopt
from lxml import etree
from yaml import load as y_load
from yaml import SafeLoader


# Default configuration struct containing non problematic test values
CONF = {
        # Paste basic information from corresponding issue on
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
        # DOI request title; can be handled via --doi CL option
        "title": "__TITLE__",
        # Author citation list; ideally analogous to the DOI landing page citation;
        # can be handled via --doi CL option
        "citation": "__CITATION__",
        # Full ssh access name of the server hosting the GIN server instance
        "gin_server": "__GIN.SERVER__",
        # Full ssh access name of the server hosting the DOI server instance
        "doi_server": "__DOI.SERVER__",
        # User working on the DOI server
        "server_user": "__SERVER_USER__",
        # Full name of the person handling the registration; used in email template texts
        "admin_name": "__FIRST LAST__",
        # DOI Server repo preparation directory
        "dir_doi_prep": "__DIR_DOI_PREP__",
        # DOI Server root doi hosting directory
        "dir_doi": "__DIR_DOI__",
        # Local staging dir to create keyword pages
        "dir_local_stage": "__DIR_LOCAL_STAGE__"
}


def text_pre_fork():
    text_block = """

-[ ] manually fork repository to the 'doi' gin user
    - log on to gin.g-node.org using the "doi" user
    - fork https://gin.g-node.org/%s/%s""" % (CONF["repo_own"], CONF["repo"])

    return text_block


def text_pre_fork_upload():
    text_block = """

-[ ] log on to the DOI server (%s) and move to %s
-[ ] fetch git and annex content and upload annex content to the DOI fork repo
     use screen to avoid large down- and uploads to be interrupted
     use CTRL+a+d to switch out of screen sessions without interruption
    - screen -S %s-%s
    - sudo su root
    - ./syncannex %s/%s > %s-%s.log""" % (
        CONF["doi_server"], CONF["dir_doi_prep"], CONF["repo_own"].lower(), str(uuid4())[0:5],
        CONF["repo_own"], CONF["repo"], CONF["repo_own"].lower(), CONF["repo"])
    return text_block


def text_pre_git_tag():
    text_block = """

- create release tag on the DOI repository; run all commands using `gin git ...` 
  to avoid issues with local git annex or other logged git users.
    -[ ] cd %s/%s
    -[ ] sudo gin git status
    -[ ] sudo gin git remote -v
    -[ ] sudo gin git tag 10.12751/g-node.%s
    -[ ] sudo gin git push --tags origin""" % (CONF["dir_doi_prep"], CONF["repo"].lower(),
                                               CONF["reg_id"])
    return text_block


def text_pre_cleanup():
    text_block = """

- cleanup directory once tagging is done
    -[ ] sudo rm %s/%s -r
    -[ ] sudo mv %s/%s*.log /home/%s/logs/""" % (CONF["dir_doi_prep"], CONF["repo"].lower(),
                                                 CONF["dir_doi_prep"], CONF["repo_own"].lower(),
                                                 CONF["server_user"])
    return text_block


def print_part_pre_doi(fip):
    """
    Print pre-registration block to file

    :param fip: filepointer
    """
    text_block = """# Part 1 - pre registration

## Base request information
-[ ] check if the following information is correct; re-run script otherwise with updated config

    DOI request
    - Repository: %s/%s
    - User: (%s)
    - Email address: %s
    - DOI XML: %s:/data/doi/10.12751/g-node.%s/doi.xml
    - DOI target URL: https://doi.gin.g-node.org/10.12751/g-node.%s

    - Request Date (as in doi.xml): %s

""" % (CONF["repo_own"], CONF["repo"], CONF["user_full_name"], CONF["email"],
       CONF["doi_server"], CONF["reg_id"], CONF["reg_id"], CONF["reg_date"])
    fip.write(text_block.encode("utf-8"))

    fip.write("## Base pre-registration checks")

    text_block = """
-[ ] GIN server (%s) check annex content
    - cd /gindata
    - ./annexcheck /gindata/gin-repositories/%s""" % (CONF["gin_server"], CONF["repo_own"].lower())
    fip.write(text_block.encode("utf-8"))

    text_block = """

- check the datacite content at 
  https://gin.g-node.org/%s/%s
    -[ ] repo is eligible to be published on gin
    -[ ] resourceType e.g. Dataset fits the repository
    -[ ] title is useful and has no typos
    -[ ] license title, license content and license link match""" % (CONF["repo_own"], CONF["repo"])
    fip.write(text_block.encode("utf-8"))

    fip.write("\n")


def print_part_pre_doi_semi(fip):
    """
    Print semi automatic DOI pre-registration block to file

    :param fip: filepointer
    """
    text_block = """
## Semi-automated DOI
- use this section if there are no technical or other issues with the DOI request 
  and skip the 'Full DOI' section."""
    fip.write(text_block.encode("utf-8"))

    text_block = """

- on the DOI server (%s) check the DOI directory content
    -[ ] zip file created in /data/doi/10.12751/g-node.%s
    -[ ] note zip size

-[ ] remove /data/doi/10.12751/g-node.%s/.htaccess

- access https://doi.gin.g-node.org/10.12751/g-node.%s
    -[ ] check landing page in general
    -[ ] check title, license name
    -[ ] check all links that should work at this stage
    -[ ] check zip download and compare size on server with size in `doi.xml`""" % \
                 (CONF["doi_server"], CONF["reg_id"], CONF["reg_id"], CONF["reg_id"])
    fip.write(text_block.encode("utf-8"))

    text_block = text_pre_fork()
    fip.write(text_block.encode("utf-8"))

    text_block = text_pre_fork_upload()
    fip.write(text_block.encode("utf-8"))

    text_block = text_pre_git_tag()
    fip.write(text_block.encode("utf-8"))

    text_block = text_pre_cleanup()
    fip.write(text_block.encode("utf-8"))

    text_block = """

-[ ] email to TWachtler;
     use and forward the first registration request email from G-Node/DOIMetadata

To: gin@g-node.org

Hi Thomas,

the repository should be prepared for the DOI registration.

Best,
%s

""" % (CONF["admin_name"].split()[0])
    fip.write(text_block.encode("utf-8"))


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
    fip.write(text_block.encode("utf-8"))

    text_block = text_pre_fork()
    fip.write(text_block.encode("utf-8"))

    text_block = text_pre_fork_upload()
    fip.write(text_block.encode("utf-8"))

    text_block = """

-[ ] create DOI zip file
    - screen -S %s-%s
    - sudo su root
    - sudo ./makezip %s

-[ ] make sure there is no zip file in the target directory left 
     from the previous registration process.

-[ ] sudo mv %s.zip %s/10.12751/g-node.%s/10.12751_g-node.%s.zip""" % (
        CONF["repo_own"].lower(), str(uuid4())[0:5], CONF["repo"].lower(), CONF["repo"].lower(),
        CONF["dir_doi"], CONF["reg_id"], CONF["reg_id"])
    fip.write(text_block.encode("utf-8"))

    text_block = text_pre_git_tag()
    fip.write(text_block.encode("utf-8"))

    text_block = text_pre_cleanup()
    fip.write(text_block.encode("utf-8"))

    text_block = """

-[ ] edit %s/10.12751/g-node.%s/doi.xml file to reflect any changes in the repo datacite.yml file.
    - include the actual size of the zip file
    - check proper title and proper license
    - any added or updated funding or reference information
    - any changes to the 'resourceType'""" % (CONF["dir_doi"], CONF["reg_id"])
    fip.write(text_block.encode("utf-8"))

    text_block = """

- remove the .htaccess file
- create the DOI landing page in the local staging directory and move it to the DOI server
    -[ ] cd %s
    -[ ] gindoid make-html https://doi.gin.g-node.org/10.12751/g-node.%s/doi.xml
    -[ ] scp %s/10.12751/g-node.%s/index.html %s@%s:/home/%s/staging
    - move to the DOI server staging directory
    -[ ] sudo chown root:root index.html
    -[ ] sudo mv index.html %s/10.12751/g-node.%s/index.html""" % (
        CONF["dir_local_stage"], CONF["reg_id"], CONF["dir_local_stage"],
        CONF["reg_id"], CONF["server_user"], CONF["doi_server"],
        CONF["server_user"], CONF["dir_doi"], CONF["reg_id"])
    fip.write(text_block.encode("utf-8"))

    text_block = """

- https://doi.gin.g-node.org/10.12751/g-node.%s
    -[ ] check page access, size, title, license name
    -[ ] check all links that should work at this stage
    -[ ] check zip download and suggested size""" % CONF["reg_id"]
    fip.write(text_block.encode("utf-8"))

    text_block = """

-[ ] email TWachtler about the prepared DOI requests;
     use and forward the first registration request email from G-Node/DOIMetadata

To: gin@g-node.org

Hi Thomas,

the repository should be prepared for the DOI registration.

In the doi.xml the following changes were made and the index.html page has been updated accordingly:
- Title was updated.
- License name and link was updated.
- Zip size was added.

Best,
%s

""" % (CONF["admin_name"].split()[0])
    fip.write(text_block.encode("utf-8"))


def print_part_post_doi(fip):
    """
    Print post-registration block to file.

    :param fip: filepointer
    """
    text_block = """
# Part 2 - post registration
-[ ] connect to DOI server (%s) and update `%s/index.html`; 
     make sure there are no unintentional line breaks!
                        <tr>
                            <td><a href="https://doi.org/10.12751/g-node.%s">%s</a>
                            <br>%s</td>
                            <td>%s</td>
                            <td><a href="https://doi.org/10.12751/g-node.%s" class ="ui grey label">10.12751/g-node.%s</a></td>
                        </tr>""" % (CONF["doi_server"], CONF["dir_doi"], CONF["reg_id"],
                                    CONF["title"], CONF["citation"], CONF["reg_date"],
                                    CONF["reg_id"], CONF["reg_id"])
    fip.write(text_block.encode("utf-8"))

    text_block = """

-[ ] update `%s/urls.txt`: https://doi.gin.g-node.org/10.12751/g-node.%s

- re-create and deploy keywords if required
  -[ ] make sure github.com/G-Node/gin-doi is locally built and the `gindoid` executable available
  -[ ] gin get G-Node/DOImetadata to local staging directory
  -[ ] create empty "keywords" directory and run the following from it
  -[ ] %s/gindoid make-keyword-pages %s/DOImetadata/*.xml
  -[ ] scp -r %s/keywords %s@%s:/home/%s/staging""" % (
        CONF["dir_doi"], CONF["reg_id"], CONF["dir_local_stage"], CONF["dir_local_stage"],
        CONF["dir_local_stage"], CONF["server_user"], CONF["doi_server"], CONF["server_user"])
    fip.write(text_block.encode("utf-8"))

    text_block = """
  -[ ] connect to DOI server (%s)
  -[ ] sudo chown -R root:root /home/%s/staging/keywords
  -[ ] sudo mv %s/keywords %s/keywords_
  -[ ] sudo mv /home/%s/staging/keywords/ %s
  -[ ] check landing page and keywords online: https://doi.gin.g-node.org
  -[ ] sudo rm %s/keywords_ -r""" % (
        CONF["doi_server"], CONF["server_user"], CONF["dir_doi"], CONF["dir_doi"],
        CONF["server_user"], CONF["dir_doi"], CONF["dir_doi"])
    fip.write(text_block.encode("utf-8"))

    text_block = """

-[ ] ensure the data directory "%s" in %s/10.12751/g-node.%s/ has been removed

-[ ] git commit all changes in %s
    - sudo git add 10.12751/g-node.%s/
    - sudo git commit -m "New dataset: 10.12751/g-node.%s"

-[ ] commit keyword and index page changes
    - sudo git add keywords/
    - sudo git add index.html
    - sudo git add urls.txt
    - sudo git commit -m "Update index and keyword pages"

-[ ] set zip to immutable
    sudo chattr +i %s/10.12751/g-node.%s/10.12751_g-node.%s.zip

-[ ] cleanup any leftover directories from previous versions 
     of this dataset in the %s/10.12751/ directory

-[ ] email to user (check below)

-[ ] close all related issues on DOImetadata

    Publication finished and user informed.""" % (
        CONF["repo"].lower(), CONF["dir_doi"], CONF["reg_id"], CONF["dir_doi"], CONF["reg_id"],
        CONF["reg_id"], CONF["dir_doi"], CONF["reg_id"], CONF["reg_id"], CONF["dir_doi"])
    fip.write(text_block.encode("utf-8"))


def print_part_ready_email(fip):
    """
    Print DOI registration ready email block to file.

    :param fip: filepointer
    """
    text_block = """
# Part 3 - eMail to user
-[ ] make sure the publication reference text does apply, remove otherwise

%s

CC: gin@g-node.org

Subject: DOI registration complete - %s/%s

Dear %s,

Your dataset with title
  %s

has been successfully registered.

The DOI for the dataset is
  https://doi.org/10.12751/g-node.%s

It can be viewed at
  https://doi.gin.g-node.org/10.12751/g-node.%s

If this is data supplementing a publication and if you haven't done so already, we kindly request that you:
- include the new DOI of this dataset in the publication as a reference, and
- update the datacite file of the registered dataset to reference the publication, including its DOI, once it is known.

The latter will result in a link in the Datacite database to your publication and will increase its discoverability.

Best regards,
  %s
  German Neuroinformatics Node
""" % (CONF["email"], CONF["repo_own"], CONF["repo"], CONF["user_full_name"], CONF["title"],
       CONF["reg_id"], CONF["reg_id"], CONF["admin_name"])
    fip.write(text_block.encode("utf-8"))


def run():
    owner = CONF["repo_own"].lower()
    if len(CONF["repo_own"]) > 5:
        owner = owner[0:5]
    repo_name = CONF["repo"].lower()
    if len(CONF["repo"]) > 10:
        repo_name = repo_name[0:15]

    c_date = datetime.now().strftime("%Y%m%d")
    out_file = "%s_%s-%s-%s.md" % (c_date, CONF["reg_id"].lower(), owner, repo_name)
    print("-- Writing to file %s" % out_file)
    with open(out_file, "w") as fip:
        print_part_pre_doi(fip)
        print_part_pre_doi_semi(fip)
        print_part_pre_doi_full(fip)
        print_part_post_doi(fip)
        print_part_ready_email(fip)

    print("-- Finished writing file %s" % out_file)


def update_conf(conf):
    for val in conf:
        if val in CONF:
            CONF[val] = conf[val]
        else:
            print("-- WARN: ignoring unknown config field '%s'" % val)


def update_conf_from_file(conf_file):
    with open(conf_file, "r") as fip:
        conf = y_load(fip, Loader=SafeLoader)

    update_conf(conf)


def parse_doi_xml(xml_string):
    doi_conf = {}
    dsns = "{http://datacite.org/schema/kernel-4}"

    root = etree.fromstring(xml_string)
    # Handle title
    title = root.find("%stitles" % dsns).find("%stitle" % dsns).text
    if title:
        doi_conf["title"] = title

    # Handle date
    date = root.find("%sdates" % dsns).find("%sdate" % dsns).text
    if date:
        doi_conf["reg_date"] = date

    # Handle citation
    citation = ""
    creators = root.find("%screators" % dsns).findall("%screator" % dsns)
    for creator in creators:
        curr = creator.find("%screatorName" % dsns).text
        curr = curr.replace(",", "").split(" ")
        citation = "%s, %s %s" % (citation, curr[0], curr[-1][0])
    if citation:
        doi_conf["citation"] = citation

    return doi_conf


def parse_repo_datacite():
    """
    Tries to access the request repository datacite file and parse the 'title'
    and the 'citation' from the files authors list.
    If the file cannot be accessed or there are any issues the script continues
    since both title and citation are not essential for the checklist.

    :return: struct to update the main config
    """
    print("-- Loading datacite file for '%s/%s'" % (CONF["repo_own"], CONF["repo"]))
    datacite_url = "https://gin.g-node.org/%s/%s/raw/master/datacite.yml" % (
        CONF["repo_own"], CONF["repo"])
    res = requests.get(datacite_url)

    # Return with an error message but continue the script on an access error
    if res.status_code != 200:
        print("-- ERROR: Status code (%s); could not access datacite file.\n"
              "\tMake sure to fill in 'title' and 'citation' in the checklist." % res.status_code)
        return

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
            fin = " %s" % creator["firstname"][0] if "firstname" in creator else ""
            if lan or fin:
                cit.append("%s%s" % (lan, fin))
        doi_conf["citation"] = ", ".join(cit)

    return doi_conf


def parse_args(args):
    parser = docopt(__doc__, argv=args, version="0.1.0")
    if parser['--config']:
        conf_file = parser['--config']
        if not os.path.isfile(conf_file):
            print("-- ERROR: Cannot open config file '%s'" % conf_file)
            exit(-1)

        update_conf_from_file(conf_file)
    elif os.path.isfile("conf.yaml"):
        print("-- Using local 'conf.yaml' file")
        update_conf_from_file("conf.yaml")

    if parser['--doi']:
        print("-- Loading doi xml for 'g-node.%s'" % CONF["reg_id"])
        doi_url = "https://doi.gin.g-node.org/10.12751/g-node.%s/doi.xml" % CONF["reg_id"]
        res = requests.get(doi_url)
        if res.status_code != 200:
            print("-- ERROR: Status code (%s); could not access requested DOI; "
                  "make sure access is available." % res.status_code)
            exit(-1)

        doi_conf = parse_doi_xml(res.text.encode())
        update_conf(doi_conf)

    run()


if __name__ == "__main__":
    if sys.argv[1:]:
        parse_args(sys.argv[1:])
    else:
        if os.path.isfile("conf.yaml"):
            print("-- Using local 'conf.yaml' file")
            update_conf_from_file("conf.yaml")
        else:
            print("-- Using script default config")

        run()
