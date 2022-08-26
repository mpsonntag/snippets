
TODO merge with previous gallery setup notes

### Setup process new conference

- keep the repository private, but make sure no live passwords are used in the config files
- keep the files with passwords in the appropriate repository

- clone repo; a full get-content is not required for now;

  ```bash
  gin get G-Node/BC-Gallery
  ```

- copy BC-latest to [BC2X] and set up the staging directory, which should be excluded from
  the git directory content.

    ```bash
    ORIGIN=/home/$USER/[path/to]/BC-latest
    TARGET=/home/$USER/[path/to]/[BC2X]
    GALLERIES_STAGING=$TARGET/staging.ignore
    cp -v $ORIGIN $TARGET -r
    mkdir -vp $GALLERIES_STAGING
    ```

- set up uploader and gogs on the hosting server
- if required use the server-resources and update all passwords, keys and IP addresses and port numbers
  - docker-compose.yml
  - app.ini
  - postgressecrets.env
  - uploader/config
  - update the uploadersalt string in [BC2X] if required
- set up required organisations and repositories on the running gogs instance
- clone repositories into `[BC2X]/staging.ignore`, adjust directory names for later 
  handling and add wiki remotes.

  ```bash
  ROOT=/home/$USER/[path/to]/[BC2X]
  GALLERIES_STAGING=$ROOT/staging.ignore
  USE_PORT=[port#]

  git -C $GALLERIES_STAGING clone ssh://git@bc.g-node.org:$USE_PORT/G-Node/Info.wiki
  git -C $GALLERIES_STAGING clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Main.git
  mv $GALLERIES_STAGING/Main/ $GALLERIES_STAGING/main
  git -C $GALLERIES_STAGING/main remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Main.wiki.git
  git -C $GALLERIES_STAGING clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Posters.git
  mv -v $GALLERIES_STAGING/Posters/ $GALLERIES_STAGING/posters
  git -C $GALLERIES_STAGING/posters remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Posters.wiki.git
  git -C $GALLERIES_STAGING clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/InvitedTalks.git
  mv -v $GALLERIES_STAGING/InvitedTalks/ $GALLERIES_STAGING/invitedtalks
  git -C $GALLERIES_STAGING/invitedtalks remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/InvitedTalks.wiki.git
  git -C $GALLERIES_STAGING clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/ContributedTalks.git
  mv -v $GALLERIES_STAGING/ContributedTalks/ $GALLERIES_STAGING/contributedtalks
  git -C $GALLERIES_STAGING/contributedtalks remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/ContributedTalks.wiki.git
  git -C $GALLERIES_STAGING clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Workshops.git
  mv -v $GALLERIES_STAGING/Workshops/ $GALLERIES_STAGING/workshops
  git -C $GALLERIES_STAGING/workshops remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Workshops.wiki.git
  git -C $GALLERIES_STAGING clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Exhibition.git
  mv -v $GALLERIES_STAGING/Exhibition/ $GALLERIES_STAGING/exhibition
  git -C $GALLERIES_STAGING/exhibition remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/Exhibition.wiki.git
  git -C $GALLERIES_STAGING clone ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/ConferenceInformation.git
  mv -v $GALLERIES_STAGING/ConferenceInformation/ $GALLERIES_STAGING/conferenceinformation
  git -C $GALLERIES_STAGING/conferenceinformation remote add wiki ssh://git@bc.g-node.org:$USE_PORT/BernsteinConference/ConferenceInformation.wiki.git
  ```

