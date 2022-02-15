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
        # Full ssh access name of the server hosting the DOI server instance
        "doi_server": "__DOI_SERVER__",
        # DOI Server repo preparation directory
        "dir_doi_prep": "__DIR_DOI_PREP__",
        # DOI Server root doi hosting directory
        "dir_doi": "__DIR_DOI__"
}


# Mapping of configuration entries to template replacement strings
CONF_MAP = {
    "reg_id": "{{ .CL.Regid }}",
    "repo_own": "{{ .CL.Repoown }}",
    "repo": "{{ .CL.Repo }}",
    "reg_date": "{{ .CL.Regdate }}",
    "email": "{{ .CL.Email }}",
    "user_full_name": "{{ .CL.Userfullname }}",
    "title": "{{ .CL.Title }}",
    "citation": "{{ .CL.Citation }}",
    "doi_server": "{{ .CL.Doiserver }}",
    "dir_doi_prep": "{{ .CL.Dirdoiprep }}",
    "dir_doi": "{{ .CL.Dirdoi }}",
    "repo_lower": "{{ .RepoLower }}",
    "repo_own_lower": "{{ .RepoownLower }}",
    "semi_doi_screen_id": "{{ .SemiDOIScreenID }}",
    "full_doi_screen_id": "{{ .FullDOIScreenID }}",
    "semi_doi_cleanup": "{{ .SemiDOICleanup }}",
    "semi_doi_dir_path": "{{ .SemiDOIDirpath }}",
    "full_doi_dir_path": "{{ .FullDOIDirpath }}",
    "forklog": "{{ .Forklog }}",
    "logfiles": "{{ .Logfiles }}",
    "ziplog": "{{ .Ziplog }}",
    "zipfile": "{{ .Zipfile }}",
    "cite_year": "{{ .Citeyear }}",
}


