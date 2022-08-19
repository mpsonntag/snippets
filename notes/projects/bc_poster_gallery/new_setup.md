## New repositories and pipelines to handle and update the Bernstein Conference Poster Gallery

### Current resources

BC20            ... github.com:G-Node/BC20
                    ... integrate into new BC-Gallery repository on GIN and archive
BC20data        ... gin.g-node.org:G-Node/BC20data
                    ... integrate into new BC-Gallery repository on GIN and archive
gin             ... gin.g-node.org:G-Node/gin-bc20
                    ... integrate into new BC-Gallery repository on GIN and archive
BC20-uploader   ... github.com:G-Node/BC20-uploader
                    ... keep as is
GCA-Python      ... github.com:G-Node/GCA-Python
                    ... keep as is
gogs            ... github.com:G-Node/gogs ... webgallery
                    ... keep as is

### New resources

BC20-uploader   ... github.com:G-Node/BC20-uploader
GCA-Python      ... github.com:G-Node/GCA-Python
gogs            ... github.com:G-Node/gogs
BC-Gallery      ... gin.g-node.org:G-Node/BC-Gallery

BC-Gallery structure
|- README.md
|- setup-notes.md
|- .gitignore
|- scripts\
|- BC-latest\
|  |- server-resources
|  |  |- README.md
|  |  |- .env
|  |  |- uploadersalt
|  |  |- docker-compose.yml
|  |  |- config\
|  |  |  |- gogs\
|  |  |  |  |- conf\
|  |  |  |  |  - app.ini
|  |  |  |  |- public\
|  |  |  |  |  |- *.jpg/.png
|  |  |  |  |- templates\
|  |  |  |  |  |- latest-template-tree\*
|  |  |  |- postgres\
|  |  |  |  |- postgressecrets.env
|  |  |  |- uploader\
|  |  |  |  |- config
|  |- galleries\
|  |  |- Info.wiki\
|  |  |  |- Datenschutz.md
|  |  |  |- Home.md
|  |  |  |- 'Terms of Use.md'
|  |  |  |- about.md
|  |  |  |- contact.md
|  |  |  |- imprint.md
|  |  |- main\
|  |  |  |- main.md
|  |  |  |- img\
|  |  |  |  |- *.jpg
|  |  |  |- posters\
|  |  |  |  |- assets\
|  |  |  |  |  |- *.jpg|.png
|  |  |  |  |- banners\
|  |  |  |  |  |- *.jpg|.png
|- BC20\
|  |- docker-logs\
|  |- galleries\
|  |- notes\
|  |- rawdata\
|  |- server-resources\
|- BC21\
|  ... as above 
|- BC22\
|  ... as above 

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
