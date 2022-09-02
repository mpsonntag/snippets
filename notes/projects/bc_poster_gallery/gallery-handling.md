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

### ssh access for wiki cloning, local content preparation and upload

- make sure the git ssh key added to the poster gallery admin is used by
  the local git configuration.
- use git and not the gin client to handle the poster gallery repositories.

- git clone all gallery repositories into the `$GALLERIES_STAGING` directory
  and add wiki remotes. The following routine describes the general process for all 
  repositories except `G-Node/Info.wiki`. A convenience script can be found further down.

  - all wikis should be initialized first via the web service, if this has not been
    done yet:
    - access bc.g-node.org/[owner]/[reponame]/wiki
    - create a page
  - clone a repository locally; use the appropriate port number

    ```bash
    REPO_OWNER=[e.g. BernsteinConference]
    REPO_NAME=[e.g. Posters]
    USE_PORT=[gallery service git port]
    git clone ssh://git@bc.g-node.org:$USE_PORT/$REPO_OWNER/$REPO_NAME.git
    ```

  - add the wiki as second remote for the repository

    ```bash
    cd $REPO_NAME
    git remote add wiki ssh://git@bc.g-node.org:$USE_PORT/$REPO_OWNER/$REPO_NAME.wiki.git
    ```

- the following script should clone and set up all required repositories in the local 
  staging directory. This script might need to change for future conferences.

  ```bash
  CONFERENCE_SHORT=[BC2X]
  REPO_ROOT=/home/$USER/[adjust]/BCCN_Conference
  CONFERENCE_ROOT=$REPO_ROOT/$CONFERENCE_SHORT
  GALLERIES_STAGING=$CONFERENCE_ROOT/staging.ignore
  USE_PORT=[gallery service git port]

  git -C $GALLERIES_STAGING clone ssh://git@bc.g-node.org:$USE_PORT/G-Node/Info.wiki

  git -C $GALLERIES_STAGING clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Main.git main
  git -C $GALLERIES_STAGING/main remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Main.wiki.git

  git -C $GALLERIES_STAGING clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Posters.git posters
  git -C $GALLERIES_STAGING/posters remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Posters.wiki.git

  git -C $GALLERIES_STAGING clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/InvitedTalks.git invitedtalks
  git -C $GALLERIES_STAGING/invitedtalks remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/InvitedTalks.wiki.git

  git -C $GALLERIES_STAGING clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/ContributedTalks.git contributedtalks
  git -C $GALLERIES_STAGING/contributedtalks remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/ContributedTalks.wiki.git

  git -C $GALLERIES_STAGING clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Workshops.git workshops
  git -C $GALLERIES_STAGING/workshops remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Workshops.wiki.git

  git -C $GALLERIES_STAGING clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Exhibition.git exhibition
  git -C $GALLERIES_STAGING/exhibition remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Exhibition.wiki.git

  git -C $GALLERIES_STAGING clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/ConferenceInformation.git conferenceinformation
  git -C $GALLERIES_STAGING/conferenceinformation remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/ConferenceInformation.wiki.git
  ```

- copy the required wiki resources like images or Info.wiki files to the staging directories

  ```bash
  CONFERENCE_SHORT=[BC2X]
  REPO_ROOT=/home/$USER/[adjust]/BCCN_Conference
  CONFERENCE_ROOT=$REPO_ROOT/$CONFERENCE_SHORT
  GALLERIES_ARCHIVE=$CONFERENCE_ROOT/galleries
  GALLERIES_STAGING=$CONFERENCE_ROOT/staging.ignore

  cp -v $GALLERIES_ARCHIVE/Info.wiki $GALLERIES_STAGING/Info.wiki -r
  cp -v $GALLERIES_ARCHIVE/main $GALLERIES_STAGING/main -r
  cp -v $GALLERIES_ARCHIVE/posters $GALLERIES_STAGING/posters -r
  ```

- update the following files to fit the current conference:
  - `$GALLERIES_STAGING/main/Home.md`
  - all files in `$GALLERIES_STAGING/Info.wiki`

- commit and upload. Fhe first push to the repository wikis will require a 
  force push, since the wikis have been initialized on the server and contain
  content that is not required but locally not in the git history.

  ```bash
  CONFERENCE_SHORT=[BC2X]
  REPO_ROOT=/home/$USER/[adjust]/BCCN_Conference
  CONFERENCE_ROOT=$REPO_ROOT/$CONFERENCE_SHORT
  GALLERIES_ARCHIVE=$CONFERENCE_ROOT/galleries
  GALLERIES_STAGING=$CONFERENCE_ROOT/staging.ignore

  alias galleryupforce='function __galleryupforce() {
    echo "Handling $HANDLE_DIR";
    git -C $GALLERIES_STAGING/$HANDLE_DIR add --all;
    git -C $GALLERIES_STAGING/$HANDLE_DIR commit -m "Inital commit";
    git -C $GALLERIES_STAGING/$HANDLE_DIR push origin master;
    git -C $GALLERIES_STAGING/$HANDLE_DIR push wiki master -f;
  }; __galleryupforce'

  # Handle Info.wiki
  HANDLE_DIR=Info.wiki
  git -C $GALLERIES_STAGING/$HANDLE_DIR add --all
  git -C $GALLERIES_STAGING/$HANDLE_DIR commit -m "Inital commit"
  git -C $GALLERIES_STAGING/$HANDLE_DIR push origin master

  # Handle Main
  HANDLE_DIR=main
  galleryupforce

  # Handle Invited Talks
  HANDLE_DIR=invitedtalks
  galleryupforce

  # Handle Contributed Talks
  HANDLE_DIR=contributedtalks
  galleryupforce

  # Handle workshops
  HANDLE_DIR=workshops
  galleryupforce

  # Handle Exhibition
  HANDLE_DIR=exhibition
  galleryupforce

  # Handle Conference Information
  HANDLE_DIR=conferenceinformation
  galleryupforce

  # Handle Posters
  HANDLE_DIR=posters
  galleryupforce
  ```
