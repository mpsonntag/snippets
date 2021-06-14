# Bernstein conference poster gallery

## Roadmap

- decide on domain
  - should be something generic for both poster gallery and uploader
  - currently bc20.g-node.org and bc20-posters.g-node.org
  - register these domains and switch this in the domains
- decide if previous conference posters should still be available
- on the current system we already have registered users
  - would need to prune these users or setup the server anew
  - only users that have registered should be able to sign up
- the page is running again
  - any design changes?
  - any changes in data structure?
    - invited talks, contributed talks, posters, workshops?
    - topics, posters, talks?
    - additional information?
    - same format with vimeo, hopin, etc?
    - poster categories?
    - new banners?

workflow on site

- bc-admins: send emails to posters - code for upload
- bc-posters: people upload poster+description - can be updated whenever

- bc-posters: conf-admins update email hash list
- conf-gogs: registration checks email hash from bc-posters
- bc-admins: google sheet with poster information, hopin, vimeo link
- bc-admins: google sheet with workshop info
- gnode: save google sheets to tsvs -> run BC20 makefile to create and upload to bc-gogs

- people register: 


- different logins:
  - gca-web
  - juelich scibo (video upload)
  - bc-posters (upload-code)
  - bc-online (checked via email hash from bc-posters)
  - hopin
  - forgot sthg?

## Notes
https://github.com/G-Node/BC20

3 submodules
- uploader
- gin instance templates


on gin
https://gin.g-node.org/G-Node/gin-bc20/src/master

this repo contains the configs and docker files as well as the BC branding

on github.com/gin ... bc20 branch -> this contains noe commit to support the whitelist email changes

  - could use gogs master branch since it now contains default whitelisting
  - but fetches hashes so we probably continue using the gogs/bc20 branch

on gin: the G-Node/bc20data
  ... contains the raw data that is used to create the markdown files that are used to displayed during the conference

https://github.com/G-Node/BC20

contains a makefile that does all the work


WORKFLOW:

spreadsheet from BCOS

makefile
- fetches data from online spreadsheet and writes data to tsv
- then tsv to json
- with the GCA client -> DL abstract to json

on machine bc20.g-node.org

directory /data
directory /gin-bc20 ... contains docker volumes and docker config files ... this is a copy of the files on gin.g-node.org/G-node/gin-bc20

msonntag ... admin
bc20

repos on bc20.g-node.org
- Invited Talks ... https://bc20.g-node.org/BernsteinConference2020/InvitedTalks/wiki ... rendered


locally clone these repositories, add the https://bc20.g-node.org/BernsteinConference2020/InvitedTalks.wiki as remote and push changes to both repos so that the wiki is always properly rendered


locally
- clone github: BC20
- fetch all subrepositories
- create `galleries` folder in the root of the repo
- git fetch all repositories from b20 e.g. 

scripts

tojson.py
mergeabstracts.py ... takes tsv json and abstracts json ... figures still hosted from GCA, just links to the figures are added 
  - adds vimeo, hopin links, 
mkgalleries.py ... for everything except workshops
  - index text came from BCOS
  - 1 markdown file for each poster - uses the previously created json files
  - also created the various index pages
  - WITHDRAWN ... 193 ... id of the withdrawn abstract
mkworkshopgallery ... bit different 


templates?


examples

git clone git@bc20.g-node.org:/BernsteinConference2020/Posters galleries/Posters
cd galleries/Posters
git remote add wiki git@bc20.g-node.org:/BernsteinConference2020/Posters.wiki
git fetch --all



templates

org/home.tmpl ... javascript redirect ... to avoid users seeing the repositories directly but getting redirected to the wiki pages instead


gin.g-node.org/g-node/bc20data ... startpage.md & landing-page.md are just infos from BCOS, not actively used anywhere


## Setup notes

Uploaderserver and gin-poster server need to be on the same machine since the posters that people upload via the uploaderserver are linked via the poster server if I understand the setup correctly.

Currently the Uploader service has to be up and running and the email address of the first admin user has to be in the hosted emailwhitelist before the gogs service can be set up and an admin created.

To manually create a gogs user with admin privileges after the gogs service has been set up:

```bash
docker exec -it posters_web_1 /bin/bash
su git
./gogs admin create-user --name tmpuser --password tmppassword --admin --email email@example.com
```

### Server prerequisites

Setup and prepare the server as described in opsdocs:admin/server-setup.md.
Setup users and groups analogous to the normal gin setup as described in opsdocs:dev/gin-setup.md.

### Server setup
- create storage locations

```bash
PROJ_ROOT=/data/dev/posters

sudo mkdir -vp $PROJ_ROOT/volumes
sudo mkdir -vp $PROJ_ROOT/data/posters-data
sudo mkdir -vp $PROJ_ROOT/data/posters-tmp
sudo mkdir -vp $PROJ_ROOT/data/posters-postgresdb
```

- clone the repo G-Node/gin-bc20 from gin.g-node.org and copy the contents (minus the git directory) to $PROJ_ROOT directory on the server.
- update the docker-compose file 
  - to match the appropriate docker containers
    - gnode/gin-web:posters
    - gnode/bc20-uploader:latest
  - to match the ids of the local `gin` user and `deploy` group; use `getent passwd` and `getent groups` to find the appropriate ids.
  - make sure the used IP addresses do not overlap with already running docker containers
  - make sure to use ssh ports that do not overlap with any other ssh port in use e.g. -> needs to be adjusted in the gin client later on as well
    - "141.84.41.217:2323:22"
  - make sure the local directories match the local setup
    - ./data/posters-data
    - ./data/posters-tmp
    - ./data/posters-postgresdb
  - change aliases to
    - posterginweb
    - posterpgres

