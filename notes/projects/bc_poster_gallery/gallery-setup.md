# Bernstein conference Poster gallery setup notes

This file describes the setup of the Bernstein conference variant of the GIN service.

Further it documents the workflow required to populate the conference galleries hosted by this service.


## Installation requirements

Adhere to the installation instructions in the server-setup.md file.

### Required users and groups

gnode, deploy

### Required packages

apache2, certbot, docker, docker-compose

### Required registered domains

The following domains need to be registered before the services can be deployed and https certificates issued via certbot.
- bc.g-node.org
- posters.bc.g-node.org

### Set up apache2 configurations and https certificates

- Set up apache2 configuration files for the two domains listed above.
- Run certbot for both domains once both configurations have been enabled for apache2.
- Again, for details check the general installation instructions in server-setup.md.

## Service installation

### Prepare required directories

```bash
PROJ_ROOT=/data/dev/posters

mkdir -vp $PROJ_ROOT/volumes/posterweb
mkdir -vp $PROJ_ROOT/volumes/uploader
mkdir -vp $PROJ_ROOT/data/posters-data
mkdir -vp $PROJ_ROOT/data/posters-tmp
mkdir -vp $PROJ_ROOT/data/posters-postgresdb
```

### Prepare required files

- clone the repo G-Node/BCCN_Conference from gin.g-node.org and copy the contents of `BC-latest/server-resources/config` to the `$PROJ_ROOT` directory on the server.
- unzip `config/gogs/public.zip` at its location.
- update the `.env` file content.
- update the `docker-compose.yml` file.
  - to match the appropriate docker containers e.g.:
    - gnode/gin-web:gallerydev
    - gnode/bc20-uploader:latest

  - to match the ids of the local `gnode` user and `deploy` group; use `getent passwd` and `getent groups` to find the appropriate ids.
  - make sure the used IP addresses do not overlap with already running docker containers.
  - make sure to use ssh ports that do not overlap with any other ssh port in use e.g., -> needs to be adjusted in the gin client later on as well
    - "141.84.41.217:2424:22"

  - make sure the local directories match the local setup
    - ./data/posters-data
    - ./data/posters-tmp
    - ./data/posters-postgresdb

  - change aliases to
    - posterginweb
    - posterpgres

- rename `$PROJ_ROOT/config/gogs/conf/app.ini` to `reference_app.ini` to avoid it being overwritten after initializing the docker container.

- change ownership of the whole `$PROJ_ROOT` directory to the appropriate user and group; also make sure people that may want to edit files are in the same group.

  ```bash
  sudo chown -R $DEPLOY_USER:$DEPLOY_GROUP $PROJ_ROOT
  sudo chmod g+w $PROJ_ROOT -R
  ```

### Run initial gin service setup

- pull all required docker containers (db, gin-web:bc20, bc20-uploader)

  ```bash
  cd $PROJ_ROOT
  docker-compose pull
  ```

- prepare the postgres database container for the first gin setup

  ```bash
  docker-compose up -d db
  docker exec -it bc_db_1 /bin/bash
  su -l postgres
  createuser -P gin
  # enter password for new role and save it before using it - e.g. somethingSecret
  # note this password, it will later be used on the initial gin setup page
  createdb -O gin gin
  exit
  exit
  ```

- launch gin-web docker container

  ```bash
  docker-compose up web
  ```

- start the gin setup via the browser at bc.g-node.org
    - db:               postgres
    - host:             posterpgres:5432
    - user:             gin
    - password:         [used during database setup]
    - database name:    gin
    - app name:         Bernstein Poster Gallery
    - repo root:        as defined in docker-compose on the container side e.g., /data/repos
    - domain:           bc.g-node.org
    - create an administration user "bcadmin".

- NOTE: DO NOT change the application URL during the initial setup - otherwise the default admin cannot be properly set up

- save; this might redirect to an error page, but this is inconsequential
- check that the page is running at bc.g-node.org
- on the server, stop all containers

  ```bash
  cd $PROJ_ROOT
  docker-compose down
  ```

