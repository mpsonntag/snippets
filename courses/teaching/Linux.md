Linux and using the Bash (Bourne Again Shell)
=============================================

#  Using the shell - a starters introduction

Baby steps:
1) get someone to show you how to open a shell and execute commands
2) get to know the file system and how to navigate through it (see explanatory tutorial above)
3) get to know the basic shell commands described below
4) script away

## Opening and closing a shell
Under Ubuntu Linux a terminal can be opened by using `Ctrl + Alt + T`.
The shell can again be closed by typing `exit`.

##  More resources:
Understanding the unix file system (you should really read this):
- http://www.december.com/unix/tutor/filesystem.html

and (if you are really interested)
- https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard

Shell Tutorials (you can work through this if you want to know more about using the shell)
- https://linuxcommand.org/lc3_learning_the_shell.php

## Navigating the filesystem:
When you first open your shell you will see something like this:
    
    [chris@troll ~]$

This means, that you are logged into a Linux network with username "chris",
that you currently use the computer named "troll" and are currently within the space
the filesystem has reserved as your workspace (indicated by "~").

In a more abstract way you will always see the information like this:

    [username@computername current_folder]$

You can navigate through the filesystem by using the "cd" (change directory) command right after the "$" sign.
Work yourself through the navigation introduction provided via the links above.


## Linux nice to knows

