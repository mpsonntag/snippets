"""create_registration_script

create_registration_script prints a checklist for DOI registrations.

Usage: create_registration_script [--config CONFIG_FILE]

Options:
    --config CONFIG_FILE    yaml file
    -h --help               Show this screen.
    --version               Show version.
"""

import os
import sys

from docopt import docopt
from yaml import load as y_load
from yaml import SafeLoader


# -- Required fields

# Automated registration id from "10.12751/g-node.[id]"
REG_ID = "__ID__"
# Repository owner
REPO_OWN = "__OWN__"
# Repository name
REPO = "__REPO__"
# date issued from doi.xml; Format YYYY-MM-DD
REG_DATE = "__DATE__"

# DOI requestee email address
EMAIL = "__MAIL__"
# DOI requestee full name
USER_FULL_NAME = "__FULL__"
# DOI request title
TITLE = "__TITLE__"
# Author citation list; ideally analogous to the DOI landing page citation
CITATION = "__CITATION__"

# Full ssh access name of the server hosting the GIN server instance
GIN_SERVER = "__GIN.SERVER__"
# Full ssh access name of the server hosting the DOI server instance
DOI_SERVER = "__DOI.SERVER__"
# User working on the DOI server
SERVER_USER = "__SERVER_USER__"
# Full name of the person handling the registration; used in email template texts
ADMIN_NAME = "__FIRST LAST__"

# DOI Server repo preparation directory
DIR_DOI_PREP = "__DIR_DOI_PREP__"
# DOI Server root doi hosting directory
DIR_DOI = "__DIR_DOI__"
# Local staging directory to create keyword pages
DIR_LOCAL_STAGE = "__DIR_LOCAL_STAGE__"

# Default configuration struct containing non problematic test values
CONF = {
    "repo": {
        "reg_id": "__ID__",         # Automated registration id from "10.12751/g-node.[id]"
        "repo_own": "__OWN__",      # Repository owner
        "repo": "__REPO__",         # Repository name
        "reg_date": "__DATE__"      # Date issued from doi.xml; Format YYYY-MM-DD
    }, "request": {
        "email": "__MAIL__",                # DOI requestee email address
        "user_full_name": "__USER_FULL__",  # DOI requestee full name
        "title": "__TITLE__",               # DOI request title
        # Author citation list; ideally analogous to the DOI landing page citation
        "citation": "__CITATION__"
    }, "server": {
        # Full ssh access name of the server hosting the GIN server instance
        "gin_server": "__GIN.SERVER__",\
        # Full ssh access name of the server hosting the DOI server instance
        "doi_server": "__DOI.SERVER__",
        # User working on the DOI server
        "server_user": "__SERVER_USER__",
        # Full name of the person handling the registration; used in email template texts
        "admin_name": "__FIRST LAST__"
    }, "directories": {
        "dir_doi_prep": "__DIR_DOI_PREP__",         # DOI Server repo preparation directory
        "dir_doi": "__DIR_DOI__",                   # DOI Server root doi hosting directory
        "dir_local_stage": "__DIR_LOCAL_STAGE__",   # Local staging dir to create keyword pages
    }
}


def print_part_pre_doi(fip):
    """
    Print pre-registration block to file

    :param fip: filepointer
    """
    text_block = """
# Part 1 - pre registration

## Semi-automated DOI
-[ ] DOI request - paste from issue on https://gin.g-node.org/G-Node/DOIMetadata
    - Repository: %s/%s
    - User: (%s)
    - Email address: %s
    - DOI XML: %s:/data/doi/10.12751/g-node.%s/doi.xml
    - DOI target URL: https://doi.gin.g-node.org/10.12751/g-node.%s

    - Request Date from DOI XML: %s""" % (REPO_OWN, REPO, USER_FULL_NAME, EMAIL,
                                          DOI_SERVER, REG_ID, REG_ID, REG_DATE)
    fip.write(text_block)

    text_block = """

-[ ] GIN server (%s) check annex content
    - cd /gindata
    - ./annexcheck /gindata/gin-repositories/%s""" % (GIN_SERVER, REPO_OWN.lower())
    fip.write(text_block)

    text_block = """
- check the datacite content at https://gin.g-node.org/%s/%s
    -[ ] check if the repo is eligible to be published on gin
    -[ ] check if the resourceType e.g. Dataset fits the repository
    -[ ] title is useful and has no typos
    -[ ] license title, license content and license link match""" % (REPO_OWN, REPO)
    fip.write(text_block)

    text_block = """
- on the DOI server (%s) check the DOI directory content
    -[ ] zip file created in /data/doi/10.12751/g-node.%s
    -[ ] note zip size
-[ ] remove /data/doi/10.12751/g-node.%s/.htaccess
-[ ] access https://doi.gin.g-node.org/10.12751/g-node.%s
    -[ ] check landing page in general
    -[ ] check title, license name
    -[ ] check all links that should work at this stage
    -[ ] check zip download and compare size on server with size in `doi.xml`
-[ ] on gin.g-node.org, log in with "doi" user and fork https://gin.g-node.org/%s/%s""" % \
                 (DOI_SERVER, REG_ID, REG_ID, REG_ID, REPO_OWN, REPO)
    fip.write(text_block)

    text_block = """
-[ ] fetch content and upload to DOI repo
     use screen to avoid large down- and uploads to be interrupted
     use CTRL+a+d to switch out of screen sessions
    - cd %s/
    - screen -S %s
    - sudo su root
    - ./syncannex %s/%s > %s_%s.log""" % (DIR_DOI_PREP, REPO_OWN.lower(), REPO_OWN,
                                          REPO, REPO_OWN.lower(), REPO)
    fip.write(text_block)

    text_block = """
-[ ] tag release on the DOI repository; run all commands using `gin git ...` 
     to avoid issues with local git annex or differently logged in users.
    -[ ] cd %s/%s
    -[ ] sudo gin git status
    -[ ] sudo gin git remote -v
    -[ ] sudo gin git tag 10.12751/g-node.%s
    -[ ] sudo gin git push --tags origin""" % (DIR_DOI_PREP, REPO.lower(), REG_ID)
    fip.write(text_block)

    text_block = """
-[ ] cleanup directory once tagging is done
    -[ ] sudo rm %s/%s -r
    -[ ] sudo mv %s/%s*.log /home/%s/logs/""" % (DIR_DOI_PREP, REPO.lower(), DIR_DOI_PREP,
                                                 REPO_OWN.lower(), SERVER_USER)
    fip.write(text_block)

    text_block = """
-[ ] email to TWachtler;
     use and forward the first registration request email from G-Node/DOIMetadata

To: gin@g-node.org

Hi Thomas,

the repository should be prepared for the DOI registration.

Best,
%s

""" % (ADMIN_NAME.split()[0])
    fip.write(text_block)