# Output template; the main template is used in a golang project and will
# remain there. The Python script uses the same template to create a checklist
# on the command line.
# When relevant and persistent changes are made to this template it should be posted
# as an issue on the go source repository: https://github.com/G-Node/gin-doi
TEMPLATE = """
# Part 1 - pre registration

## Base request information
-[ ] check if the following information is correct; re-run script otherwise with updated config

    DOI request
    - Repository: {{ .CL.Repoown }}/{{ .CL.Repo }}
    - User: ({{ .CL.Userfullname }})
    - Email address: {{ .CL.Email }}
    - DOI XML: {{ .CL.Doiserver }}:/data/doi/10.12751/g-node.{{ .CL.Regid }}/doi.xml
    - DOI target URL: https://doi.gin.g-node.org/10.12751/g-node.{{ .CL.Regid }}

    - Request Date (as in doi.xml): {{ .CL.Regdate }}

## Base pre-registration checks

- check the datacite content at 
  https://gin.g-node.org/{{ .CL.Repoown }}/{{ .CL.Repo }}
    -[ ] repo is eligible to be published via GIN DOI
    -[ ] the repo name is sufficiently unique to avoid clashes when 
         forking to the DOI GIN user.
    -[ ] resourceType e.g. Dataset fits the repository
    -[ ] license in datacite.yml and LICENSE file match
    -[ ] author list includes requester, otherwise ask requester for confirmation
    -[ ] ORCIDs look reasonable / are valid
    -[ ] title is useful and has no typos
    -[ ] keywords have no typos
    -[ ] automated issues are all addressed

- on the GIN server check annex content
    -[ ] /gindata/annexcheck /gindata/gin-repositories/{{ .RepoownLower }}/{{ .RepoLower }}.git

- on the DOI server ({{ .CL.Doiserver }}) make sure all information has been properly downloaded 
  to the staging directory and all annex files are unlocked and the content is present:
    -[ ] {{ .CL.Dirdoiprep }}/annexcheck {{ .SemiDOIDirpath }}
    - identify "normal" git annex issues e.g. locked or missing annex content
    -[ ] cd {{ .SemiDOICleanup }}/{{ .RepoLower }}
    -[ ] gin git annex find --locked
    -[ ] gin git annex find --not --in=here
    -[ ] find {{ .SemiDOICleanup }} -type l -print
    -[ ] find {{ .SemiDOICleanup }} -type f -size -100c -print0 | xargs -0 grep -i annex.objects
    -[ ] grep annex.objects $(find {{ .SemiDOICleanup }} -type f -size -100c -print)
    -[ ] check that the content size of the repository and the created zip file matches
    -[ ] if there still are symlinks present or the content size does not match up, the zip
         file does not contain all required data. Run the next steps - the script will
         download all missing information and upload to the DOI fork. When recreating the
         zip file, all files will be manually unlocked first.
    - approximate the required zip size via the git annex file size and the repository size
    -[ ] gin git annex info --fast .
    -[ ] du -chL --exclude=.git* .
    -[ ] ls -lahrt  {{ .CL.Dirdoi }}/10.12751/g-node.{{ .CL.Regid }}/
    - check the DOI directory content
      -[ ] zip file created in {{ .CL.Dirdoi }}/10.12751/g-node.{{ .CL.Regid }}
      -[ ] check zip file content
           unzip -vl {{ .CL.Dirdoi }}/10.12751/g-node.{{ .CL.Regid }}/10.12751_g-node.{{ .CL.Regid }}.zip
      -[ ] note zip size
    - check potential dataset zip files for issues
      find {{ .SemiDOICleanup }} -name "*.zip" -ls -exec unzip -P "" -t {} \; > $HOME/logs/zipcheck_{{ .CL.Regid }}.log
      echo "Valid zips: $(cat $HOME/logs/zipcheck_{{ .CL.Regid }}.log | grep "No errors detected" | wc -l)/$(find . -name "*.zip" | wc -l)"
    - if the number of valid zips does not match the number of total zips, check the logfile for details

## Semi-automated DOI or DOI update
- use this section if there are no technical or other issues with the DOI request 
  and skip the 'Full DOI' section.
- also use this section if there were no issues and an update to an existing DOI has
  been requested. The 'doiforkupload' script does both initial upload and update.

-[ ] remove {{ .CL.Dirdoi }}/10.12751/g-node.{{ .CL.Regid }}/.htaccess

- access https://doi.gin.g-node.org/10.12751/g-node.{{ .CL.Regid }}
    -[ ] check landing page in general
    -[ ] check title, license name
    -[ ] check all links that should work at this stage
    -[ ] check zip download and compare size on server with size in 'doi.xml'

-[ ] manually fork repository to the 'doi' gin user
    - log on to gin.g-node.org using the "doi" user
    - fork https://gin.g-node.org/{{ .CL.Repoown }}/{{ .CL.Repo }}

-[ ] log on to the DOI server ({{ .CL.Doiserver }}) and move to {{ .CL.Dirdoiprep }}
-[ ] fetch git and annex content and upload annex content to the DOI fork repo.
     use screen to avoid large down- and uploads to be interrupted.
     use CTRL+a+d to switch out of screen sessions without interruption.
     use either the logfile or 'htop' to check on the status of the download/upload.
    - screen -S {{ .SemiDOIScreenID }}
    - sudo su root
    - ./doiforkupload {{ .SemiDOIDirpath }} > {{ .Forklog }}
-[ ] after detaching from the session, check the log file until the upload starts to avoid
     any security check issues.
     Also read the commit hash comparison line to check if the content of the repo has
     been changed after the DOI request has been submitted.
     tail -f {{ .Forklog }}
-[ ] if a) the logfile contains the line "repo was not at the DOI request state" the
     repository was changed after the DOI request and the uploaded archive content will
     most likely differ from the zip file content. If b) the 'tree' command showed symlinks or 
     missing content, the zip file will also not contain the file content for all files.
       In this case use the 'makezip' bash script to recreate the zip file and 
     copy it to the the DOI hosting folder.
-[ ] once the upload is done, check that the git tag has been created on the DOI fork repository at
     https://gin.g-node.org/doi/{{ .CL.Repo }}.

- cleanup directory once tagging is done
    -[ ] sudo rm {{ .SemiDOICleanup }} -r
    -[ ] sudo mv {{ .CL.Dirdoiprep }}/{{ .Logfiles }} $HOME/logs/
    -[ ] cleanup screen session: screen -XS {{ .SemiDOIScreenID }} quit

-[ ] Check link to archive repo on the DOI landing page works:
    https://doi.gin.g-node.org/10.12751/g-node.{{ .CL.Regid }}

-[ ] issue comment on https://gin.g-node.org/G-Node/DOImetadata/issues
     New publication request: {{ .RepoownLower }}/{{ .RepoLower }} (10.12751/g-node.{{ .CL.Regid }})

     This repository is prepared for the DOI registration.

## Full DOI
- This usually has to be done when
  a) the semi-automated process has failed or
  b) the user requested changes but needs to keep the originally issued DOI

-[ ] manually fork repository to the 'doi' gin user
    - log on to gin.g-node.org using the "doi" user
    - fork https://gin.g-node.org/{{ .CL.Repoown }}/{{ .CL.Repo }}

-[ ] log on to the DOI server ({{ .CL.Doiserver }}) and move to {{ .CL.Dirdoiprep }}
-[ ] fetch git and annex content and upload annex content to the DOI fork repo.
     use screen to avoid large down- and uploads to be interrupted.
     use CTRL+a+d to switch out of screen sessions without interruption.
     use either the logfile or 'htop' to check on the status of the download/upload.
    - screen -S {{ .FullDOIScreenID }}
    - sudo su root
    - ./syncannex {{ .CL.Repoown }}/{{ .CL.Repo }} > {{ .Forklog }}

-[ ] check downloaded data; if any of the checks fail, the DOI fork has to be deleted and the 
     process repeated after the issue has been addressed
    -[ ] {{ .CL.Dirdoiprep }}/annexcheck {{ .CL.Dirdoiprep }}/{{ .CL.Repo }}
    - identify "normal" git annex issues e.g. locked or missing annex content
    -[ ] cd {{ .CL.Dirdoiprep }}/{{ .CL.Repo }}
    -[ ] gin git annex find --locked
    -[ ] gin git annex find --not --in=here
    -[ ] find {{ .CL.Dirdoiprep }}/{{ .CL.Repo }} -type l -print
    -[ ] find {{ .CL.Dirdoiprep }}/{{ .CL.Repo }} -type f -size -100c -print0 | xargs -0 grep -i annex.objects
    -[ ] grep annex.objects $(find {{ .CL.Dirdoiprep }}/{{ .CL.Repo }} -type f -size -100c -print)
    - check potential dataset zip files for issues
      find {{ .CL.Dirdoiprep }}/{{ .CL.Repo }} -name "*.zip" -ls -exec unzip -P "" -t {} \; > $HOME/logs/zipcheck_{{ .CL.Regid }}.log
      echo "Valid zips: $(cat $HOME/logs/zipcheck_{{ .CL.Regid }}.log | grep "No errors detected" | wc -l)/$(find . -name "*.zip" | wc -l)"
    - if the number of valid zips does not match the number of total zips, check the logfile for details

-[ ] create DOI zip file
    - screen -r {{ .FullDOIScreenID }}
    - sudo ./makezip {{ .RepoLower }} > {{ .Ziplog }}

- approximate the required zip size via the git annex file size and the repository size and compare to the created zip size
    -[ ] cd {{ .CL.Dirdoiprep }}/{{ .CL.Repo }}
    -[ ] gin git annex info --fast .
    -[ ] du -chL --exclude=.git* .
    -[ ] ls -lahrt {{ .CL.Dirdoiprep }}/{{ .CL.Repo }}/*.zip

-[ ] make sure there is no zip file in the target directory left 
     from the previous registration process.

-[ ] sudo mv {{ .RepoLower }}.zip {{ .Zipfile }}

- create release tag on the DOI repository; run all commands using 'gin git ...' 
  to avoid issues with local git annex or other logged git users.
    -[ ] cd {{ .CL.Dirdoiprep }}/{{ .RepoLower }}
    -[ ] check that "doi" is the set origin: sudo gin git remote -v
    -[ ] sudo gin git tag 10.12751/g-node.{{ .CL.Regid }}
    -[ ] sudo gin git push --tags origin

- cleanup directory once tagging is done
    -[ ] sudo rm {{ .FullDOIDirpath }} -r
    -[ ] sudo mv {{ .CL.Dirdoiprep }}/{{ .Logfiles }} $HOME/logs/
    -[ ] cleanup screen session: screen -XS {{ .FullDOIScreenID }} quit

-[ ] edit {{ .CL.Dirdoi }}/10.12751/g-node.{{ .CL.Regid }}/doi.xml file to reflect
     any changes in the repo datacite.yml file.
    - include the actual size of the zip file
    - check proper title and proper license
    - any added or updated funding or reference information
    - any changes to the 'resourceType'

- remove the .htaccess file
- re-create the DOI landing page in the server staging directory
    -[ ] cd $HOME/staging
    -[ ] sudo {{ .CL.Dirdoiprep }}/gindoid make-html https://doi.gin.g-node.org/10.12751/g-node.{{ .CL.Regid }}/doi.xml
    -[ ] sudo mv index.html {{ .CL.Dirdoi }}/10.12751/g-node.{{ .CL.Regid }}/index.html

- https://doi.gin.g-node.org/10.12751/g-node.{{ .CL.Regid }}
    -[ ] check page access, size, title, license name
    -[ ] check all links that should work at this stage
    -[ ] check zip download and suggested size

-[ ] issue comment on https://gin.g-node.org/G-Node/DOImetadata/issues
     New publication request: {{ .RepoownLower }}/{{ .RepoLower }} (10.12751/g-node.{{ .CL.Regid }})

     This repository is prepared for the DOI registration.

# Part 2 - post registration
-[ ] connect to DOI server ({{ .CL.Doiserver }})
- update the G-Node/DOImetadata repository
  cd {{ .CL.Dirdoiprep }}/DOImetadata
  sudo gin download
- update site listing page, google sitemap and keywords
  -[ ] create a clean server staging directory
    sudo mkdir -p $HOME/staging/g-node.{{ .CL.Regid }}
    cd $HOME/staging/g-node.{{ .CL.Regid }}
  -[ ] create all required files
    -[ ] sudo {{ .CL.Dirdoiprep }}/gindoid make-all {{ .CL.Dirdoiprep }}/DOImetadata/*.xml
    -[ ] check index.html and urls.txt file
    -[ ] sudo mv {{ .CL.Dirdoi }}/keywords {{ .CL.Dirdoi }}/keywords_
    -[ ] sudo mv $HOME/staging/g-node.{{ .CL.Regid }}/keywords/ {{ .CL.Dirdoi }}
    -[ ] sudo mv $HOME/staging/g-node.{{ .CL.Regid }}/index.html {{ .CL.Dirdoi }}
    -[ ] sudo mv $HOME/staging/g-node.{{ .CL.Regid }}/urls.txt {{ .CL.Dirdoi }}
  -[ ] check landing page and keywords online: https://doi.gin.g-node.org
  -[ ] cleanup previous keywords
    sudo rm {{ .CL.Dirdoi }}/keywords_ -r
  -[ ] cleanup the staging directory
    cd $HOME/staging
    sudo rm g-node.{{ .CL.Regid }} -r

-[ ] git commit all changes in {{ .CL.Dirdoi }}
    - sudo git add 10.12751/g-node.{{ .CL.Regid }}/
    - sudo git commit -m "New dataset: 10.12751/g-node.{{ .CL.Regid }}"

-[ ] commit keyword and index page changes
    - sudo git add keywords/
    - sudo git add index.html
    - sudo git add urls.txt
    - sudo git commit -m "Update index and keyword pages"

-[ ] set zip to immutable
    sudo chattr +i {{ .CL.Dirdoi }}/10.12751/g-node.{{ .CL.Regid }}/10.12751_g-node.{{ .CL.Regid }}.zip

-[ ] cleanup any leftover directories from previous versions 
     of this dataset in the {{ .CL.Dirdoi }}/10.12751/ and 
    {{ .CL.Dirdoiprep }}/10.12751/ directories.

-[ ] email to user (check below)

-[ ] close all related issues on https://gin.g-node.org/G-Node/DOImetadata/issues
     New publication request: {{ .RepoownLower }}/{{ .RepoLower }} (10.12751/g-node.{{ .CL.Regid }})

     Publication finished and user informed.

# Part 3 - eMail to user
-[ ] make sure the publication reference text does apply, remove otherwise

{{ .CL.Email }}

CC: gin@g-node.org

Subject: DOI registration complete - {{ .CL.Repoown }}/{{ .CL.Repo }}

Dear {{ .CL.Userfullname }},

Your dataset with title
  {{ .CL.Title }}

has been successfully registered.

The DOI for the dataset is
  https://doi.org/10.12751/g-node.{{ .CL.Regid }}

Please always reference the dataset by its DOI (not the link to the repository) and cite the dataset as
  {{ .CL.Citation }} ({{ .Citeyear }}) {{ .CL.Title }}. G-Node. https://doi.org/10.12751/g-node.{{ .CL.Regid }}

If this is data supplementing a publication and if you haven't done so already, we kindly request that you:
- include the new DOI of this dataset in the publication as a reference, and
- update the datacite file of the registered dataset to reference the publication, including its DOI, once it is known.

The latter will result in a link in the Datacite database to your publication and will increase its discoverability.

Best regards,

  German Neuroinformatics Node
"""