- rename `$PROJ_ROOT/config/gogs/conf/app.ini` to `reference_app.ini` to avoid it being overwritten after initializing the docker container.

- change ownership of the whole `$PROJ_ROOT` directory to the appropriate user and group; also make sure people in the same group may edit

    sudo chown -R $DEPLOY_USER:$DEPLOY_GROUP $PROJ_ROOT
    sudo chmod g+w $PROJ_ROOT -R

- pull all required docker containers (db, gin-web:bc20, bc20-uploader)

    cd $PROJ_ROOT
    docker-compose pull

- add apache configuration files and run certbot for these files - the configuration might need to be a bit different on the dev server compared to a live machine.

- create apache configurations for bc20 and bc20-posters in /etc/apache2/sites-available

- create certbot certificates (certbot command might differ depending on OS)

    # Stop apache
    sudo systemctl stop apache2
    sudo certbot certonly
    # Manually select apache (1); Make sure to use the same domain as specified in the apache2 config files 
    # add domain as appropriate: bc20.dev.g-node.org
    # Run the same setup again for domain: bc20-posters.dev.g-node.org
    # Check that both certificates have been added:
    sudo ls -lart /etc/letsencrypt/live/
    # Start apache
    sudo systemctl start apache2

- Chrome needs a restart to properly accept renewed certificates.

- enable bc20.dev.g-node.org via apache2

    sudo a2ensite bc20.dev.g-node.org.conf
    sudo systemctl reload apache2

- run the setup procedure for gin-web:b20; follow the procedure in the [dev:gin-web setup description](../dev/gin-setup.md) with the following changes

- fetch all required containers from the docker-gin directory

        cd $DIR_GINROOT/gin-dockerfile
        docker-compose pull

- prepare the postgres database container for the first gin setup

```bash
docker-compose up -d db
docker exec -it posters_db_1 /bin/bash
su -l postgres
createuser -P gin
# enter password for new role and save it before using it - e.g. somethingSecret
# note this password, it will later be used on the initial gin setup page
createdb -O gin gin
exit
exit
```

- launch gin-web docker container

        docker-compose up web

- start the gin setup via the browser at bc20.dev.g-node.org
    - db:               postgres
    - host:             posterpgres:5432
    - user:             gin
    - password:         [used during database setup]
    - database name:    gin
    - app name:         Bernstein Poster Gallery
    - repo root:        as defined in docker-compose on the container side e.g. /data/repos
    - domain:           bc20.dev.g-node.org
    - create an administration user; do not use 'admin'; if the database is restored from the live server, this user will be overwritten.

- NOTE: DO NOT change the application URL during the initial setup - otherwise the default admin cannot be properly set up

- save; this might redirect to an error page, but this is inconsequential
- check that the page is running at bc20.dev.g-node.org
- on the dev server, stop all containers

    ```
    cd $DIR_GINROOT/gin-dockerfile
    docker-compose down
    ```


### Build poster gallery specific gin-web container from source

If the container is not already built and available, locally build it from source,
push it to dockerhub and pull on the server that is hosting the container.

```bash
git clone git@github.com:G-Node/gogs.git
cd gogs
git fetch --all
# Checkout the poster gallery specific branch
git checkout bc20
# build the docker images
docker build -t gnode/gin-web:posters .
# push the built container
docker push gnode/gin-web:posters
```

### Poster upload codes workflow

[finetune description]

To create the poster upload codes run the `mkuploadcodes.py` script in the G-Node/BC20 repo. The script requires a json file with all posters. It creates a json file with all posters including the upload codes. These upload codes have to be entered into the posters tsv file. The resulting posters.json file from this tsv file has to be put in the config folder of the uploader server.

The required uploadersalt file is found in gin.g-node.org/G-Node/gin-bc20.
The script requires a poster.json file that has been created via the `tojson.py` script from the poster.tsv file.

### From tsv to gallery

The github repository G-Node/BC20 contains all scripts required to create and upload the poster gallery pages. Check the `makefile` at the root of the repository. It can be run to create and upload all files in one go.

The following describes how to run the individual steps manually:

#### Create the raw json files from tsv

- running the following creates a "raw" `posters.json` file
```bash
python tojson.py posters.tsv
```

- running the following creates a "raw" `workshops.json` file
```bash
python tojson.py workshops.tsv
```

# Config files

## Docker file (DEV server)

version: '2.4'
services:

  web:
    image: gnode/gin-web:bc20
    volumes:
      - ./config/gogs:/custom:rw
      - ./data/posters-data:/data/repos:rw
      - ./volumes/posterweb:/data:rw
      - gintmp:/data/tmp:rw
    restart: always
    environment:
      - PUID=999      # 'gin' user id
      - PGID=2139     # 'gindeploy' group id
      - GOGS_CUSTOM=/custom
    ports:
      - "2323:22"
    networks:
      net:
        ipv4_address: 172.29.0.10
        aliases:
          - posterginweb
    depends_on:
      - db

  uploader:
    image: gnode/bc20-uploader:latest
    entrypoint: ["/bin/uploader", "-config", "/srvcfg/config"]
    volumes:
      - ./config/uploader:/srvcfg:ro
      - ./volumes/uploader:/uploads:rw
    restart: always
    networks:
      net:
        ipv4_address: 172.29.0.20
        aliases:
          - uploader
  db:
    image: postgres:11
    env_file: ./config/postgres/pgressecrets.env
    restart: always
    networks:
      net:
        aliases:
          - posterpgres
    volumes:
      - ./data/posters-postgresdb:/var/lib/postgresql/data:rw

volumes:
  gintmp:

networks:
  net:
    ipam:
      driver: default
      config:
        - subnet: 172.29.0.0/16
          gateway: 172.29.0.254


## Apache config files (DEV Server)