def print_part_pre_doi_full(fip):
    """
    Print optional full DOI pre-registration block to file.

    :param fip: filepointer
    """
    text_block = """
## Full DOI
-[ ] check that the annex content is fully available on the gin server (%s)
    - cd /gindata
    - ./annexcheck /gindata/gin-repositories/%s
-[ ] check the datacite content at https://gin.g-node.org/%s/%s
    - title is useful and has no typos
    - license title, license content and license link match
-[ ] log onto https://gin.g-node.org using the "doi" user (check G-Node vault for pw)""" % \
                 (GIN_SERVER, REPO_OWN, REPO_OWN, REPO)
    fip.write(text_block)

    text_block = """
-[ ] manually fork https://gin.g-node.org/%s/%s to DOI user
-[ ] log on to the DOI server (%s) and move to %s
-[ ] fetch content and upload to DOI repo
     use screen to avoid large down- and uploads to be interrupted
     use CTRL+a+d to switch out of screen sessions
    - screen -S %s
    - sudo su root
    - ./syncannex %s/%s > %s-%s.log""" % (REPO_OWN, REPO, DOI_SERVER, DIR_DOI_PREP,
                                          REPO_OWN.lower(), REPO_OWN, REPO, REPO_OWN.lower(), REPO)
    fip.write(text_block)

    text_block = """
-[ ] create DOI zip file
    - screen -S %s
    - sudo su root
    - sudo ./makezip %s
-[ ] sudo mv %s.zip %s/10.12751/g-node.%s/10.12751_g-node.%s.zip""" % \
                 (REPO_OWN.lower(), REPO.lower(), REPO.lower(), DIR_DOI, REG_ID, REG_ID)
    fip.write(text_block)

    text_block = """
-[ ] create a tag release on the DOI repository; run all commands using `gin git ...` 
     to avoid issues with local git annex or differently logged in gin/git users.
    -[ ] cd %s/%s
    -[ ] sudo gin git status
    -[ ] sudo gin git remote -v
    -[ ] sudo gin git tag 10.12751/g-node.%s
    -[ ] sudo gin git push --tags origin
-[ ] clean up directory once tagging is done
    -[ ] sudo rm %s/%s -r
    -[ ] sudo mv %s/%s*.log /home/%s/logs/""" % (DIR_DOI_PREP, REPO.lower(), REG_ID, DIR_DOI_PREP,
                                                 REPO.lower(), DIR_DOI_PREP, REPO_OWN, SERVER_USER)
    fip.write(text_block)

    text_block = """
-[ ] edit %s/10.12751/g-node.%s/doi.xml file 
     to include the actual size, the proper title and the proper license
- move to local, create index.html from published doi.xml""" % (DIR_DOI, REG_ID)
    fip.write(text_block)

    text_block = """
-[ ] Create the DOI landing page in the local staging directory and move it to the DOI server
    gindoid make-html https://doi.gin.g-node.org/10.12751/g-node.%s/doi.xml
    scp index.html %s@%s:/home/%s/staging
    sudo mv index.html %s/10.12751/g-node.%s/index.html
    sudo chown root:root %s
    sudo chmod ugo+rX -R %s""" % (REG_ID, SERVER_USER, DOI_SERVER, SERVER_USER,
                                  DIR_DOI, REG_ID, DIR_DOI, DIR_DOI)
    fip.write(text_block)

    text_block = """
- https://doi.gin.g-node.org/10.12751/g-node.%s
    -[ ] check page access, size, title, license name
    -[ ] check all links that should work at this stage
    -[ ] check zip download and suggested size""" % REG_ID
    fip.write(text_block)

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

