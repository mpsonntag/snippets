# Bernstein Conference poster gallery handling notes

These notes describe how to
- prepare a running instance of the GIN poster gallery
- use the companion poster uploader service to enable user registration on the poster gallery
- create and upload the poster gallery content

These notes require a running service as described in the [server setup notes](./gallery-setup.md).


## Required gallery service content preparations

### Gallery service preparation; ssh access, organizations and required repositories
- log in to the running gallery service (bc.g-node.org) using the admin user
- copy a git ssh key to the user's settings; https://bc.g-node.org/user/settings/ssh
- create the following organizations via the Web interface
  - BernsteinConference
  - G-Node
- adjust the BernsteinConference organization logo e.g. use G-Node/BCCN_Conference:/BC-latest/server-resources/static/resources/favicon.png
- create the "Info" repository using the "G-Node" organization and initialize the wiki
- create the following repositories using the "BernsteinConference" organization; initialize all wiki pages
  - Main
  - Posters
  - InvitedTalks
  - ContributedTalks
  - Workshops
  - Exhibition
  - ConferenceInformation

### Local preparations

- clone the GIN G-Node/BCCN_Conference repository. It contains all required configs, templates 
  and assets to populate the required poster gallery wiki pages.
- Note: a full `gin get-content` is not required for now; PDF files from previous conferences
  are kept in the annex, but are not necessary.

  ```bash
  gin get G-Node/BCCN_Conference
  REPO_ROOT=$(pwd)/BCCN_Conference
  ```

- copy `BC-latest` to a new directory in the BCCN_Conference repository. This directory
  will archive any changes made to the gallery service config files, templates and assets, any
  changes to the gallery content scripts and provides a staging ground and an archive for 
  the gallery content.

  ```bash
  # adjust the CONFERENCE_SHORT value to reflect the current years' conference e.g. BC22
  CONFERENCE_SHORT=[BC2X]
  ORIGIN=$REPO_ROOT/BC-latest
  CONFERENCE_ROOT=$REPO_ROOT/$CONFERENCE_SHORT
  cp -v $ORIGIN $CONFERENCE_ROOT -r
  cd $REPO_ROOT/$CONFERENCE_SHORT
  ```

- if required, update all passwords, keys, IP addresses and port numbers found in the `$REPO_ROOT/$CONFERENCE_SHORT/server-resources` folder
  according to the used settings on the running server.
  - `docker-compose.yml`
  - `config/gogs/conf/app.ini`
  - `config/postgres/postgressecrets.env`
  - `config/uploader/config`
  - the `uploadersalt` string

- commit and upload the changes

  ```bash
  cd $REPO_ROOT
  gin commit $CONFERENCE_ROOT -m "Add basic conference information"
  gin upload
  ```

- prepare a wiki staging directory in the BCCN_Conference repository. The directory name
  should include ".ignore" to make sure these files will not yet become part of the
  repository for now.

  ```bash
  GALLERIES_STAGING=$CONFERENCE_ROOT/staging.ignore
  mkdir -vp $GALLERIES_STAGING
  ```
