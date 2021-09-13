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

- clone the repo G-Node/gin-bc20 from gin.g-node.org and copy the contents (minus the git directory) to $PROJ_ROOT directory on the server.
- update the `.env` file content
- update the `docker-compose.yml` file 
  - to match the appropriate docker containers e.g.:
    - gnode/gin-web:posters
    - gnode/bc20-uploader:latest

  - to match the ids of the local `gnode` user and `deploy` group; use `getent passwd` and `getent groups` to find the appropriate ids.
  - make sure the used IP addresses do not overlap with already running docker containers
  - make sure to use ssh ports that do not overlap with any other ssh port in use e.g. -> needs to be adjusted in the gin client later on as well
    - "141.84.41.217:2424:22"

  - make sure the local directories match the local setup
    - ./data/posters-data
    - ./data/posters-tmp
    - ./data/posters-postgresdb

  - change aliases to
    - posterginweb
    - posterpgres

- rename `$PROJ_ROOT/config/gogs/conf/app.ini` to `reference_app.ini` to avoid it being overwritten after initializing the docker container.

- change ownership of the whole `$PROJ_ROOT` directory to the appropriate user and group; also make sure people that may want to edit files are in the same group

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
    - repo root:        as defined in docker-compose on the container side e.g. /data/repos
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
  - the `[service]` section has to contain `REQUIRE_SIGN_IN = true` to ensure, that only logged in users have access to the repositories:
    ```
      REQUIRE_SIGNIN_VIEW    = true
    ```

- if this is not already the case, copy the latest page templates from https://gin.g-node.org/G-Node/gin-bc20 to `$PROJ_ROOT/config/gogs/templates`.
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


## Required repository setup

### ssh access for cloning, local editing and pushing

- copy ssh git key to the gogs user's settings
- create a repo via the webinterface
- clone it locally; use the appropriate port number - in our example it was 2424

  ```bash
      git clone ssh://git@bc.g-node.org:2424/[owner]/[reponame].git
  ```

- to clone the wiki, it has to be initialized via the web service as well
  - bc.g-node.org/[owner]/[reponame]/wiki
  - create a page
  - clone locally:

  ```bash
  git clone ssh://bc.g-node.org:2424/[owner]/[reponame].wiki.git
  ```

### Create all required repos and wikis

- create the following organizations via the Web interface: "BernsteinConference", "G-Node"
- adjust the BernsteinConference organization logo
- create the "Info" repository using the "G-Node" organization and initialize the wiki
- clone the G-Node/Info.wiki.git using git locally and add the footer pages using the files from gin.g-node.org.
- create the following repositories using the "BernsteinConference" organization:
  - Main
  - Posters
  - InvitedTalks
  - ContributedTalks
  - Workshops
  - Exhibition
  - create the first wiki page for all repos via the web interface


## Poster gallery wiki preparations

- locally clone the BC20 repo from github https://github.com/G-Node/BC20
  - initialize and fetch all submodules

