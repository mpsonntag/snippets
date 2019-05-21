# Networking

IP ... internet protocol
inter network communication protocol to enable communication between
two defined addresses. IPv4 addresses.

UDP ... User datagram protocol
inter network data transfer protocol. carries besides the data itself only 
checksum and the address of the receiver. does not provide support against data loss.

Ports ... 
logical construct to enable multiple different gate points at a specific address
for different services. can also be seen as an endpoint of a communication 
channel. at an endpoint 16bit unsigned integer number of ports can be
assigned, ranging 0-65535. Depending on the protocol ports may be reserved and
should not be used e.g. port 0 for TCP

TCP ... Transmission control protocol


DAV

WebDAV

SMTP

HTTP

HTTPS

TLS

SSH


TTY ... teletypewriter - driver to provide connection between kernel and a shell
"In unix terminology, a tty is a particular kind of device file which implements a 
number of additional commands (ioctls) beyond read and write. In its most common meaning, 
terminal is synonymous with tty." [from here](https://unix.stackexchange.com/a/4132)

A tty provides session management, programm handling (signals for starting, stopping, 
killing, etc; e.g. SIGTERM, SIGKILL, etc), IO operations in the shell ("line disciplines") 
and terminal display handling e.g. vim file content display.

[tty introduction](http://www.linusakesson.net/programming/tty/index.php)


# Linux commands and paths

... that are good to know and understand...

## Shell environment

Display all environmental variables

    env

## Job control

Starting an application in the background and get the command line back can
be done by using `&` after the command.

    gedit &

To see which jobs are running in the background of the shell, use `jobs`

    # example of our above case
    jobs
    # would print
    [1]+  Running                 gedit &

Bring a background job to the front by using `fg`

    # in our example
    fg "%gedit"

A running job blocking the shell can be stopped by using `ctrl+z`

    # jobs would show the following in our example
    [1]+  Stopped                 gedit

A stopped job can be restarted by `fg` or by `bg` (background)

    # in our example gedit would now run as a job in the background
    bg "%gedit"


## Process commands

`ps` ... display running processes

    # plain ps displays the running processes of the current user
    ps

    # ps -aux displays all running processes
    ps -aux

Processes can be found in `/proc/$PID`


## Terminal commands

`/dev/pts` holds all the currently open terminals

To identify the currently open terminal type `tty`.


## User and permission commands

`useradd` ... add a user

`groupadd` ... add a user to a group

`chown` ... change the owner or a file or directory

`chmod` ... change file permissions

`sudo` ... execute commands as a different user. default user is root

`su` ... switch to a different user; can also run commands w/o opening a new shell

    # switch to a different user, opening a new shell, stop with 'exit'
    su - [username]

    # run a command as specific user; requires password
    # -m preserves the current environment except for $PATH
    # -c invokes running a command
    su [username] -m -c 'ls -la'

`passwd` ... change password

## File commands

Copy command

        # -r ... recursive, -u update target only, -L resolve symbolic links, v ... verbose
        cp -vruL [source_directory] [target_directory]

Get the name of a file in a path

        basename [path]

Get the directory of a file in a path

        dirname [path]

watch a file or a command and refresh the view

    # e.g. the content of a file
    watch tail file.log
    # e.g. running docker containers
    watch docker ps

directory disk usage; display estimated size of a directory

    # s ... print only total size
    # h ... print human friendly sizes
    du -sh [dir_path]

system disk usage; display system wide disk space usage

    df -h


## Shell commands

`shopt` ... shell options

    # list all available shell options and whether they are set
    shopt

    # set a shell option
    shopt -s [option]

`xargs` ... pass output of a command to the next

    ls -d [dir_path] | xargs -I {} echo {}


## Server commands

`systemctl [start stop] [service]`

`journalctl -f`

`apache2 [start stop reload restart]`

`a2enmod` ... enable an apache2 mod
`a2ensite` ... enable an available apache2 webservice configuration
`a2disite` ... disable an available apache2 webservice configuration

`certbot` ... create https certificates for a webservice

Scheduled jobs via `crontab`:

    # list current users crontab
    crontab -l

    # list specificed users crontab
    sudo crontab -lu [username]

    # edit crontab [for superuser]
    [sudo] crontab -e 


## Networking commands

`ss` ... tool to investigate sockets (former `netstats`)

`nmap` ... show ports of a running server

    # e.g.
    nmap example.org

`hostname`

    # print name of the current host
    hostname

    # print IP of the current host
    hostname -I

`ssh` ... log into a remote host. requires a private ssh key in ~/.ssh and
        the public key pendant in the ~/.ssh/authorized_keys file on the remote host.

`scp` ... provides remote access like ssh, but copies files instead of logging
        into the remote machine.

`rsync` ...


## File handling

Compress all files into a common zip archive

    zip [archive_name] [directory]
    
    # add files recursively
    zip -r [name] [dir] 

    # move files into the archive
    zip -m [name] [dir]

    # add a password
    zip -e [name] [dir]

    # exclude specific files e.g. text files
    zip -e [name] [dir] -x \*.txt

Decompress zip archive

    # unzip all files into the current directory
    unzip [archive_name]
    
    # unzip all files in a directory - will create the dir if it does not exist
    unzip [name] -d [directory_name]

    # unzip files without overwriting files
    unzip -n [name]

    # list content
    unzip -l [name]

Compress all files into a common tar archive

    # c ... create, z ... zip content, v ... verbose, f ... archive_name
    tar -czvf [archive_name].gz.tar [directory]

Decompress all files from a tar archive

    # x ... extract, z .. unzip content, v ... verbose, f ... archive_name; 
    # Extract content into current directory
    tar -xzvf [archive_name].gz.tar

Compress all files in a specified directory individually

    gzip [dir]/*

    # include subdirectories
    gzip -r [dir]/*

Decompress all zipped files in a specific directory

    gunzip [dir]/*
    gzip -d [dir]/*

Deduplicate files; the files to be compared for deduplication must not be zipped

    fdupes [dir]
    
    # remove duplicates without asking
    fdupes -dN [dir]

Get md5 hashes of files:

    md5sum [file/dir]


## Paths

### Server related paths
    /etc/apache2
    /etc/letsencrypt

### Server email related
    /etc/postfix
    /etc/aliases

### user and groups
    /etc/group
    /etc/passwd

    /var/logs

    /home/[uname]/.ssh

### TTYs

    /dev/pts

### Systemwide available executables

    /usr/bin


## Env vars

    $PATH
    $USER
    $UID
    $HOME



# Docker variants


Build a container with the source code found at a provided directory

    docker build -t [containername:label] [source_dir]

Start a container in detatched mode, remove it when it is stopped.

    docker run --rm -dit [container]

List running containers

    docker ps

List all containers, running and stopped

    docker ps -a

List all images

    docker images

Remove container

    docker rm [container]

Remove image

    docker rmi [image]

Access log of a running container and follow

    docker logs -f [container]

Access a running container in interactive mode

    docker exec -it [container] /bin/bash

## Docker compose

Start docker containers defined in a `docker-compose.yml` file. This
file has to reside in the directory where the following command is executed.
Any `.env` file providing environment variables for the services have to reside 
in the same directory as well.

    # -p defines a name for the started containers. by default, its the directory name (?)
    # -d starts the containers in detached mode 
    docker-compose -p [projectname] up -d

## Notes
- when using volumes, the directories on the host system need to be assigned either 
  to a user that is in the user group or should be assigned to the docker group. 


# Postgres

Access a specific database with a specific user

    psql -U[username] -d[dbname]

`\dn`           ... list schemas

`\dt`           ... list tables

`\d [table]`    ... display details of [table]


# Random usage notes

How to figure out if anyone is connected to a service:

    /var/log/apache2/other_vhosts_access.log
    
    # e.g.
    cat /var/log/apache2/other_vhosts_access.log | grep "GET /login"

Or connect to the web service docker container and run

    watch ss

Connect to one host via another one that is accessible from outside a network

    ssh -A -J username@gateway.org username@[ip address of target in closed network]

Find out which operating system is running

    uname -a
    lsb_release -a
    cat /etc/*_version
    cat /etc/*-release