""" % (ADMIN_NAME.split()[0])
    fip.write(text_block)


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
                        </tr>""" % (DOI_SERVER, DIR_DOI, REG_ID, TITLE, CITATION,
                                    REG_DATE, REG_ID, REG_ID)
    fip.write(text_block)

    text_block = """
-[ ] update `%s/urls.txt`: https://doi.gin.g-node.org/10.12751/g-node.%s
-[ ] make sure github.com/G-Node/gin-doi is locally built and the `gindoid` executable available
-[ ] gin get G-Node/DOImetadata to local staging directory
-[ ] create empty "keywords" directory and run the following from it
-[ ] %s/gindoid make-keyword-pages %s/DOImetadata/*.xml
-[ ] scp -r %s/keywords %s@%s:/home/%s/staging""" % (DIR_DOI, REG_ID, DIR_LOCAL_STAGE,
                                                     DIR_LOCAL_STAGE, DIR_LOCAL_STAGE,
                                                     SERVER_USER, DOI_SERVER, SERVER_USER)
    fip.write(text_block)

    text_block = """
-[ ] connect to DOI server (%s)
-[ ] sudo chown -R root:root /home/%s/staging/keywords
-[ ] sudo mv %s/keywords %s/keywords_
-[ ] sudo mv /home/%s/staging/keywords/ %s
-[ ] check landing page and keywords online: https://doi.gin.g-node.org
-[ ] sudo rm %s/keywords_ -r""" % (DOI_SERVER, SERVER_USER, DIR_DOI,
                                   DIR_DOI, SERVER_USER, DIR_DOI, DIR_DOI)
    fip.write(text_block)

    text_block = """
-[ ] ensure the data directory "%s" in %s/10.12751/g-node.%s/ has been removed
-[ ] git commit all changes in %s
    sudo git add 10.12751/g-node.%s/
    sudo git commit -m "New dataset: 10.12751/g-node.%s"
-[ ] commit keyword and index page changes
    sudo git add keywords/
    sudo git add index.html
    sudo git add urls.txt
    sudo git commit -m "Update index and keyword pages"
-[ ] set zip to immutable
    sudo chattr +i %s/10.12751/g-node.%s/10.12751_g-node.%s.zip
-[ ] cleanup any leftover directories from previous versions 
     of this dataset in the %s/10.12751/ directory
-[ ] email to user (check below)
-[ ] close all related issues on DOImetadata

    Publication finished and user informed.""" % (REPO.lower(), DIR_DOI, REG_ID, DIR_DOI, REG_ID,
                                                  REG_ID, DIR_DOI, REG_ID, REG_ID, DIR_DOI)
    fip.write(text_block)


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
""" % (EMAIL, REPO_OWN, REPO, USER_FULL_NAME, TITLE, REG_ID, REG_ID, ADMIN_NAME)
    fip.write(text_block)


def run():
    owner = REPO_OWN.lower()
    if len(REPO_OWN) > 5:
        owner = owner[0:5]
    repo_name = REPO.lower()
    if len(REPO) > 10:
        repo_name = repo_name[0:10]

    out_file = "%s_%s_%s.md" % (REG_ID.lower(), owner, repo_name)
    print("-- Writing to file %s" % out_file)
    with open(out_file, "w") as fip:
        print_part_pre_doi(fip)
        print_part_pre_doi_full(fip)
        print_part_post_doi(fip)
        print_part_ready_email(fip)

    print("-- Finished writing file %s" % out_file)


def update_conf(conf_file):
    with open(conf_file, "r") as fip:
        conf = y_load(fip, Loader=SafeLoader)

    for category in conf:
        if category in CONF:
            for val in conf[category]:
                if val in CONF[category]:
                    CONF[category][val] = conf[category][val]
                else:
                    print("-- Warning: ignoring unknown config field '%s/%s'" % (category, val))
        else:
            print("-- Warning: ignoring unknown config category '%s'" % category)


def parse_args(args):
    parser = docopt(__doc__, argv=args, version="0.1.0")
    if parser['--config']:
        conf_file = parser['--config']
        if not os.path.isfile(conf_file):
            print("-- Error: Cannot open config file '%s'" % conf_file)
            exit(-1)

        update_conf(conf_file)

    run()


if __name__ == "__main__":
    if sys.argv[1:]:
        parse_args(sys.argv[1:])
    else:
        if os.path.isfile("conf.yaml"):
            print("-- Using local 'conf.yaml' file")
            update_conf("conf.yaml")
        else:
            print("-- Using script default config")

        run()