- locally clone the BC20data repo from gin (https://gin.g-node.org/G-Node/BC20data)
  - cleanup from the last conference if required
  - when making changes to this repository, make sure to update the corresponding submodule in the BC20 clone or work directly within this clone.

- the following preparations require a couple of manual steps between the main `json` file and a spreadsheet shared with BCOS. The main `json` file will change multiple times before it contains all information required to create the poster gallery.
- As a general note for spreadsheet entries that deal with LINKS: they all HAVE to start with "http" or "https"; Otherwise links in the created markdown files will not create working links.
- prepare a spreadsheet with all required information (posters, invited talks, contributed talks); ideally this spreadsheet is available online e.g. via sciebo and is shared with BCOS.
- the following are the required columns and the column titles have to match exactly; the order can differ and there may be additional columns that will be ignored; NOTE: column title "abstract no NEW" will be transformed to column title "abstract_number" by the `tojson.py` script. Some columns are empty for now and will be manually filled during the next steps.

  "abstract no NEW", "title", "authors", "email", "topic", "id", "session", "time", "upload_key", " "vimeo link", "link hopin", "individual video link" "repo_link"

- save the spreadsheet to a tab separated csv file.
- move to the `scripts` folder of the github "BC20" repository
- run the `tojson.py` script providing the tsv file saved in the step above.

  ```bash
  python tojson.py posters.csv 
  ```

- with the resulting `json` file run the `mkuploadcodes.py` script from the same directory; this will create a `posters-codes.json` file linking the abstract ID to an upload code for the PDF upload service. It also creates a tab separated `posters-codes.tsv` file containing ID mapped to upload code. The uploadcodes require a salt file for the code creation.

  ```bash
  python mkuploadcodes.py [uploadsalt file] [posters.json]
  ```

- move the resulting json file to file `posters.json` in the uploader config directory (`$PROJ_ROOT/config/uploader`) on the server (bc.g-node.org). Restart of the uploader service should not be necessary, but it does not hurt to test if PDF uploads are working.
- add the upload codes to the online spreadsheet "upload_key" column.
- make sure the spreadsheet also contains invited and contributed talks
- download the abstract texts from the GCA server; make sure the `.netrc` credentials are prepared -> check the GCA-Client github README for details.
  - `./gca-client https://abstracts.g-node.org abstracts [conferenceShort] > [output].json`
  - make sure that all abstracts on the server have been REVIEWED. Abstracts in state InReview and InPreparation are skipped.

- from the "scripts" folder of the BC20 repo, run the `mergeabstracts.py` file to merge the main json file with the abstracts information. It will create a `posters-abstracts.json` file containing all posters information with the abstracts texts.

  ```bash
  python mergeabstracts.py abstracts.json posters.json
  ```

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

- copy `assets` and `banners` directories from a previous conference to the "posters" repository, commit and push
  - these are required for the banners on the poster topic pages and poster topic thumbnails
  - the images can also be found in the gin.g-node.org/G-Node/BC20data repository.

- for the poster thumbnail conversion to work, you need 
  - imagemagick installed
  - set the security policy to allow PDFs to be accessed by imagemagick `convert`;
  - see these threads for details [1](https://stackoverflow.com/questions/52998331/imagemagick-security-policy-pdf-blocking-conversion/53180170#53180170), [2](https://imagemagick.org/script/security-policy.php), [3](https://legacy.imagemagick.org/discourse-server/viewtopic.php?t=29653)
  - the policy file can be found by running `convert -list policy`
  - edit the policy file to include the active line `<policy domain="module" rights="read|write" pattern="{PS,PDF,XPS}" />`

- run the following to create poster, contributed and invited talks files.

  ```bash
  python mkgalleries.py [path to posters/abstracts json file] [path to galleries root]
  ```

- run the following to download PDFs from the PDF upload server and create thumbnails for these PDFs
  ```bash
  python mkgalleries.py --download [path to json file] [path to galleries root]
  ```

- run the following to create images for any latex equations in the abstracts texts of the posters. A sidenote at this point: when running plain `mkgalleries.py` and creating the poster index and landing pages, the latex equations in the abstract texts are already replaced with image links. Only when running the following script, the corresponding images are created. The reason for the split is, that rendering the equations takes time and the equations do not change any longer since the abstracts have already been accepted. Due to this, this script should only be required to be run once. If it is not run, the abstract texts will contain broken links in place of the equations.
  ```bash
  python mkgalleries.py --render-equations [path to json file] [path to galleries root]
  ```

- workshops and exhibitions have their own spreadsheet and get their own `tojson` run:
  - the workshop tsv file has to contain "workshops" in its filename before it will be correctly converted to json by the `tojson.py` script.
  - the workshop spreadsheet has to contain the following named columns:
    "workshop number", "workshop name", "organisers", "info url", "talk title", "speakers", "recording status", "recording url"
  - to create the workshops pages, run the `mkgalleries.py` script with the `--workshops` flag

    ```bash
    python mkgalleries.py --workshop [path to workshops json file] [path to galleries root]
    ```

  - the exhibition tsv file has to contain "exhibition" in its filename before it will be correctly converted to json by the `tojson.py` script.
  - the exhibition spreadsheet has to contain the following named columns:
    TBA
  - to create the exhibition pages, run the `mkgalleries.py` script with the `--exhibition` flag

- once all this is done commit and upload the changes for all changed galleries:

  ```bash
    git add --all
    git commit -m "Updates"
    git push origin master
    git push wiki master
  ```

- whenever new changes come in - either via the shared spreadsheet e.g. when the hopin links are provided, if any changes in the abstracts texts are done or if PDFs have been changed, rinse and repeat the following:
  - download shared spreadsheet as tab separated csv
  - run `tojson.py`
  - fetch abstract texts
  - merge abstract texts with json file
  - download PDFs and render equations
  - make galleries
  - if required update workshops as well: download xy-workshops.tsv, `tojson`, `mkworkshopgallery`
  - commit and upload changes to the wiki


### Full bash script to fetch, create and upload the poster gallery

- download all spreadsheet data as tab separated csv files; use "workshops" and "exhibition" in the file names.
- run the following after adjusting the directories appropriately.

    ```bash
    FILES_DIR=/home/$USER/path/to/csv/files
    MAIN_ROOT=/home/$USER/path/to/script/and/galleries/folder
    GCA_CLIENT=/home/$USER/path/to/gca-client
    
    $GCA_CLIENT https://abstracts.g-node.org abstracts conferenceShort > $FILES_DIR/abstracts.json
    
    python $MAIN_ROOT/scripts/tojson.py $FILES_DIR/posters.csv
    python $MAIN_ROOT/scripts/tojson.py $FILES_DIR/workshops.csv
    python $MAIN_ROOT/scripts/tojson.py $FILES_DIR/exhibition.csv
    
    python $MAIN_ROOT/scripts/mergeabstracts.py $FILES_DIR/abstracts.json $FILES_DIR/posters.json
    
    python $MAIN_ROOT/scripts/mkgalleries.py $FILES_DIR/posters-abstracts.json $MAIN_ROOT/galleries/
    python $MAIN_ROOT/scripts/mkgalleries.py --download $FILES_DIR/posters-abstracts.json $MAIN_ROOT/galleries/
    python $MAIN_ROOT/scripts/mkgalleries.py --render-equations $FILES_DIR/posters-abstracts.json $MAIN_ROOT/galleries/
    
    python $MAIN_ROOT/scripts/mkgalleries.py --workshops $FILES_DIR/workshops.json $MAIN_ROOT/galleries/
    
    python $MAIN_ROOT/scripts/mkgalleries.py --exhibition $FILES_DIR/exhibition.json $MAIN_ROOT/galleries/
    
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
