# -- Required fields

# Automated registration id from "10.12751/g-node.[id]"
REG_ID = "__ID__"
# Repository owner
REPO_OWN = "__OWN__"
# Repository name
REPO = "__REPO__"
# Format YYYY-MM-DD
REG_DATE = "__DATE__"

# DOI requestee email address
EMAIL = "__MAIL__"
# DOI requestee full name
USER_FULL_NAME = "__FULL__"
# DOI request title
TITLE = "__TITLE__"
# Author citation list; ideally analogous to the DOI landing page citation
CITATION = "__CITATION__"

# Full ssh access name of the server hosting the DOI server instance
DOI_SERVER = "__DOI.SERVER__"
# User working on the DOI server
SERVER_USER = "__SERVER_USER__"
# Full name of the person handling the registration; used in email template text
ADMIN_NAME = "__FIRST LAST__"


def print_part_pre_doi(fp):
    """
    Print pre-registration block to file

    :param fp: filepointer
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

    - Request Date from DOI XML: %s
    """ % (REPO_OWN, REPO, USER_FULL_NAME, EMAIL, DOI_SERVER, REG_ID, REG_ID, REG_DATE)
    fp.write(text_block)

    text_block = """

-[ ] gin server check annex content
    - cd /gindata
    - ./annexcheck /gindata/gin-repositories/%s
    """ % REPO_OWN.lower()
    fp.write(text_block)

    text_block = """
-[ ] check the datacite content at https://gin.g-node.org/%s/%s
    - check if the repo is eligible to be published on gin
    - title is useful and has no typos
    - license title, license content and license link match
    """ % (REPO_OWN, REPO)
    fp.write(text_block)

    text_block = """
-[ ] check DOI directory content
    -[ ] /data/doi/10.12751/g-node.%s
-[ ] remove `.htaccess`, check landing page and zip download
-[ ] access https://doi.gin.g-node.org/10.12751/g-node.%s
    -[ ] check title, license name
    -[ ] check all links
    -[ ] check zip download and suggested size
-[ ] on gin.g-node.org, log in with "doi" user and fork https://gin.g-node.org/%s/%s
    """ % (REG_ID, REG_ID, REPO_OWN, REPO)
    fp.write(text_block)

    text_block = """
-[ ] fetch content and upload to DOI repo
    - cd /data/doiprep/
    - screen -S %s
    - sudo su root
    - ./syncannex %s/%s > %s_%s.log
    """ % (REPO_OWN.lower(), REPO_OWN, REPO, REPO_OWN.lower(), REPO)
    fp.write(text_block)

    text_block = """
-[ ] tag release on the DOI repository; run all commands using `gin git ...` 
     to avoid issues with local git annex or differently logged in users.
    -[ ] cd /data/doiprep/%s
    -[ ] sudo gin git status
    -[ ] sudo gin git remote -v
    -[ ] sudo gin git tag 10.12751/g-node.%s
    -[ ] sudo gin git push --tags origin
    """ % (REPO.lower(), REG_ID)
    fp.write(text_block)

    text_block = """
-[ ] cleanup directory once tagging is done
    -[ ] sudo rm /data/doiprep/%s -r
    -[ ] sudo mv /data/doiprep/%s*.log /home/%s/logs/
    """ % (REPO.lower(), REPO_OWN, SERVER_USER)
    fp.write(text_block)

    text_block = """
-[ ] email to TWachtler

Hi Thomas,

the repository should be prepared for the DOI registration.

Best,
%s
    """ % (ADMIN_NAME.split()[0])
    fp.write(text_block)