CHECK IF THE FOLLOWING WORKS AS WELL

  ```bash
  ROOT=/home/$USER/[path/to]/[BC2X]
  GALLERIES_STAGING=$ROOT/staging.ignore
  USE_PORT=[port#]

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

- copy the necessary resources to the staging directories

  ```bash
  ROOT=/home/$USER/[path/to]/[BC2X]
  GALLERIES_ARCHIVE=$ROOT/galleries
  GALLERIES_STAGING=$ROOT/staging.ignore

  cp -v $GALLERIES_ARCHIVE/Info.wiki $GALLERIES_STAGING/Info.wiki -r
  cp -v $GALLERIES_ARCHIVE/main $GALLERIES_STAGING/main -r
  cp -v $GALLERIES_ARCHIVE/posters $GALLERIES_STAGING/posters -r
  ```

- adjust the following files to fit the current conference:
  - `$GALLERIES_STAGING/main/Home.md`
  - all files in `$GALLERIES_STAGING/Info.wiki`

- always add new or changed images and server templates not only to the appropriate 
  repositories and directories on the server, but also immediately to the `BC-latest` 
  directory.

- commit and upload. Fhe first push to the wiki of these repositories will require a 
  force push, since the wikis have been initialized on the server and contain
  unnecessary content.

  ```bash
  ROOT=/home/$USER/[path/to]/[BC2X]
  GALLERIES_ARCHIVE=$ROOT/galleries
  GALLERIES_STAGING=$ROOT/staging.ignore

  # Handle Info.wiki
  CURR_DIR=Info.wiki
  git -C $GALLERIES_STAGING/$CURR_DIR add --all
  git -C $GALLERIES_STAGING/$CURR_DIR commit -m "Updates"
  git -C $GALLERIES_STAGING/$CURR_DIR push origin master
  # copy all changes to the archive directory
  cp $GALLERIES_STAGING/$CURR_DIR -r $GALLERIES_ARCHIVE/$CURR_DIR

  # Handle Main
  CURR_DIR=main
  CURR_ARCHIVE=Main
  git -C $GALLERIES_STAGING/$CURR_DIR add --all
  git -C $GALLERIES_STAGING/$CURR_DIR commit -m "Updates"
  git -C $GALLERIES_STAGING/$CURR_DIR push origin master
  git -C $GALLERIES_STAGING/$CURR_DIR push wiki master -f
  # copy all changes to the archive directory
  cp $GALLERIES_STAGING/$CURR_DIR -r $GALLERIES_ARCHIVE/$CURR_ARCHIVE

  # Handle Posters
  CURR_DIR=posters
  CURR_ARCHIVE=Main
  git -C $GALLERIES_STAGING/$CURR_DIR add --all
  git -C $GALLERIES_STAGING/$CURR_DIR commit -m "Updates"
  git -C $GALLERIES_STAGING/$CURR_DIR push origin master
  git -C $GALLERIES_STAGING/$CURR_DIR push wiki master -f
  # copy all changes to the archive directory
  cp $GALLERIES_STAGING/$CURR_DIR -r $GALLERIES_ARCHIVE/$CURR_ARCHIVE

  # Handle Invited Talks
  CURR_DIR=invitedtalks
  CURR_ARCHIVE=InvitedTalks
  git -C $GALLERIES_STAGING/$CURR_DIR add --all
  git -C $GALLERIES_STAGING/$CURR_DIR commit -m "Updates"
  git -C $GALLERIES_STAGING/$CURR_DIR push origin master
  git -C $GALLERIES_STAGING/$CURR_DIR push wiki master -f
  # copy all changes to the archive directory
  cp $GALLERIES_STAGING/$CURR_DIR -r $GALLERIES_ARCHIVE/$CURR_ARCHIVE

  # Handle Contributed Talks
  CURR_DIR=contributedtalks
  CURR_ARCHIVE=ContributedTalks
  git -C $GALLERIES_STAGING/$CURR_DIR add --all
  git -C $GALLERIES_STAGING/$CURR_DIR commit -m "Updates"
  git -C $GALLERIES_STAGING/$CURR_DIR push origin master
  git -C $GALLERIES_STAGING/$CURR_DIR push wiki master -f
  # copy all changes to the archive directory
  cp $GALLERIES_STAGING/$CURR_DIR -r $GALLERIES_ARCHIVE/$CURR_ARCHIVE

  # Handle workshops
  CURR_DIR=workshops
  CURR_ARCHIVE=Workshops
  git -C $GALLERIES_STAGING/$CURR_DIR add --all
  git -C $GALLERIES_STAGING/$CURR_DIR commit -m "Updates"
  git -C $GALLERIES_STAGING/$CURR_DIR push origin master
  git -C $GALLERIES_STAGING/$CURR_DIR push wiki master -f
  # copy all changes to the archive directory
  cp $GALLERIES_STAGING/$CURR_DIR -r $GALLERIES_ARCHIVE/$CURR_ARCHIVE

  # Handle Exhibition
  CURR_DIR=exhibition
  CURR_ARCHIVE=Exhibition
  git -C $GALLERIES_STAGING/$CURR_DIR add --all
  git -C $GALLERIES_STAGING/$CURR_DIR commit -m "Updates"
  git -C $GALLERIES_STAGING/$CURR_DIR push origin master
  git -C $GALLERIES_STAGING/$CURR_DIR push wiki master -f
  # copy all changes to the archive directory
  cp $GALLERIES_STAGING/$CURR_DIR -r $GALLERIES_ARCHIVE/$CURR_ARCHIVE

  # Handle Conference Information
  CURR_DIR=conferenceinformation
  CURR_ARCHIVE=ConferenceInformation
  git -C $GALLERIES_STAGING/$CURR_DIR add --all
  git -C $GALLERIES_STAGING/$CURR_DIR commit -m "Updates"
  git -C $GALLERIES_STAGING/$CURR_DIR push origin master
  git -C $GALLERIES_STAGING/$CURR_DIR push wiki master -f
  # copy all changes to the archive directory
  cp $GALLERIES_STAGING/$CURR_DIR -r $GALLERIES_ARCHIVE/$CURR_ARCHIVE
  ```

TODO test local bash function for cleaner script

  ```bash
  ROOT=/home/$USER/[path/to]/[BC2X]
  GALLERIES_ARCHIVE=$ROOT/galleries
  GALLERIES_STAGING=$ROOT/staging.ignore

  alias galleryupforce='function __galleryupforce() {
    echo "Handling $CURR_ARCHIVE";
    git -C $GALLERIES_STAGING/$CURR_DIR add --all;
    git -C $GALLERIES_STAGING/$CURR_DIR commit -m "Updates";
    git -C $GALLERIES_STAGING/$CURR_DIR push origin master;
    git -C $GALLERIES_STAGING/$CURR_DIR push wiki master -f;
    echo "Copy data to archive";
    cp $GALLERIES_STAGING/$CURR_DIR -r $GALLERIES_ARCHIVE/$CURR_ARCHIVE;
  }; __galleryupforce'

  # Handle Info.wiki
  CURR_DIR=Info.wiki
  git -C $GALLERIES_STAGING/$CURR_DIR add --all
  git -C $GALLERIES_STAGING/$CURR_DIR commit -m "Updates"
  git -C $GALLERIES_STAGING/$CURR_DIR push origin master
  # copy all changes to the archive directory
  cp $GALLERIES_STAGING/$CURR_DIR -r $GALLERIES_ARCHIVE/$CURR_DIR

  # Handle Main
  CURR_DIR=main
  CURR_ARCHIVE=Main
  galleryup

  # Handle Posters
  CURR_DIR=posters
  CURR_ARCHIVE=Main
  galleryupforce

  # Handle Invited Talks
  CURR_DIR=invitedtalks
  CURR_ARCHIVE=InvitedTalks
  galleryupforce

  # Handle Contributed Talks
  CURR_DIR=contributedtalks
  CURR_ARCHIVE=ContributedTalks
  galleryupforce

  # Handle workshops
  CURR_DIR=workshops
  CURR_ARCHIVE=Workshops
  galleryupforce

  # Handle Exhibition
  CURR_DIR=exhibition
  CURR_ARCHIVE=Exhibition
  galleryupforce

  # Handle Conference Information
  CURR_DIR=conferenceinformation
  CURR_ARCHIVE=ConferenceInformation
  galleryupforce
  ```

- add the initial csv file to the `[BC2X]/rawdata` folder

- add all discussion notes, timetable notes, emails on the subject, email templates, 
  image or banner zip files to the `[BC2X]/notes` directory for easy review in the next 
  year.

- after running the scripts to create the poster gallery repositories the following 
  commits and pushes all changes.

  ```bash
  ROOT=/home/$USER/[path/to]/[BC2X]
  GALLERIES_ARCHIVE=$ROOT/galleries
  GALLERIES_STAGING=$ROOT/staging.ignore

  alias galleryup='function __galleryup() {
    echo "Handling $CURR_ARCHIVE";
    git -C $GALLERIES_STAGING/$CURR_DIR add --all;
    git -C $GALLERIES_STAGING/$CURR_DIR commit -m "Updates";
    git -C $GALLERIES_STAGING/$CURR_DIR push origin master;
    git -C $GALLERIES_STAGING/$CURR_DIR push wiki master;
    echo "Copy data to archive";
    cp $GALLERIES_STAGING/$CURR_DIR -r $GALLERIES_ARCHIVE/$CURR_ARCHIVE;
  }; __galleryup'

  # Handle Main
  CURR_DIR=main
  CURR_ARCHIVE=Main
  galleryup

  # Handle Posters
  CURR_DIR=posters
  CURR_ARCHIVE=Main
  galleryup

  # Handle Invited Talks
  CURR_DIR=invitedtalks
  CURR_ARCHIVE=InvitedTalks
  galleryup

  # Handle Contributed Talks
  CURR_DIR=contributedtalks
  CURR_ARCHIVE=ContributedTalks
  galleryup

  # Handle workshops
  CURR_DIR=workshops
  CURR_ARCHIVE=Workshops
  galleryup

  # Handle Exhibition
  CURR_DIR=exhibition
  CURR_ARCHIVE=Exhibition
  galleryup

  # Handle Conference Information
  CURR_DIR=conferenceinformation
  CURR_ARCHIVE=ConferenceInformation
  galleryup
  ```