def conf_derivatives():
    lrepo = CONF["repo"].lower()
    lrepoown = CONF["repo_own"].lower()
    doiprep = CONF["dir_doi_prep"]
    reg_dir = f"10.12751/g-node.{CONF['reg_id']}"

    CONF["repo_lower"] = lrepo
    CONF["repo_own_lower"] = lrepoown
    CONF["semi_doi_screen_id"] = f"{lrepoown}-{str(uuid4())[0:5]}"
    CONF["full_doi_screen_id"] = f"{lrepoown}-{str(uuid4())[0:5]}"
    CONF["semi_doi_cleanup"] = f"{doiprep}/{reg_dir}"
    CONF["semi_doi_dir_path"] = f"{doiprep}/{reg_dir}/{lrepo}"
    CONF["full_doi_dir_path"] = f"{doiprep}/{lrepo}"
    CONF["forklog"] = f"{lrepoown}-{lrepo}.log"
    CONF["logfiles"] = f"{lrepoown}-{lrepo}*.log"
    CONF["ziplog"] = f"{lrepoown}-{lrepo}_zip.log"
    CONF["zipfile"] = f"{CONF['dir_doi']}/{reg_dir}/10.12751_g-node.{CONF['reg_id']}.zip"
    CONF["cite_year"] = datetime.now().strftime("%Y")


def print_checklist(fip):
    """
    Replaces all TEMPLATE variables with CONF values and writes
    the resulting text block to a provided file.

    :param fip: file pointer to a write-ready file.
    """
    text_block = TEMPLATE

    # replace template entries
    for map_key, map_val in CONF_MAP.items():
        text_block = text_block.replace(map_val, CONF[map_key])

    fip.write(text_block)


def run():
    # create derivative config entries
    conf_derivatives()

    # prepare output filename
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
        print_checklist(fip)

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
    parser = docopt(__doc__, argv=args, version="0.2.0")
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