- modify the `$PROJ_ROOT/config/gogs/conf/app.ini` to mimic the `reference_app.ini`:
  - To ensure custom templates and assets are properly loaded, the ini file's `[server]` section should contain the lines:
    ```
      LOAD_ASSETS_FROM_DISK = true
      STATIC_ROOT_PATH = /custom/
    ```
  - the `[service]` section has to contain `REQUIRE_SIGNIN_VIEW = true` to ensure that only logged in users have access to the repositories:
    ```
      REQUIRE_SIGNIN_VIEW    = true
    ```

- if this is not already the case from a previous step, copy the gogs images and templates "gin.g-node.org/G-Node/BCCN_Conference:/BC-latest/server-resources/config/gogs" to `$PROJ_ROOT/config/gogs/` on the server; make sure the `config/gogs/public.zip` file has been extracted at its location. Update the file ownership.
- update the custom templates and images in `$PROJ_ROOT/config/gogs/templates` so links, times and dates match the current conference requirements.

- update the content of the `$PROJ_ROOT/config/uploader` config file to match the current conference requirements.

- ensure all directories are owned by users and groups that docker has access to via the docker-compose file

  ```bash
  sudo chown -R $DEPLOY_USER:$DEPLOY_GROUP $PROJ_ROOT
  ```

- restart all services

  ```bash
  cd $PROJ_ROOT
  docker-compose up -d
  ```

## Re-using the conference setup on an existing server

The set up at this point can be re-used for another conference. On the current server,
a blank, but functional set up of the service can be found at `$PROJ_ROOT`.

Recursively copy this directory to `posters20XX`, adjusting the directory name to
the current year. Update all required passwords, IP addresses and ports and start
the service from the copied directory.


---- MOVE TO GALLERY-HANDLING FILE


## Required registration routine set up

To enable registration at the poster gallery, the email address has to be made available 
via the uploader service. If not set up differently, the uploader URL is https://posters.bc.g-node.org.

The routine is as follows:
- provide an upload PW on the server in `$PROJ_ROOT/config/uploader/config`
- add email addresses on the uploader service via route `[uploader URL]/uploademail`
- this will create an output file containing hashes of the email addresses
- these hashes can be queried by the poster gallery service via the route `[uploader URL]/uploads/emailwhitelist`
- all email addresses in this hash file are eligible to register with the poster gallery service.


## Required poster upload hash set up

- provide a salt file with an according value in a `$PROJ_ROOT/uploadersalt` file ... it is required for the poster upload hash
- create a poster_hash.json file using the `mkuploadcodes.py` file from gin.g-node.org/G-Node/BCCN-Conference:BC-latest/scripts directory.
- copy the resulting file to `$PROJ_ROOT/config/uploader/poster.json`


## Required repository setup

### ssh access for cloning, local editing and pushing

- copy ssh git key to the gogs user's settings
- create a repo via the webinterface
- clone it locally; use the appropriate port number - in our example it was 2424

  ```bash
      git clone ssh://git@bc.g-node.org:[port]/[owner]/[reponame].git
  ```

- to clone the wiki, it has to be initialized via the web service as well
  - bc.g-node.org/[owner]/[reponame]/wiki
  - create a page
  - clone locally:

  ```bash
  git clone ssh://git@bc.g-node.org:[port]/[owner]/[reponame].wiki.git
  ```

### Create all required repos and wikis

- create the following organizations via the Web interface: "BernsteinConference", "G-Node"
- adjust the BernsteinConference organization logo
- create the "Info" repository using the "G-Node" organization and initialize the wiki
- clone the G-Node/Info.wiki.git using git locally and add the footer pages using the files from https://gin.g-node.org/G-Node/BC20data/BC21/Info.wiki.
- create the following repositories using the "BernsteinConference" organization:
  - Main
  - Posters
  - InvitedTalks
  - ContributedTalks
  - Workshops
  - Exhibition
  - ConferenceInformation
  - create the first wiki page for all repos via the web interface


