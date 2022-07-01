# Docker

## Docker general usage

- create a docker build file named `Dockerfile` in the root of the project
- run a docker build from the root of the project containing the docker build file

- build a container with the source code found at a provided directory

    docker build -t [containername:label] [source_dir]

- to ensure a full, clean build use the `--no-cache` and `--pull` flags to ensure no stale dependent images are used

    docker build -t --no-cache --pull [containername:label] [source_dir]

- the configuration of a built docker container can be reviewed by using

        docker inspect [container]

- the configuration can be filtered to print only content of interest by using the "-f" flag for running containers or docker images

  ```bash
  # e.g. filter for the IP address a container is running in
  docker inspect -f "{{ .NetworkSettings.Networks.gcanet.IPAddress }}" [DOCKER_CONTAINER_NAME]
  # find out when the image of a running container was created
  docker inspect -f "{{ .Created }}" [DOCKER_IMAGE_org/name:tag]
  ```

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

- connect container and host ports; make sure exposing a port is really necessary before you do it!

    docker run -it -p [host port]:[container port] [container]


## Docker volumes and file handling
- mounting directories from the docker container to the outside and vice versa; can be specified multiple times

        docker run -it -v /path/on/host/:/path/on/container [container]

- NOTE: `-v` will always overwrite everything thats in the container target directory; it is actually not an overwrite, but the directory from the outside will be mounted "over" the directory inside the container. as long as it is mounted, the container directory is not removed, but not accessible.

- NOTE: when using volumes, the directories on the host system need to be assigned either to a user that is in the user group or should be assigned to the docker group.

- copy files from a running docker instance

        docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-
        docker cp [OPTIONS] SRC_PATH|- CONTAINER:DEST_PATH

- NOTE: if frequently building docker containers, make sure that the docker volumes path is located at a partition that has enough space.
    Find out where the current location of the docker volumes (`Docker Root Dir`) is via `docker info` and then checking the partition location via `df -T [path]`.

- ALSO NOTE: that with the following command a lot of space can be freed up from currently unused resources. It will delete ALL UNUSED VOLUMES, so if there is a shut down container lying around maps to the outside and has usefull files still, be aware, that these data will be removed as well!
    Space can be cleaned up via the command `docker system prune` that removes all unused docker resources.

## Docker networks

- When multiple docker instances are running, they can communicate with each other via a docker network

        docker network create someNetworkName

- Now start two different named docker instances that join the created network. By naming them, each
  docker instance can be address by any other docker instance via its name

        docker run -dit --rm --name appA --network=someNetworkName applicationA:latest
        docker run -dit --rm --name appB --network=someNetworkName applicationB:latest

- When we access one container, we can check, if the other app is available

        docker exec -it appA /bin/bash
        #-- check if appB appears in the list of known hosts
        cat /etc/hosts
        #-- or even ping the application by name
        ping appB


### Docker cleanup

docker can be a bit messy with the images and containers it leaves behind. Normal cleanup with the `rm` command might not be enough.

List all exited containers

    docker ps -aq -f status=exited

Remove stopped containers

    docker ps -aq --no-trunc -f status=exited | xargs docker rm

Cleanup dangling images

    docker images -f "dangling=true" -q | xargs docker rmi

Remove unused data

    docker system prune

Cleanup pipe/script

    docker ps -aq --no-trunc -f status=exited | xargs docker rm
    docker images -f "dangling=true" -q | xargs docker rmi
    docker system prune


### Publishing a docker container
- [publish a docker container](https://ropenscilabs.github.io/r-docker-tutorial/04-Dockerhub.html)

- create a repo on dockerhub
- locally docker login
- create a tag from the to be published image - ideally use tagname "latest" if you want a docker pull to be easy.

        docker tag [imageID] [dockerhubUsername]/[reponame]:[tagname]

- push tag to dockerhub
  
        docker push [dockerhubUsername]/[reponame]:[tagname] 


### Various notes on docker usage

By default docker (images, containers, volumes) reside in `/var/lib/docker`. Keep an eye on the size of this folder and migrate if the space runs out.

https://blog.adriel.co.nz/2018/01/25/change-docker-data-directory-in-debian-jessie/ 

When having an external storage location for files via ` -v /external:/internal`, the content of `/external` is mounted into the docker volume `/internal`, which resides in `/var/lib/docker`.


### Docker logs

By default docker logs can be found at `/var/lib/docker/containers/[container-id]/[container-id]-json.log`. If the docker storage has been moved from the default location to another due to space issues, the logfiles will be found there. They can be easily identified for copy via the docker config:

```bash
docker inspect [container_name] | grep LogPath
```

Docker writes `json` files by default; the format can be checked using the command 
```
docker info --format '{{.LoggingDriver}}'
# or
docker info | grep Logging
```

Check the size of these log files e.g. with tree
```tree --du -h /var/lib/docker/containers```


## Docker compose

Start docker containers defined in a `docker-compose.yml` file. This file has to reside in the directory where the following command is executed. Any `.env` file providing environment variables for the services have to reside in the same directory as well.

    # -p ... defines a name for the started containers.
    #    ... by default, its the directory name (?)
    # -d ... starts the containers in detached mode 
    docker-compose -p [projectname] up -d

### Docker compose installation:

https://docs.docker.com/compose/install/

Usually install to `/usr/local/bin`

    sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose


### docker compose usage

All commands work from the directory that contains the `docker-compose.yml` file.

- pull all docker containers specified in the docker-compose file. fetches the `latest` tag by default.

        docker-compose pull

- pull only a specific container, if more containers are specified in the compose file.

        docker-compose pull [container name]

- start docker via docker-compose

        # start all projects; detach from processes after start. leaving it running in the background
        docker-compose -d up

- start only a specific container, if more containers are specified in the compose file.

        # again start and detach from process
        docker-compoase -d up [container name]


# Docker installation

## Ubuntu linux

Install docker using `apt`:

    sudo apt install docker.io

With this docker can only be run as root user. Add your user to the docker usergroup to be able to run it as well.

    sudo usermod -a -G docker $USER

This will append (`-a`) `$USER` to the usergroup (`-G`) `docker`. The current usergroups can be found and checked in `/etc/group`.
It will need a re-login for the changes to take effect.

https://www.linux.com/learn/intro-to-linux/2017/11/how-install-and-use-docker-linux
