# -- Required fields

# Automated registration id from "10.12751/g-node.[id]"
REG_ID = "id"
# Repository owner
REPO_OWN = "own"
# Repository name
REPO = "repo"
# Format YYYY-MM-DD
REG_DATE = "date"

# DOI requestee email address
EMAIL = "mail"
# DOI requestee full name
USER_FULL_NAME = "full"
# DOI request title
TITLE = ""
# Author citation list; ideally analogous to the DOI landing page citation
CITATION = ""

# Full ssh access name of the server hosting the DOI server instance
DOI_SERVER = "ser.ver.org"
# User working on the DOI server
SERVER_USER = ""
# Full name of the person handling the registration; used in email template text
ADMIN_NAME = "Michael Sonntag"

OUT_FILE = "%s_%s.md" % (REG_ID.lower(), REPO_OWN.lower())
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

-[ ] gin server check annex content
    - cd /gindata
    """ % (REPO_OWN, REPO, USER_FULL_NAME, EMAIL, DOI_SERVER, REG_ID, REG_ID, REG_DATE)
    f.write(text_block)
    f.write("    - ./annexcheck /gindata/gin-repositories/%s" % REPO_OWN.lower())