## Poster gallery wiki preparations

- locally clone the BC20 repo from GitHub https://github.com/G-Node/BC20
  - initialize and fetch all submodules

- locally clone the BC20data repo from gin (https://gin.g-node.org/G-Node/BC20data)
  - cleanup from the last conference if required
  - when making changes to this repository, make sure to update the corresponding submodule in the BC20 clone or work directly within this clone.

- NOTE: due to certain code features, the Python scripts require Python version 3.8+.

- the following preparations require a couple of manual steps between the main `json` file and a spreadsheet shared with BCOS. The main `json` file will change multiple times before it contains all information required to create the poster gallery.
- As a general note for spreadsheet entries that deal with LINKS: they all HAVE to start with "http" or "https"; Otherwise links in the created markdown files will not create working links.
- prepare a spreadsheet with all required information (posters, invited talks, contributed talks); ideally this spreadsheet is available online e.g., via sciebo and is shared with BCOS.
- the following are the required columns, and the column titles have to match exactly; the order can differ and there may be additional columns that will be ignored; NOTE: column title "abstract no NEW" will be transformed to column title "abstract_number" by the `tojson.py` script. Some columns are empty for now and will be manually filled during the next steps.

  "abstract no NEW", "title", "authors", "email", "topic", "id", "session", "time", "upload_key", " "vimeo link", "link hopin", "individual video link" "repo_link"

- save the spreadsheet to a tab separated csv file.
- move to the `scripts` folder of the GitHub "BC20" repository
- run the `tojson.py` script providing the tsv file saved in the step above.

  ```bash
  POSTERS_FILE_CSV=posters.csv
  python tojson.py $POSTERS_FILE_CSV
  ```

- with the resulting `json` file run the `mkuploadcodes.py` script from the same directory; this will create a `posters-codes.json` file linking the abstract ID to an upload code for the PDF upload service. It also creates a tab separated `posters-codes.tsv` file containing ID mapped to upload code. The upload-codes require a salt file for the code creation.

  ```bash
  SALT_FILE=[uploadsalt file]
  POSTERS_JSON=[posters.json]
  python mkuploadcodes.py $SALT_FILE $POSTERS_JSON
  ```

- move the resulting json file to file `posters.json` in the uploader config directory (`$PROJ_ROOT/config/uploader`) on the server (bc.g-node.org). Restart of the uploader service should not be necessary, but it does not hurt to test if PDF uploads are working.
- add the upload codes to the online spreadsheet "upload_key" column.
- make sure the spreadsheet also contains invited and contributed talks
- download the abstract texts from the GCA server; make sure the `.netrc` credentials are prepared -> check the GCA-Client GitHub README for details.
  - `./gca-client https://abstracts.g-node.org abstracts [conferenceShort] > [output].json`
  - make sure that all abstracts on the server have been REVIEWED. Abstracts in state InReview and InPreparation are skipped.

    ```bash
    GCA_CLIENT=[path to gca-client]
    # conference short description e.g. BC20
    CONFERENCE_SHORT=[conferenceShort]
    $GCA_CLIENT https://abstracts.g-node.org abstracts $CONFERENCE_SHORT > abstracts.json`
    ```

- from the "scripts" folder of the BC20 repo, run the `mergeabstracts.py` file to merge the main json file with the abstract information. It will create a `posters-abstracts.json` file containing all poster information with the abstracts texts.

  ```bash
  ABSTRACTS_JSON=abstracts.json
  RAW_POSTERS_JSON=posters.json
  python mergeabstracts.py $ABSTRACTS_JSON $RAW_POSTERS_JSON
  ```

- provide full landing page review to uploading users
  - copy the `posters-abstracts.json` again to the renamed file `posters.json` in the uploader config directory (`$PROJ_ROOT/config/uploader`) on the server (bc.g-node.org)
  - users uploading a poster PDF will now get a complete review page including the abstract after the upload is done.

- update information in the BC20 repo in `scripts/mkgalleries.py` to accommodate the new conference:
  - URLs, repos
  - topics
  - session times
  - item types
  - index_text
  - withdrawn

- create a "galleries" directory in the BC20 repository
- prepare bc.g-node.org repos and wiki remotes; clone all galleries ("posters", "invitedtalks", "contributedtalks", "main", "workshops", "exhibitors") into the BC20 repo "galleries" directory

  ```bash
  e.g.; adjust server name and port as required
  git clone ssh://git@bc.g-node.org:[port]/BernsteinConference/Main.git
  ```

- after cloning, move the repo names to ALL LOWERCASE, otherwise the `mkgallery.py` script will create files in other lowercase dirs; `cd` into the directory; add `wiki` as an additional git remote.

  ```bash
  # rename and move to repo
  git remote add wiki ssh://git@bc.g-node.org:[port]/BernsteinConference/[repo].wiki.git
  ```

- the following batch script can be used to speed up this process, if the categories have not been changed:
  ```bash
  USE_PORT=[port#]
  git clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Main.git
  mv Main/ main
  git -C ./main remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Main.wiki.git
  git clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Posters.git
  mv Posters/ posters
  git -C ./posters remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Posters.wiki.git
  git clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/InvitedTalks.git
  mv InvitedTalks/ invitedtalks
  git -C ./invitedtalks remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/InvitedTalks.wiki.git
  git clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/ContributedTalks.git
  mv ContributedTalks/ contributedtalks
  git -C ./contributedtalks remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/ContributedTalks.wiki.git
  git clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Workshops.git
  mv Workshops/ workshops
  git -C ./workshops remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Workshops.wiki.git
  git clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Exhibition.git
  mv Exhibition/ exhibition
  git -C ./exhibition remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Exhibition.wiki.git
  git clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/ConferenceInformation.git
  mv ConferenceInformation/ conferenceinformation
  git -C ./conferenceinformation remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/ConferenceInformation.wiki.git
  ```

- copy `assets` and `banners` directories from the "gin.g-node.org/G-Node/gin-bc20:/config/gogs/public" directory to the "galleries/posters" repository, commit and push.
  - these are required for the banners on the poster topic pages and poster topic thumbnails

- for the poster thumbnail conversion to work, 
  - `imagemagick` needs to be installed
  - set the security policy to allow PDFs to be accessed by imagemagick `convert`;
  - see these threads for details [1](https://stackoverflow.com/questions/52998331/imagemagick-security-policy-pdf-blocking-conversion/53180170#53180170), [2](https://imagemagick.org/script/security-policy.php), [3](https://legacy.imagemagick.org/discourse-server/viewtopic.php?t=29653)
  - the policy file can be found by running `convert -list policy`
  - edit the policy file to include the active line `<policy domain="module" rights="read|write" pattern="{PS,PDF,XPS}" />`

- run the following to create poster, contributed and invited talks files.

  ```bash
  POSTERS_JSON=[path to "merged" posters/abstracts json file]
  DIR_GALLERIES_ROOT=[path to galleries root]
  python mkgalleries.py $POSTERS_JSON $DIR_GALLERIES_ROOT
  ```

- run the following to download PDFs from the PDF upload server and create thumbnails for these PDFs
  ```bash
  POSTERS_JSON=[path to "merged" posters/abstracts json file]
  DIR_GALLERIES_ROOT=[path to galleries root]
  python mkgalleries.py --download $POSTERS_JSON $DIR_GALLERIES_ROOT
  ```

- run the following to create images for any latex equations in the abstracts texts of the posters. A side note at this point: when running plain `mkgalleries.py` and creating the poster index and landing pages, the latex equations in the abstract texts are already replaced with image links. Only when running the following script, the corresponding images are created. The reason for the split is, that rendering the equations takes time, and the equations do not change any longer since the abstracts have already been accepted. Due to this, this script should only be required to be run once. If it is not run, the abstract texts will contain broken links in place of the equations.
- NOTE that this step requires an existing, FULL installation of `latex`.

  ```bash
  POSTERS_JSON=[path to "merged" posters/abstracts json file]
  DIR_GALLERIES_ROOT=[path to galleries root]
  python mkgalleries.py --render-equations $POSTERS_JSON $DIR_GALLERIES_ROOT
  ```

- workshops and exhibitions have their own spreadsheet and get their own `tojson` run:
  - the workshop tsv file has to contain "workshops" in its filename before it will be correctly converted to json by the `tojson.py` script.
  - the workshop spreadsheet has to contain the following named columns:
    "workshop number", "workshop name", "organisers", "info url", "talk title", "speakers", "recording status", "recording url"
  - to create the workshops pages, run the `mkgalleries.py` script with the `--workshops` flag

    ```bash
    WORKSHOP_JSON=[path to workshop json file]
    DIR_GALLERIES_ROOT=[path to galleries root]
    python mkgalleries.py --workshop $WORKSHOP_JSON $DIR_GALLERIES_ROOT
    ```

  - the exhibition tsv file has to contain "exhibition" in its filename before it will be correctly converted to json by the `tojson.py` script.
  - the exhibition spreadsheet has to contain the following named columns:
    TBA
  - to create the exhibition pages, run the `mkgalleries.py` script with the `--exhibition` flag

    ```bash
    EXHIBITION_JSON=[path to exhibition json file]
    DIR_GALLERIES_ROOT=[path to galleries root]
    python mkgalleries.py --exhibition $EXHIBITION_JSON $DIR_GALLERIES_ROOT
    ```

- check the original data for broken external links using the `linkcheck.py` script:
  ```bash
  POSTERS_JSON=[path to "merged" posters/abstracts json file]
  WORKSHOP_JSON=[path to workshop json file]
  EXHIBITION_JSON=[path to exhibition json file]
  python linkcheck.py $POSTERS_JSON
  python linkcheck.py --workshops $WORKSHOP_JSON
  python linkcheck.py --exhibition $EXHIBITION_JSON
  ```

- once all this is done commit and upload the changes for all changed galleries:

  ```bash
  cd [updated gallery directory]
  git add --all
  git commit -m "Updates"
  git push origin master
  git push wiki master
  ```

- whenever new changes come in - either via the shared spreadsheet e.g., when the hopin links are provided, if any changes in the abstracts texts are done or if PDFs have been changed, rinse and repeat the following:
  - download shared spreadsheet as tab separated csv
  - run `tojson.py`
  - fetch abstract texts
  - merge abstract texts with json file
  - download PDFs and render equations
  - make galleries
  - if required update workshops as well: download xy-workshops.tsv, `tojson`, `mkworkshopgallery`
  - commit and upload changes to the wiki

- the script `docker_log_stats.py` can be used to get basic access statistics out of the gogs docker logs.
  - on the gogs host type `docker ps`; note the container ID
  - run `ls /var/lib/docker` to identify the full [docker ID]
  - the log files can be found at `/var/lib/docker/[docker ID]/[docker ID]-json.log`
  - if there are multiple docker log files, concatenate them before running the `docker_log_stats` script:
    
  ```bash
  DOCKER_LOG=[path/to/docker-json.log]
  python docker_logs_stats.py $DOCKER_LOG
  ```

### After-conference handling

- backup the csv files and galleries to a new folder in the gin.g-node.org/G-Node/BC20data repository.
- backup the added images and template updates from the server at `$ROOT/config/gogs` to the gin.g-node.org/G-Node/gin-bc20 repository.
- add the content of the `static` folder to `/web/static` on the bc.g-node.org machine.
- update the content of the `index.html` file with respect to year and BCOS requests.
- update the apache config files for `bc.g-node.org` and `posters.bc.g-node.org` to point to the static page (see `apache-conf` directory for details) and `sytemctl reload apache2` for the changes to take effect.

### Full bash script to fetch, create and upload the poster gallery

- download all spreadsheet data as tab separated csv files; use "workshops" and "exhibition" in the file names.
- run the following after adjusting the directories appropriately.

  ```bash
  # conference short description e.g. BC20
  CONFERENCE_SHORT=[conferenceShort]
  FILES_DIR=/home/$USER/path/to/data/files
  MAIN_ROOT=/home/$USER/path/to/script/and/galleries/folder
  GCA_CLIENT=/home/$USER/path/to/gca-client
  
  $GCA_CLIENT https://abstracts.g-node.org abstracts $CONFERENCE_SHORT > $FILES_DIR/abstracts.json
  
  python $MAIN_ROOT/scripts/tojson.py $FILES_DIR/posters.csv
  python $MAIN_ROOT/scripts/tojson.py $FILES_DIR/workshops.csv
  python $MAIN_ROOT/scripts/tojson.py $FILES_DIR/exhibition.csv
  
  python $MAIN_ROOT/scripts/mergeabstracts.py $FILES_DIR/abstracts.json $FILES_DIR/posters.json
  
  python $MAIN_ROOT/scripts/mkgalleries.py $FILES_DIR/posters-abstracts.json $MAIN_ROOT/galleries/
  python $MAIN_ROOT/scripts/mkgalleries.py --download $FILES_DIR/posters-abstracts.json $MAIN_ROOT/galleries/
  python $MAIN_ROOT/scripts/mkgalleries.py --render-equations $FILES_DIR/posters-abstracts.json $MAIN_ROOT/galleries/
  
  python $MAIN_ROOT/scripts/mkgalleries.py --workshops $FILES_DIR/workshops.json $MAIN_ROOT/galleries/
  
  python $MAIN_ROOT/scripts/mkgalleries.py --exhibition $FILES_DIR/exhibition.json $MAIN_ROOT/galleries/

  # Check external links to identify potential 404s
  python $MAIN_ROOT/scripts/linkcheck.py $FILES_DIR/posters-abstracts.json
  python $MAIN_ROOT/scripts/linkcheck.py --workshops $FILES_DIR/workshops.json
  python $MAIN_ROOT/scripts/linkcheck.py --exhibition $FILES_DIR/exhibition.json

  # Check changes before commit
  POSTERS_DIR=$MAIN_ROOT/galleries/posters
  INV_TALKS_DIR=$MAIN_ROOT/galleries/invitedtalks
  CON_TALKS_DIR=$MAIN_ROOT/galleries/contributedtalks
  WORK_DIR=$MAIN_ROOT/galleries/workshops
  EXHIB_DIR=$MAIN_ROOT/galleries/exhibition
  
  git -C $POSTERS_DIR status
  
  git -C $INV_TALKS_DIR status
  
  git -C $CON_TALKS_DIR status
  
  git -C $WORK_DIR status
  
  git -C $EXHIB_DIR status
  
  # Commit and push
  git -C $POSTERS_DIR add --all
  git -C $POSTERS_DIR commit -m "Updates"
  git -C $POSTERS_DIR push origin master
  git -C $POSTERS_DIR push wiki master
  
  git -C $INV_TALKS_DIR add --all
  git -C $INV_TALKS_DIR commit -m "Updates"
  git -C $INV_TALKS_DIR push origin master
  git -C $INV_TALKS_DIR push wiki master
  
  git -C $CON_TALKS_DIR add --all
  git -C $CON_TALKS_DIR commit -m "Updates"
  git -C $CON_TALKS_DIR push origin master
  git -C $CON_TALKS_DIR push wiki master
  
  git -C $WORK_DIR add --all
  git -C $WORK_DIR commit -m "Updates"
  git -C $WORK_DIR push origin master
  git -C $WORK_DIR push wiki master
  
  git -C $EXHIB_DIR add --all
  git -C $EXHIB_DIR commit -m "Updates"
  git -C $EXHIB_DIR push origin master
  git -C $EXHIB_DIR push wiki master
  ```