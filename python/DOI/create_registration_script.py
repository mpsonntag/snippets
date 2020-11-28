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

OUT_FILE = "%s_%s.md" % (REG_ID.lower(), REPO_OWN.lower())
print("-- Writing to file %s" % OUT_FILE)
with open(OUT_FILE, "w") as f:
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
    f.write(text_block)

    text_block = """

-[ ] gin server check annex content
    - cd /gindata
    - ./annexcheck /gindata/gin-repositories/%s
    """ % REPO_OWN.lower()
    f.write(text_block)

    text_block = """
-[ ] check the datacite content at https://gin.g-node.org/%s/%s
    - check if the repo is eligible to be published on gin
    - title is useful and has no typos
    - license title, license content and license link match
    """ % (REPO_OWN, REPO)
    f.write(text_block)

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
    f.write(text_block)

    text_block = """
-[ ] fetch content and upload to DOI repo
    - cd /data/doiprep/
    - screen -S %s
    - sudo su root
    - ./syncannex %s/%s > %s_%s.log
    """ % (REPO_OWN.lower(), REPO_OWN, REPO, REPO_OWN.lower(), REPO)
    f.write(text_block)

    text_block = """
-[ ] tag release on the DOI repository; run all commands using `gin git ...` 
     to avoid issues with local git annex or differently logged in users.
    -[ ] cd /data/doiprep/%s
    -[ ] sudo gin git status
    -[ ] sudo gin git remote -v
    -[ ] sudo gin git tag 10.12751/g-node.%s
    -[ ] sudo gin git push --tags origin
    """ % (REPO.lower(), REG_ID)
    f.write(text_block)

    text_block = """
-[ ] cleanup directory once tagging is done
    -[ ] sudo rm /data/doiprep/%s -r
    -[ ] sudo mv /data/doiprep/%s*.log /home/%s/logs/
    """ % (REPO.lower(), REPO_OWN, SERVER_USER)
    f.write(text_block)

    text_block = """
-[ ] email to TWachtler

Hi Thomas,

the repository should be prepared for the DOI registration.

Best,
%s
    """ % (ADMIN_NAME.split()[0])
    f.write(text_block)

print("-- Finished writing file %s" % OUT_FILE)
