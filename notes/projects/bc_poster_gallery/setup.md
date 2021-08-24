
## Installation requirements

Adhere to the installation instructions in the server-setup.md file.

### Required users and groups

gnode, deploy

### Required packages

apache2, certbot, docker, docker-compose

### Required registered domains

The following domains need to be registered before the services can be deployed and https certificates issued via certbot.

bc.g-node.org
posters.bc.g-node.org

### Set up apache configurations and https certificates

- Set up apache configuration files for the two domains listed above.
- Run certbot for both domains once both configurations have been enabled for apache.
- Again for details check the general installation instructions in server-setup.md

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
- on the dev server, stop all containers
```bash
cd $PROJ_ROOT
docker-compose down
```

- modify the `$PROJ_ROOT/config/gogs/config/app.ini` to mimic the `reference_app.ini`. To ensure custom templates and assets are properly loaded, the ini file's [server] section should contain the lines:
```
  LOAD_ASSETS_FROM_DISK = true
  STATIC_ROOT_PATH = /custom/
```

- copy the latest page templates from https://gin.g-node.org/G-Node/gin-bc20 to `$PROJ_ROOT/config/templates`
- update the custom templates and images in `$PROJ_ROOT/config/templates` so links, times and dates match the 

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
  - InvitedTalks
  - ContributedTalks
  - Posters
  - Workshops
  - Main
  - create the first wiki page for all repos via the web interface

