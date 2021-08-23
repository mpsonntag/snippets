
## Installation requirements

Adhere to the installation instructions in the server-setup.md file.

### Required users and groups

gnode, deploy

### Required packages

apache2, certbot, docker, docker-compose

### Required directories

PROJ_ROOT=/data/dev/posters

sudo mkdir -vp $PROJ_ROOT/volumes
sudo mkdir -vp $PROJ_ROOT/data/posters-data
sudo mkdir -vp $PROJ_ROOT/data/posters-tmp
sudo mkdir -vp $PROJ_ROOT/data/posters-postgresdb