def print_part_pre_doi_full(fp):
    text_block = """
## Full DOI
-[ ] check that the annex content is fully available on the gin server (srv5)
    - cd /gindata
    - ./annexcheck /gindata/gin-repositories/%s
-[ ] check the datacite content at https://gin.g-node.org/%s/%s
    - title is useful and has no typos
    - license title, license content and license link match
-[ ] log onto https://gin.g-node.org using the "doi" user (check G-Node vault for pw)
    """ % (REPO_OWN, REPO_OWN, REPO)
    fp.write(text_block)

    text_block = """
-[ ] manually fork https://gin.g-node.org/%s/%s to DOI user
-[ ] log on to the doi server (srv6) and move to /data/doiprep
-[ ] fetch content and upload annex data to the DOI repo on gin
    - screen -S %s
    - sudo su root
    - ./syncannex %s/%s > %s-%s.log
    """ % (REPO_OWN, REPO, REPO_OWN.lower(), REPO_OWN, REPO, REPO_OWN.lower(), REPO)
    fp.write(text_block)

    text_block = """
-[ ] create DOI zip file
    - screen -S %s
    - sudo su root
    - sudo ./makezip %s
-[ ] sudo mv %s.zip /data/doi/10.12751/g-node.%s/10.12751_g-node.%s.zip
    """ % (REPO_OWN.lower(), REPO.lower(), REPO.lower(), REG_ID, REG_ID)
    fp.write(text_block)

    text_block = """
-[ ] create a tag release on the DOI repository; run all commands using `gin git ...` 
     to avoid issues with local git annex or differently logged in gin/git users.
    -[ ] cd /data/doiprep/%s
    -[ ] sudo gin git status
    -[ ] sudo gin git remote -v
    -[ ] sudo gin git tag 10.12751/g-node.%s
    -[ ] sudo gin git push --tags origin
-[ ] clean up directory once tagging is done
    -[ ] sudo rm /data/doiprep/%s -r
    -[ ] sudo mv /data/doiprep/%s*.log /home/%s/logs/
    """ % (REPO.lower(), REG_ID, REPO.lower(), REPO_OWN, SERVER_USER)
    fp.write(text_block)

    text_block = """
-[ ] edit /data/doi/10.12751/g-node.%s/doi.xml file 
     to include the actual size, the proper title and the proper license
- move to local, create index.html from published doi.xml
-[ ] Create the DOI landing page in the local staging directory and move it to the doi server
    gindoid make-html https://doi.gin.g-node.org/10.12751/g-node.%s/doi.xml
    scp index.html %s@%s:/home/%s/staging
    sudo mv index.html /data/doi/10.12751/g-node.%s/index.html
    sudo chown root:root /data/doi
    sudo chmod ugo+rX -R /data/doi
    """ % (REG_ID, REG_ID, SERVER_USER, DOI_SERVER, SERVER_USER, REG_ID)
    fp.write(text_block)

    text_block = """
- https://doi.gin.g-node.org/10.12751/g-node.%s
    -[ ] check page access, size, title, license name
    -[ ] check all links
    -[ ] check zip download and suggested size
    """ % REG_ID
    fp.write(text_block)

    text_block = """
-[ ] email TWachtler about the prepared DOI requests; use and forward the first registration request email

To: gin@g-node.org

Hi Thomas,

the repository should be prepared for the DOI registration.

In the doi.xml the following changes were made and the index.html page has been updated accordingly:
- Title was updated.
- License name and link was updated.
- Zip size was added.

Best,
Michael
    """
    fp.write(text_block)

    text_block = """
    
    """
    fp.write(text_block)


def print_part_post_doi(fp):
    text_block = """
# Part 2 - post registration
-[ ] connect to doi server (srv6) and update `/data/doi/index.html`; 
     make sure there are no unintentional line breaks!
                        <tr>
                            <td><a href="https://doi.org/10.12751/g-node.%s">%s</a>
                            <br>%s</td>
                            <td>%s</td>
                            <td><a href="https://doi.org/10.12751/g-node.%s" class ="ui grey label">10.12751/g-node.%s</a></td>
                        </tr>
    """ % (REG_ID, TITLE, CITATION, REG_DATE, REG_ID, REG_ID)
    fp.write(text_block)

    text_block = """
-[ ] update `/data/doi/urls.txt`: https://doi.gin.g-node.org/10.12751/g-node.%s
-[ ] make sure github.com/G-Node/gin-doi is locally build and the `gindoid` executable available
-[ ] gin get G-Node/DOImetadata to or refresh DOIMetadata repo in local staging directory
-[ ] create empty "keywords" directory and run the following from it
-[ ] /path/to/gindoid make-keyword-pages /path/to/DOImetadata/*.xml
-[ ] scp -r keywords %s@%s:/home/%s/staging
    """ % (REG_ID, SERVER_USER, DOI_SERVER, SERVER_USER)
    fp.write(text_block)

    text_block = """
-[ ] connect to DOI server (%s) and move to staging ground
-[ ] sudo chown -R root:root keywords
-[ ] sudo mv /data/doi/keywords /data/doi/keywords_
-[ ] sudo mv keywords/ /data/doi
-[ ] check landing page and keywords online: https://doi.gin.g-node.org
-[ ] sudo rm /data/doi/keywords_ -r
    """ % DOI_SERVER
    fp.write(text_block)

    text_block = """
-[ ] git commit all changes in /data/doi
    sudo git add 10.12751/g-node.%s/
    sudo git commit -m "New dataset: 10.12751/g-node.%s"
-[ ] commit keyword and index page changes
    sudo git add --all
    sudo git commit -m "Update index and keyword pages"
-[ ] set zip to immutable
    sudo chattr +i /data/doi/10.12751/g-node.%s/10.12751_g-node.%s.zip
-[ ] cleanup any leftover directories from previous versions of this dataset
-[ ] email to user (check below)
-[ ] close all related issues on DOImetadata
    """ % (REG_ID, REG_ID, REG_ID, REG_ID)
    fp.write(text_block)

    text_block = """

    """
    fp.write(text_block)


OUT_FILE = "%s_%s.md" % (REG_ID.lower(), REPO_OWN.lower())
print("-- Writing to file %s" % OUT_FILE)
with open(OUT_FILE, "w") as f:
    print_part_pre_doi(f)
    print_part_pre_doi_full(f)
    print_part_post_doi(f)

print("-- Finished writing file %s" % OUT_FILE)
