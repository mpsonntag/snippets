# Bernstein Conference poster gallery handling notes

These notes describe how to
- prepare a running instance of the GIN poster gallery
- use the companion poster uploader service to enable user registration on the poster gallery
- create and upload the poster gallery content

These notes require a running service as described in the [server setup notes](./gallery-setup.md).


## Required gallery service content preparations

### Required registration routine set up

To enable registration at the poster gallery, the email address has to be made available 
via the uploader service. If not set up differently, the uploader URL is https://posters.bc.g-node.org.

The routine is as follows:
- provide an upload PW on the server in `$PROJ_ROOT/config/uploader/config`
- add email addresses on the uploader service via route `[uploader URL]/uploademail`
- this will create an output file containing hashes of the email addresses
- these hashes can be queried by the poster gallery service via the route `[uploader URL]/uploads/emailwhitelist`
- all email addresses in this hash file are eligible to register with the poster gallery service.


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
  repository for now. Further, prepare `notes` and `rawdata` directories

  ```bash
  GALLERIES_STAGING=$CONFERENCE_ROOT/staging.ignore
  mkdir -vp $GALLERIES_STAGING
  mkdir -v $CONFERENCE_ROOT/rawdata
  mkdir -v $CONFERENCE_ROOT/notes
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

## Poster gallery wiki preparations

- The following describes how to create the poster gallery content files from information
  received from online spreadsheets provided by BCOS and information from the abstracts 
  service.
- all scripts required to create the poster gallery content are found in the 
  G-Node/BCCN_Conference repository at $REPO_ROOT/scripts.
- due to certain code features, the Python scripts require Python version 3.8+.
- the structure of the required spreadsheets can be reviewed in files from the previous
  conferences e.g. in "BCCN_Conference/BC21/rawdata".

### Create initial posters json file from BCOS spreadsheets

- as a general note for spreadsheet entries that deal with LINKS: they all HAVE to start 
  with "http" or "https"; otherwise links in the created markdown files will not create 
  working links.
- the following preparations require a couple of manual steps between the main `json` 
  file and a spreadsheet shared with BCOS. The main `json` file will be updated multiple 
  times before it contains all information required to create the final poster gallery.
- prepare a single spreadsheet with the information about "posters", "invited talks" and 
  "contributed talks". Ideally this spreadsheet is available online e.g., via sciebo and 
  is shared with BCOS.
- the following are the required columns in this spreadsheet, and the column titles have 
  to match exactly; the order can differ and there may be additional columns that will 
  be ignored:
  "abstract no NEW", "title", "authors", "email", "topic", "id", "session", "time", 
  "upload_key", "vimeo link", "link hopin", "individual video link" "repo_link", 
  "abstract", "Poster_Board_Number"
- NOTE: column title "abstract no NEW" will be transformed to column title 
  "abstract_number" by the `tojson.py` script. Some columns are empty for now and will be 
  manually filled during the next steps.

- save this spreadsheet to a local file. NOTE: when downloading from a SciBo spreadsheet to
  a tab separated file, it might happen, that the line breaks are not properly parsed by
  the conversion script. To avoid this issue, save the file as ".xlsx", open locally with
  libre office and export to a tab separated, UTF-8 CSV file.
  The tell-tale error to look for when running the script is:

  ```
  UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe4 in position 1855: invalid continuation byte
  ```

- the file can automatically be converted to a tab delimited text file using libreoffice.
  Check the details for the conversion here: https://wiki.openoffice.org/wiki/Documentation/DevGuide/Spreadsheets/Filter_Options

  ```bash
  CONFERENCE_SHORT=[BC2X]
  REPO_ROOT=/home/$USER/[adjust]/BCCN_Conference
  DOWNLOAD_DIR=[path/to/downloads]
  FILENAME_BASE=[filename without extension]

  CONFERENCE_DATA=$REPO_ROOT/$CONFERENCE_SHORT/rawdata

  EXPORTED_XLSX_FILE=$DOWNLOAD_DIR/$FILENAME_BASE.xlsx
  EXPORTED_CSV_FILE=$CONFERENCE_DATA/$FILENAME_BASE.csv

  POSTERS_CSV_FILE=$CONFERENCE_DATA/posters.csv

  # converts to tab (9) delimited text file, using " (34) as text delimiter and 
  # UTF-8 (76) as charset.
  libreoffice --headless  --convert-to "csv:Text - txt - csv (StarCalc):9,34,76,1,1/1" --outdir $CONFERENCE_DATA $EXPORTED_XLSX_FILE

  mv $EXPORTED_CSV_FILE $POSTERS_CSV_FILE
  ```

- use the `tojson.py` script from `BCCN_Conference/scripts` to create the initial 
  `posters.json` file.

  ```bash
  CONFERENCE_SHORT=[BC2X]
  REPO_ROOT=/home/$USER/[adjust]/BCCN_Conference

  CONFERENCE_DATA=$REPO_ROOT/$CONFERENCE_SHORT/rawdata
  SCRIPTS_DIR=$REPO_ROOT/scripts
  POSTERS_CSV_FILE=$CONFERENCE_DATA/posters.csv

  # make sure to use Python 3.8+
  python $SCRIPTS_DIR/tojson.py $POSTERS_CSV_FILE
  ```


### Poster PDF upload key handling

Poster authors have to upload their PDFs and video URLs via https://posters.bc.g-node.org.
To do this, they require a poster upload key. The keys are tied to the poster abstract
UUID from abstracts.g-node.org. The service at posters.bc.g-node.org requires a `posters.json`
file containing the full poster information, poster abstract and upload key.
To create this from scratch, a couple of steps are required:

- use the `posters.json` file with the salt hash string from `BCCN_Conference/BC2X/server-resources/uploadersalt` 
  to create the upload keys tied to the abstracts UUID.

  ```bash
  CONFERENCE_SHORT=[BC2X]
  REPO_ROOT=/home/$USER/[adjust]/BCCN_Conference

  SCRIPTS_DIR=$REPO_ROOT/scripts

  SALT_FILE=$REPO_ROOT/$CONFERENCE_SHORT/server-resources/uploadersalt
  CONFERENCE_DATA=$REPO_ROOT/$CONFERENCE_SHORT/rawdata
  POSTERS_JSON=$CONFERENCE_DATA/posters.json

  # the script writes output files into the current directory; switch to the raw data dir
  cd $CONFERENCE_DATA
  python $SCRIPTS_DIR/mkuploadcodes.py $SALT_FILE $POSTERS_JSON
  ```

- paste the output of the `posters-codes.tsv` into the SciBo spreadsheet; the first column
  are the abstract UUIDs, the second column are the upload keys created using these
  UUIDs; copy this data to the "upload_key" column and cross check whether the keys match
  the appropriate abstract UUID.
  The next time the SciBo spreadsheet is imported, the upload keys will be part
  of the created `posters.json` file.

- TODO: add the `abstracts_uploadkey_csv.py` script to scripts and add the option here before the initial information is sent to BCOS -> saves the roundabout handling with the `mkuploadcodes.py` script.


### Accepted authors list for the uploader service

- make sure to download the latest SciBo spreadsheet and re-create the `posters.json`
  file including the `upload_key` values.
- locally clone the [GCA-Python](https://github.com/G-Node/GCA-Python) client. Make sure 
  the local `.netrc` credentials are prepared; check the GCA-Python README for details.
- make sure that all abstracts on the GCA-Web server have been reviewed and are set to 
  "ACCEPTED". Abstracts in state "InReview" and "InPreparation" are skipped; authors of
  skipped abstracts will not be able to upload their data.
- download the abstract texts from the GCA server.

  ```bash
  CONFERENCE_SHORT=[BC2X]
  REPO_ROOT=/home/$USER/[adjust]/BCCN_Conference
  GCA_CLIENT=[path to gca-client]/GCA-Python/gca-client

  ABSTRACTS_JSON=$REPO_ROOT/$CONFERENCE_SHORT/rawdata/abstracts.json

  # make sure to use Python 3.8+
  $GCA_CLIENT https://abstracts.g-node.org abstracts $CONFERENCE_SHORT > $ABSTRACTS_JSON
  ```

- merge the information from `posters.json` and `abstracts.json` using the 
  `mergeabstracts.py` script from `BCCN_Conference/scripts`. It will create a 
  `posters-abstracts.json` file containing all poster information including the 
  abstracts texts.
  
  ```bash
  CONFERENCE_SHORT=[BC2X]
  REPO_ROOT=/home/$USER/[adjust]/BCCN_Conference

  SCRIPTS_DIR=$REPO_ROOT/scripts
  CONFERENCE_DATA=$REPO_ROOT/$CONFERENCE_SHORT/rawdata
  POSTERS_JSON=$CONFERENCE_DATA/posters.json
  ABSTRACTS_JSON=$CONFERENCE_DATA/abstracts.json

  python $SCRIPTS_DIR/mergeabstracts.py $ABSTRACTS_JSON $POSTERS_JSON
  ```

- copy the resulting `posters-abstracts.json` to the server hosting the poster
  upload service. Copy it as `posters.json` to `$PROJ_ROOT/config/uploader/poster.json`.
  Authors will now be able to upload their poster using the key they have been provided.
  Using the information from the `posters.json` file, the upload key will link the
  uploaded poster PDF and any video url to the appropriate abstract and will save
  the information as [abstractUUID].pdf or [abstractUUID].url in `$PROJ_ROOT/volumes/uploader`
  Restart of the uploader service should not be necessary, but it does not hurt to test 
  if PDF uploads are working after the `posters.json` file has been updated. Authors
  that have not been approved via the abstracts.g-node.org service yet (abstract not
  in state "Approved") will also not be able to upload any data via the uploader.
  Furthermore, after an author has uploaded a PDF, the resulting page will show
  a preview of the Poster landing page including all relevant information including
  the abstract of the poster.

- everytime information changes in the SciBo spreadsheet or in the state of the
  abstracts, redo the previous steps and update the `posters.json` file on the
  uploader service.


### Creating the gallery content

- update all relevant information in the `BCCN_Conference/scripts/mkgalleries.py` script
  to accommodate the current conference:
  - URLs, repos
  - topics
  - session times
  - item types
  - index_text
  - withdrawn IDs
  - not available Poster PDF IDs
- make sure the posters spreadsheet also contains invited and contributed talks

- run the following to create poster, contributed and invited talks files.

  ```bash
  CONFERENCE_SHORT=[BC2X]
  REPO_ROOT=/home/$USER/[adjust]/BCCN_Conference

  SCRIPTS_DIR=$REPO_ROOT/scripts
  GALLERIES_STAGING=$REPO_ROOT/$CONFERENCE_SHORT/staging.ignore
  CONFERENCE_DATA=$REPO_ROOT/$CONFERENCE_SHORT/rawdata
  POSTERS_JSON=$CONFERENCE_DATA/posters-abstracts.json

  python $SCRIPTS_DIR/mkgalleries.py $POSTERS_JSON $GALLERIES_STAGING
  ```

- run the following to download PDFs from the PDF upload server and create thumbnails for these PDFs
  ```bash
  CONFERENCE_SHORT=[BC2X]
  REPO_ROOT=/home/$USER/[adjust]/BCCN_Conference

  SCRIPTS_DIR=$REPO_ROOT/scripts
  GALLERIES_STAGING=$REPO_ROOT/$CONFERENCE_SHORT/staging.ignore
  CONFERENCE_DATA=$REPO_ROOT/$CONFERENCE_SHORT/rawdata
  POSTERS_JSON=$CONFERENCE_DATA/posters-abstracts.json

  python $SCRIPTS_DIR/mkgalleries.py --download $POSTERS_JSON $GALLERIES_STAGING
  ```

- for the poster thumbnail conversion to work, 
  - `imagemagick` needs to be installed
  - set the security policy to allow PDFs to be accessed by imagemagick `convert`;
  - see these threads for details [1](https://stackoverflow.com/questions/52998331/imagemagick-security-policy-pdf-blocking-conversion/53180170#53180170), [2](https://imagemagick.org/script/security-policy.php), [3](https://legacy.imagemagick.org/discourse-server/viewtopic.php?t=29653)
  - the policy file can be found by running `convert -list policy`
  - edit the policy file to include the active line `<policy domain="module" rights="read|write" pattern="{PS,PDF,XPS}" />`

- run the following to create images for any latex equations in the abstracts texts of the posters. A side note at this point: when running plain `mkgalleries.py` and creating the poster index and landing pages, the latex equations in the abstract texts are already replaced with image links. Only when running the following script, the corresponding images are created. The reason for the split is, that rendering the equations takes time, and the equations do not change any longer since the abstracts have already been accepted. Due to this, this script should only be required to be run once. If it is not run, the abstract texts will contain broken links in place of the equations.
- NOTE that this step requires an existing, FULL installation of `latex`.

  ```bash
  CONFERENCE_SHORT=[BC2X]
  REPO_ROOT=/home/$USER/[adjust]/BCCN_Conference

  SCRIPTS_DIR=$REPO_ROOT/scripts
  GALLERIES_STAGING=$REPO_ROOT/$CONFERENCE_SHORT/staging.ignore
  CONFERENCE_DATA=$REPO_ROOT/$CONFERENCE_SHORT/rawdata
  POSTERS_JSON=$CONFERENCE_DATA/posters-abstracts.json

  python $SCRIPTS_DIR/mkgalleries.py --render-equations $POSTERS_JSON $GALLERIES_STAGING
  ```


### Workshop, Exhibition, Conference information handling

- workshops and exhibitions have their own spreadsheet download and convert to tsv accordingly.
- the workshop tsv file has to contain "workshops" in its filename before it will be 
  correctly converted to json by the `tojson.py` script.
- the workshop spreadsheet has to contain the following named columns:
  "workshop number", "workshop name", "organisers", "info url", "talk title", "speakers", "recording status", "recording url"
- to create the workshops pages, run the `mkgalleries.py` script with the `--workshops` flag

  ```bash
  CONFERENCE_SHORT=[BC2X]
  REPO_ROOT=/home/$USER/[adjust]/BCCN_Conference

  SCRIPTS_DIR=$REPO_ROOT/scripts
  GALLERIES_STAGING=$REPO_ROOT/$CONFERENCE_SHORT/staging.ignore
  CONFERENCE_DATA=$REPO_ROOT/$CONFERENCE_SHORT/rawdata
  WORKSHOP_JSON=$CONFERENCE_DATA/workshop.json

  python $SCRIPTS_DIR/mkgalleries.py --workshop $WORKSHOP_JSON $GALLERIES_STAGING
  ```

- the exhibition tsv file has to contain "exhibition" in its filename before it will be 
  correctly converted to json by the `tojson.py` script.
- the exhibition spreadsheet has to contain the following named columns:
    TBA
- to create the exhibition pages, run the `mkgalleries.py` script with the `--exhibition` flag

  ```bash
  CONFERENCE_SHORT=[BC2X]
  REPO_ROOT=/home/$USER/[adjust]/BCCN_Conference

  SCRIPTS_DIR=$REPO_ROOT/scripts
  GALLERIES_STAGING=$REPO_ROOT/$CONFERENCE_SHORT/staging.ignore
  CONFERENCE_DATA=$REPO_ROOT/$CONFERENCE_SHORT/rawdata
  EXHIBITION_JSON=$CONFERENCE_DATA/exhibition.json

  python $SCRIPTS_DIR/mkgalleries.py --exhibition $EXHIBITION_JSON $GALLERIES_STAGING
  ```

- TODO: Conference information handling

- check the original data for broken external links using the `linkcheck.py` script:
  ```bash
  CONFERENCE_SHORT=[BC2X]
  REPO_ROOT=/home/$USER/[adjust]/BCCN_Conference

  SCRIPTS_DIR=$REPO_ROOT/scripts
  GALLERIES_STAGING=$REPO_ROOT/$CONFERENCE_SHORT/staging.ignore
  CONFERENCE_DATA=$REPO_ROOT/$CONFERENCE_SHORT/rawdata
  POSTERS_JSON=$CONFERENCE_DATA/posters-abstracts.json
  WORKSHOP_JSON=$CONFERENCE_DATA/workshop.json
  EXHIBITION_JSON=$CONFERENCE_DATA/exhibition.json

  python $SCRIPTS_DIR/linkcheck.py $POSTERS_JSON
  python $SCRIPTS_DIR/linkcheck.py --workshops $WORKSHOP_JSON
  python $SCRIPTS_DIR/linkcheck.py --exhibition $EXHIBITION_JSON
  ```

### Gallery content updates

- once all this is done, commit and upload the changes for all changed galleries:

  ```bash
  cd [updated gallery directory]
  git add --all
  git commit -m "Updates"
  git push origin master
  git push wiki master
  ```

- the following script can be used to automatically commit and upload any current changes:

  ```bash
  CONFERENCE_SHORT=[BC2X]
  REPO_ROOT=/home/$USER/[adjust]/BCCN_Conference

  GALLERIES_STAGING=$REPO_ROOT/$CONFERENCE_SHORT/staging.ignore

  alias galleryup='function __galleryup() {
    echo "Handling $CURR_DIR";
    git -C $GALLERIES_STAGING/$CURR_DIR add --all;
    git -C $GALLERIES_STAGING/$CURR_DIR commit -m "Updates";
    git -C $GALLERIES_STAGING/$CURR_DIR push origin master;
    git -C $GALLERIES_STAGING/$CURR_DIR push wiki master;
  }; __galleryup'

  # Handle Main
  CURR_DIR=main
  galleryup

  # Handle Posters
  CURR_DIR=posters
  galleryup

  # Handle Invited Talks
  CURR_DIR=invitedtalks
  galleryup

  # Handle Contributed Talks
  CURR_DIR=contributedtalks
  galleryup

  # Handle workshops
  CURR_DIR=workshops
  galleryup

  # Handle Exhibition
  CURR_DIR=exhibition
  galleryup

  # Handle Conference Information
  CURR_DIR=conferenceinformation
  galleryup
  ```

- whenever new changes come in - either via the shared spreadsheet e.g., 
  when the hopin links are provided, if any changes in the abstracts texts are done or 
  if PDFs have been changed, rinse and repeat the following:
  - download shared spreadsheet as tab separated csv
  - run `tojson.py`
  - fetch abstract texts
  - merge abstract texts with json file
  - update posters-abstracts.json on the uploader service
  - download PDFs and render equations
  - make galleries
  - if required update workshops as well: download xy-workshops.tsv, `tojson`, `mkworkshopgallery`
  - commit and upload changes to the wiki


### Full update convenience script


### Statistics via docker logs

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

- add the initial csv file to the `[BC2X]/rawdata` folder

- add all discussion notes, timetable notes, emails on the subject, email templates, 
  image or banner zip files to the `[BC2X]/notes` directory for easy review in the next 
  year.

- archive the poster gallery content

  ```bash
  CONFERENCE_SHORT=[BC2X]
  REPO_ROOT=/home/$USER/[adjust]/BCCN_Conference
  CONFERENCE_ROOT=$REPO_ROOT/$CONFERENCE_SHORT
  GALLERIES_ARCHIVE=$CONFERENCE_ROOT/galleries
  GALLERIES_STAGING=$CONFERENCE_ROOT/staging.ignore

  # Handle Info.wiki
  HANDLE_DIR=Info.wiki
  cp $GALLERIES_STAGING/$HANDLE_DIR -r $GALLERIES_ARCHIVE/$HANDLE_DIR

  # Handle Main
  HANDLE_DIR=main
  HANDLE_ARCHIVE=Main
  cp $GALLERIES_STAGING/$HANDLE_DIR -r $GALLERIES_ARCHIVE/$HANDLE_ARCHIVE

  # Handle Invited Talks
  HANDLE_DIR=invitedtalks
  HANDLE_ARCHIVE=InvitedTalks
  cp $GALLERIES_STAGING/$HANDLE_DIR -r $GALLERIES_ARCHIVE/$HANDLE_ARCHIVE

  # Handle Contributed Talks
  HANDLE_DIR=contributedtalks
  HANDLE_ARCHIVE=ContributedTalks
  cp $GALLERIES_STAGING/$HANDLE_DIR -r $GALLERIES_ARCHIVE/$HANDLE_ARCHIVE

  # Handle workshops
  HANDLE_DIR=workshops
  HANDLE_ARCHIVE=Workshops
  cp $GALLERIES_STAGING/$HANDLE_DIR -r $GALLERIES_ARCHIVE/$HANDLE_ARCHIVE

  # Handle Exhibition
  HANDLE_DIR=exhibition
  HANDLE_ARCHIVE=Exhibition
  cp $GALLERIES_STAGING/$HANDLE_DIR -r $GALLERIES_ARCHIVE/$HANDLE_ARCHIVE

  # Handle Conference Information
  HANDLE_DIR=conferenceinformation
  HANDLE_ARCHIVE=ConferenceInformation
  cp $GALLERIES_STAGING/$HANDLE_DIR -r $GALLERIES_ARCHIVE/$HANDLE_ARCHIVE

  # Keep updates of the smaller repos and Posters separate
  gin commit $GALLERIES_ARCHIVE -m "Update gallery archive"
  gin upload .

  # Handle Posters
  HANDLE_DIR=posters
  HANDLE_ARCHIVE=Posters

  # Posters contains a large number of files. Keep the files per commit at a lower level.
  # Also put PDF content into the annex to keep the initial clone of the repo light and fast.
  cp $GALLERIES_STAGING/$HANDLE_DIR -r $GALLERIES_ARCHIVE/$HANDLE_ARCHIVE
  gin commit $GALLERIES_ARCHIVE/$HANDLE_ARCHIVE/*.url -m "Adding poster video urls"
  gin git annex add $GALLERIES_ARCHIVE/$HANDLE_ARCHIVE/*.pdf
  gin git commit -m "Adding poster PDFs to annex"
  gin commit . -m "Add poster resources"
  gin upload .
  ```