- Special characters which are not allowed in file- or folder names:

    ` /, .., ~, *, ?, >, <, |, \`

- Linux is case sensitive!
    `Filename.txt` is not the same as `filename.txt`

- Try to avoid blanks within file- or folder names, always use underscore or minus; especially,
if you create folders or files using the filebrowser!

        e.g.
        do not use:
        project computational systems biology
        
        use:
        project_computational_systems_biology

- Use the auto-complete function provided by the tabulator key:

        [username@computername ~]$cd /h

    hit "tab" once, it should auto-complete your entry to

        [username@computername ~]$cd /home/

    if you hit "tab" twice, it will display the contents of the directory, without disrupting your command entry

        [username@listeria ~]$ cd /home/
        admin/ apps/  conf/  edu/   proj/  user/
        [username@listeria ~]$ cd /home/

    if there are more than one files or directories with the same starting letters (e.g. `/home/` or `/hello/`) you will have to enter the next letter, before autocomplete will work

        [username@listeria ~]$ cd /h    

    "tab" will  not work
    but:

        [username@listeria ~]$ cd /he

    "tab" returns:

        [username@listeria ~]$ cd /hello/

- Get help! : either by using "man" (manual) command:

        [username@computername directory]$man [command]

        e.g. [chris@troll ~]$man cp

    or by using `--help` commandline option:

        [username@computername directory]$[command] --help

        e.g. [chris@troll ~]$cp --help

- Most of the command line programs displaying the contents of text files can be ended by simply pressing "q".

- How to end a running program:

        ctrl + c

- How to stop a running program (process will be on hold in the background):

        ctrl + z

- How to kill a running program (process will be terminated):

        ctrl + d

- No paper basket! If you remove files or directories using the shell, there is no easy recovery!

## Basic Bash commands:

- `ls`        ... display files and directories within your current directory
- `ls -l`     ... like ls, but display additional information
- `ls -a`     ... like ls, but also display hidden files and directories
- `ls -l -a`  ... combination of `ls -l` and `ls -a`
- `ls ../Foldername` ... display the contents of directory "Foldername" residing on the same
hierarchical layer as the folder we are currently residing in
- `ll` ... is an alias for `la -la`, might not be available in non-bash shells
- `pwd` ... print working directory, prints the complete path from root until the directory we are currently residing in

        e.g. [chris@troll papers]$pwd
             /home/users/chris/papers/
             [chris@troll papers]$

- `cd [path]` ... change directory; move within the filesystem from your current directory to another directory specified in your [path]

        e.g. [chris@troll ~]$ cd /home/user/bernd/

- `cd ..`   ... change from the current directory to the directory directly above.

- `mkdir foldername` ... create folder "foldername" at your current position within the filesystem

        e.g. [chris@troll papers]$ mkdir cell_papers

- `rmdir foldername` ... remove folder "foldername" from the filesystem. will only work, if the folder is empty.

        e.g. [chris@troll papers]$ rmdir cell_papers

- `rm filename` ... remove file "filename" from the filesystem.

        e.g. [chris@troll papers]$ rm 2011_Science_2282772.pdf

- `rm foldername -r` ... remove folder `foldername` from the filesystem including all files and folders it contains.

        e.g. [chris@troll work]$ rm papers -r

- `cp path1/source path2/target` ... copy file `source` residing at location `path1` to file `target`
residing at location `path2`

        e.g. [chris@troll work]$cp /home/user/chris/work/papers/2011_Science_2282772.pdf /home/users/chris/work/papers/science/2011_Science_2282772.pdf

- `cp path1/source ./target` ... copy file `source` residing at location `path1` to file `target` at the current location

        e.g. [chris@troll science]$ cp /home/user/chris/work/papers/2011_Science_2282772.pdf ./2011_Science_2282772.pdf

will copy the file `2011_Science_2282772.pdf` from location `/home/user/chris/work/papers/` to location `/home/users/chris/work/papers/science/`

- `cp path1/source .` ... copy file`source` residing at location `path1` to the current location, keeping the same filename.

        e.g. [chris@troll science]$ cp /home/user/chris/work/papers/2011_Science_2282772.pdf .

will copy the file `2011_Science_2282772.pdf` from location `/home/user/chris/work/papers/` to location `/home/users/chris/work/papers/science/`

- `mv [Pfad-Quelle]/[Filename] [Pfad-Ziel]` ... same as "cp" command, but moves the file from one location to the other, deleting the original file.

- `echo text` ... prints "text" onto the screen

        e.g. [chris@troll work]$ echo hurray for icecream!
        
- `echo text > filename.txt` ... saves "text" into file "filename.txt" which will be created at the current filesystem location

        e.g. [chris@troll work]$ echo hurray for icecream! > important.txt

- `cat filename` ... prints the contents of file "filename" onto the screen.

        e.g. [chris@troll work]$ cat important.txt

- `less filename` ... displays the contents of file "filename" in the screen, contents are scrollable by using "up" and "down" keys. end this by pressing "q"

        e.g. [chris@troll work]$ less important.txt

- `history` ... list of all commands executed within this terminal

        e.g. [chris@troll ~]$ history

- `exit` ... close the shell

        e.g. [chris@troll ~]$ exit

- `man [program]` ... manual of a command line program. Displays a brief description and all command line options.

        e.g. [chris@troll ~]$ man ls

## Further basic Bash command line options:

- `[command] > [filename]` ... will write the output of a specific `[command]` to a specific file.
Note, that an already existing file with the same filename at the same location will be replaced!

        e.g.    [chris@troll work]$echo hurray for icecream! > important.txt
                [chris@troll work]$less important.txt
                [chris@troll work]$echo another hurray for schnitzel! > important.txt
                [chris@troll work]$less important.txt

- `[command] >> [filename]` ... will append the output of a specific `[command]` to a specific file.
If the file does not exist yet, it will be created.

        e.g.    [chris@troll work]$echo chicken >> shopping_list.txt
                [chris@troll work]$less shopping_list.txt
                [chris@troll work]$echo onions >> shopping_list.txt
                [chris@troll work]$echo lemons >> shopping_list.txt
                [chris@troll work]$echo olive oil >> shopping_list.txt
                [chris@troll work]$echo rosemary >> shopping_list.txt
                [chris@troll work]$less shopping_list.txt

- `[command] &` ... start a program running in the background, getting back the shell.

        e.g.    [chris@troll work]$firefox &

- `[command]` ... start a program

        e.g.    [chris@troll work]$firefox

- `ctr + z`         ... stop the execution of the program and keep it on hold in the background
- `bg`              ... restart the program, but keep it running in the background (bg)

                [chris@troll work]$bg

- `fg`              ... if you have a program running in the background, get it back by fg (foreground)

        e.g.    [chris@troll work]$fg

- `command_1 | command_2` ... | ... "pipe". executes "command_1", directs the output of this command not to the screen, but the second command "command_2". Only then the output of "command_2" will be printed onto the screen.

- `dd`          ... create a file with a specific size

        # create 10MB file named 'out.txt' filled with zeros 
        e.g. dd if=/dev/zero of=out.txt bs=1M count=10

Output from commandline programs can easily be formatted to display as a table
by piping it to the `column` command e.g.:

    cat /etc/passwrd | column -t -s :

### File content handling

- replace spaces with tabs

        cat textfile.txt | tr ':[space]:' '\t' > out.txt

- convert a file to upper or lower case

        cat textfile.txt | tr a-z A_Z > out.txt


# Advanced commands and good to knows

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

`sudo` ... execute commands as a different user. default user is root which has administrative permissions.

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

Find out which partition a file or directory belongs to

    df -T [dir_path]

List all block devices

    sudo sfdisk -l
    lsblk -l

List disk hardware

    sudo lshw -short -C disk


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

`rsync` ... Copy and update all files from a local directory to and at a remote directory
- new files will be copied
- files that were changed locally will overwrite the remote files
- ideally run the command with the `dry-run` flag first to ensure that the update is save

        rsync -v --dry-run --update -e "ssh -i [key location]" -r /local/path/to/folder/ [username]@[remote hostname or IP]:/remote/path/to/parent/folder

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
