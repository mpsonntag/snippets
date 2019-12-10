# Linux commands and paths

... that are good to know and understand...


## Job control

Starting an application in the background and returning an active command line 
can be done by using `&` after the command.

    gedit &

To see which jobs are running in the background of the shell, use `jobs`

    # example of the use case above
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

`/dev/pts` contains the required files of all the currently open terminals

To identify the files location of the currently open terminal type `tty`.

To get more information about what a tty is, read this [tty introduction](
http://www.linusakesson.net/programming/tty/index.php).

`env` ... Display all environmental variables of the current shell

`shopt` ... shell options

    # list all available shell options and whether they are set
    shopt

    # set a shell option
    shopt -s [option]

`xargs` ... pass output of a command to the next

    ls -d [dir_path] | xargs -I {} echo {}


## User and permission commands

`useradd` ... add a user

`groupadd` ... add a user to a group

`chown` ... change the user and group owners of a file or directory

    chown [username]:[group] [file/dir]

    # if a directory is provided, -R can also change ownership recursively for all children
    chown -R fuseki:docker /some/directory

`chmod` ... change file permissions; define which users and groups 
            are allowed to access, change or execute a file.
            Read up [here](https://www.linux.org/threads/file-permissions-chmod.4124/) 
            on file permissions.

`sudo` ... execute commands as a different user. default user is root

`su` ... switch to a different user; can also run commands w/o opening a new shell

    # switch to a different user, opening a new shell, stop with 'exit'
    su - [username]

    # run a command as specific user; requires password
    # -m preserves the current environment except for $PATH
    # -c invokes running a command
    su [username] -m -c 'ls -la'

`passwd` ... change password

`id` ... check if a user exists, list user id and groups

    id [username]

## File commands

Use `cp [source] [target]` to copy files or directories
Use `mv [source] [target]` to move them

Copy command

    # -r ... recursive, -u update target only, -L resolve symbolic links, v ... verbose
    cp -vruL [source_directory] [target_directory]

Get the name of a file in a path

    basename [path]

Get the directory of a file in a path

    dirname [path]

Watch a file or a command and refresh the view, exit with `ctrl+c`

    # e.g. the content of a file
    watch tail file.log
    # e.g. running docker containers
    watch docker ps


## File management

Compress all files in a directory into a common zip archive

    zip [archive_name] [directory]
    
    # add files recursively
    zip -r [name] [dir]

    # move files into the archive (remove them from the directory)
    zip -m [name] [dir]

    # add a password
    # add a password
    zip -e [name] [dir]

    # exclude specific files e.g. text files
    zip [name] [dir] -x \*.txt

Decompress zip archive

    # unzip all files into the current directory
    unzip [archive_name]
    
    # unzip all files into a directory - will create the dir if it does not exist
    unzip [name] -d [directory_name]

    # unzip files without overwriting files
    unzip -n [name]

    # list content
    unzip -l [name]

Compress all files into a common tar archive; 
    will not create archive file extension on its own.

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

Print tree structure of a directory

    tree [dir]


## Disk management

Directory disk usage; display estimated size of a directory

    # s ... print only total size
    # h ... print human friendly sizes
    du -sh [dir_path]

System disk usage; display system wide disk space usage

    df -h


## Server commands

`systemctl [start stop] [service]`

`journalctl -f`

`apache2 [start stop reload restart]`

`a2enmod` ... enable an apache2 mod
`a2ensite` ... enable an available apache2 webservice configuration
`a2disite` ... disable an available apache2 webservice configuration

### Webservice certificates for encryption via certbot

When using certbot, make sure you have the latest version and some additional
plugins installed:

    sudo apt-get update
    sudo apt-get install certbot python3-certbot-apache

`certbot` ... create https certificates for a webservice

Check installed certificates and their status:

    certbot certificates

Check installed certbot plugins:

    certbot plugins

When trying to renew a certificate manually, make sure to use the `--dry-run` option
first. If a renewal continuously fails a timeout for the next run might occur:

    certbot renew --dry-run

Renew all installed certificates:

    certbot renew

If you have an apache running up front your webservice, the renewal might require
the `apache` flag; this probably depends on the `cerbot` version in use, newer version
appear to do this automatically.

    certbot renew --apache

### Scheduled jobs via `crontab`:

    # list current users crontab
    crontab -l

    # list specificed users crontab
    sudo crontab -lu [username]

    # edit crontab [for superuser]
    [sudo] crontab -e 

Note on how to read crontabs:

* * * * *       command
| | | | |
| | | | + ----- day of the week; 0-6; Sunday=0
| | | + ------- month; 1-12
| | + --------- day of the month; 1-31
| + ----------- hour; 0-23
+ ------------- min; 0-59 or fractions e.g. */10 ... every then minutes

If not differently set up crontab writes its log entries to syslog:

    /var/log/syslog

- find cron specific log entries:


    grep CRON /var/log/syslog


By default crontab sets up jobs under the currently logged in user. There can
be different crontabs under different users including root.


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

`curl` ... run http requests from the command line

    # run a GET http request
    curl [URL]

    # run a POST http request
    curl -X POST [URL]

    # add content header
    curl -H "Content-Type: application/rdf+xml" [URL]

Interesting for debugging with Chromium:
- "Network" - right click request - Copy - Copy as curl


## Scripting

Use `test` or `[]` for checks that make sense from a command line perspective
e.g. if a directory or a file exists, which of a file is older etc.
This builtin provides a wide range of available checks, see `man test` for a list.

    # e.g. Check whether a directory exists
    test -d dirname && echo "exists" || echo "does not exist"


## Paths

### Executables

Most of the executables that are available on the command line are
softlinks found in this directory:

    /usr/bin

Some of these executables are linked from the alternatives directory, that
contains different variants of software which in turn contains links to
the actual location of the files

    /etc/alternatives 

### Server related paths
    /etc/apache2
    /etc/letsencrypt

### Server email related
    /etc/postfix
    /etc/aliases

### user and groups
`/etc/group` ... contains all available groups and the ids of users that are part of a group
`/etc/passwd` ... contains all users with their id, shell preference and home directory

`/var/logs`
`/home/[uname]/.ssh` ... directory containing user specific ssh keys

### TTYs

    /dev/pts

### Default mount points

A mount point is a link between a disk partition and the file system on 
this partition

    cat /etc/fstab

More info on [mount points](http://www.linfo.org/mount_point.html)
Easy, graphic introduction to [partitioning and mount points](
https://www.linuxnix.com/what-is-a-mount-point-in-linuxunix/)
Another introduction to [Linux disk management](
https://www.linuxnix.com/disk-management-in-linux/)


### System wide available executables

    /usr/bin


## Env vars

    $PATH
    $USER
    $UID
    $HOME


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

## Using different java versions

Currently there are a couple of java version from two main distributers (Oracle, OpenJava)
flying around. One can have both of them installed and switch between them using the
`update-alternatives` command.

If one does `which java`, it will give the path `/usr/bin/java`. An `ls` on that folder
will show, that this is actually just a link to a java version in `/etc/alternatives/jvm`.
An `ls` on the `/etc/alternatives/jvm` folder will show, which java versions are installed.

To switch between these alternatives use:

    `sudo update-alternatives --config java`

There you will be prompted to select which of the java versions installed should
be linked to `/usr/bin/java`.

Be aware tough, that this does not also link the `javac` command to the appropriate
version as well. So you usually should update both to the required java distribution.

Check [here](http://ask.xmodulo.com/change-default-java-version-linux.html) for details.
 

Updating the alternatives does not update the environment variables though. Until a
restart PATH, JAVA and JAVA_HOME might need a manual reset to link to the appropriate
java version.

### SBT project and activator specifics

If you are running sbt projects and you ever get errors along the line:

'The java installation you have is not up to date
Activator requires at least version 1.6+, you have
version [xxx]'

then you need to switch your java alternatives and reset the JAVA_HOME environment
variable and make sure the variable properly set via `.profile` or `.bash_alias`

e.g. 

    JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64/
    # or 
    JAVA_HOME=/usr/lib/jvm/java-12-oracle/


## Adding additional fonts

The following notes are at least true for Ubunut 18

- create a folder in `/usr/share/fonts/truetype/newfonts`
- move any new `.ttf` font files into this folder
- the system should automatically make the new fonts available
- you can check whether they have been added via


        fc-list | grep [name of new font]

- if a font has not been properly added, the font cache might need to
  be refreshed; use the `fc-cache` command in this case.
