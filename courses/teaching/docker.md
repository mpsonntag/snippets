# Docker

## Docker general usage

Build a container with the source code found at a provided directory

    docker build -t [containername:label] [source_dir]

Start a container in detached mode, remove it when it is stopped.

    docker run --rm -dit [container]

List running containers

    # -a ... lists also the stopped containers
    docker ps [-a]

List images

    # -a ... lists all containers
    docker images [-a]

Remove container

    docker rm [container]

Remove all stopped containers

    docker rm $(docker ps -a -q)

Remove image

    docker rmi [image]

Access log of a running container and follow

    docker logs -f [container]

Access a running container in interactive mode

    docker exec -it [container] /bin/bash

List docker volumes

    docker volume ls

Remove volume

    docker volume rm [volumeName]

### Thorough cleanup

docker can be a bit messy with the images and containers it leaves behind. Normal cleanup with the `rm` command might not be enough.

    # cleanup unused docker containers
    docker ps -aq --no-trunc -f status=exited | xargs docker rm

    # cleanup unused docker images
    docker images -f "dangling=true" -q | xargs docker rmi


### Various notes on docker usage

By default docker (images, containers, volumes) reside in `/var/lib/docker`. Keep an eye on the size of this folder and migrate if the space runs out.

https://blog.adriel.co.nz/2018/01/25/change-docker-data-directory-in-debian-jessie/ 

When having an external storage location for files via ` -v /external:/internal`, the content of `/external` is mounted into the docker volume `/internal`, which resides in `/var/lib/docker`.


## Docker compose

Start docker containers defined in a `docker-compose.yml` file. This file has to reside in the directory where the following command is executed. Any `.env` file providing environment variables for the services have to reside in the same directory as well.

    # -p ... defines a name for the started containers.
    #    ... by default, its the directory name (?)
    # -d ... starts the containers in detached mode 
    docker-compose -p [projectname] up -d

## Notes
- when using volumes, the directories on the host system need to be assigned either to a user that is in the user group or should be assigned to the docker group.
