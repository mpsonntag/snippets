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
