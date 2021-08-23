
## Installation requirements

Adhere to the installation instructions in the server-setup.md file.

### Required users and groups

gnode, deploy

### Required packages

apache2, certbot, docker, docker-compose

### Required directories

```bash
PROJ_ROOT=/data/dev/posters

mkdir -vp $PROJ_ROOT/volumes/posterweb
mkdir -vp $PROJ_ROOT/volumes/uploader
mkdir -vp $PROJ_ROOT/data/posters-data
mkdir -vp $PROJ_ROOT/data/posters-tmp
mkdir -vp $PROJ_ROOT/data/posters-postgresdb
```

- clone the repo G-Node/gin-bc20 from gin.g-node.org and copy the contents (minus the git directory) to $PROJ_ROOT directory on the server.
- update the `.env` file content
- update the `docker-compose.yml` file 
  - to match the appropriate docker containers e.g.:
    - gnode/gin-web:posters
    - gnode/bc20-uploader:latest
  - to match the ids of the local `gnode` user and `deploy` group; use `getent passwd` and `getent groups` to find the appropriate ids.
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

- change ownership of the whole `$PROJ_ROOT` directory to the appropriate user and group; also make sure people that may want to edit files are in the same group
```bash
sudo chown -R $DEPLOY_USER:$DEPLOY_GROUP $PROJ_ROOT
sudo chmod g+w $PROJ_ROOT -R
```


