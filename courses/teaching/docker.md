# Docker

## Docker general usage

- create a docker build file named `Dockerfile` in the root of the project
- run a docker build from the root of the project containing the docker build file

- build a container with the source code found at a provided directory

    docker build -t [containername:label] [source_dir]

- the configuration of a built docker container can be reviewed by using

        docker inspect [container]

- start a container in detached mode, remove it when it is stopped.

    # -d ... detached mode
    # -it ... interactive mode, access container at runtime and keep running after start script has run
    # --rm ...remove container when stopped
    docker run --rm -dit [container]

- a built docker container can be run and accessed using the command. `-it` means interactive, `--entrypoint /bin/bash` opens the shell of the container giving cli access.
- enter a container at startup to look around for any setup problems. This will not start the service since the `entrypoint` is overwritten by executing `/bin/bash`. The container can be left by typing in `exit`.

    docker run -t --entrypoint=/bin/bash [container]

- start a detached container with a specified runtime name

    docker run -d --name [someName] [container]

- stop a running container

    docker stop [container runtime name]

- list running containers

    # -a ... lists also the stopped containers
    docker ps [-a]

- list docker images

    # -a ... lists all containers
    docker images [-a]

- remove a docker container container

    docker rm [container]

- remove all stopped containers

    docker rm $(docker ps -a -q)

- remove an image

    docker rmi [image]

- access log of a running container and follow

    docker logs -f [container runtime name]

- access a running container in interactive mode

    docker exec -it [container runtime name] /bin/bash

- list docker volumes

    docker volume ls

- remove a docker volume

    docker volume rm [volumeName]

- mounting directories from the docker container to the outside and vice versa; can be specified multiple times
- NOTE: -v will always overwrite everything thats in the container target directory; it is actually not an overwrite, but the directory from the outside will be mounted "over" the directory inside the container. as long as it is mounted, the container directory is not removed, but not accessible.

    docker run -it -v /path/on/host/:/path/on/container [container]

- connect container and host ports; make sure exposing a port is really necessary before you do it!

    docker run -it -p [host port]:[container port] [container]


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

# docker installation

## Ubuntu linux

Install docker using `apt`:

    sudo apt install docker.io

With this docker can only be run as root user. Add your user to the docker usergroup to be able to run it as well.

    sudo usermod -a -G docker $USER

This will append (`-a`) `$USER` to the usergroup (`-G`) `docker`. The current usergroups can be found and checked in `/etc/group`.
It will need a re-login for the changes to take effect.

https://www.linux.com/learn/intro-to-linux/2017/11/how-install-and-use-docker-linux
