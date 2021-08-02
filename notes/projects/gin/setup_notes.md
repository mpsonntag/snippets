# in-house-gin

This repository documents how to set up a custom instance of the [GIN](https://gin.g-node.org) G-Node infrastructure 
service.

## Setup prerequisites and preparations

The setup has been tried and tested on Linux based Operating systems.

`docker` and `docker-compose` are required.

To smoothly work with a docker deployment, the following groups and users should be set up.

### System preparations
- prepare dedicated deployment group e.g. "ginservice" group if it does not exist
- create a dedicated deployment user e.g. "ginuser"
- note deployment group and user IDs for the `docker-compose.yml` file.
- for any further setup, all required directories and files should be created with this user/group as owners.
- make sure to add all users that are running docker-compose or need access to project files to the docker and deploy groups.