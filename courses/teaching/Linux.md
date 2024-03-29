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
             /home/chris/papers/
             [chris@troll papers]$

- `cd [path]` ... change directory; move within the filesystem from your current directory to another directory specified in your [path]

        e.g. [chris@troll ~]$ cd /home/bernd/

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

        e.g. [chris@troll work]$cp /home/chris/work/papers/2011_Science_2282772.pdf /home/chris/work/papers/science/2011_Science_2282772.pdf

- `cp path1/source ./target` ... copy file `source` residing at location `path1` to file `target` at the current location

        e.g. [chris@troll science]$ cp /home/chris/work/papers/2011_Science_2282772.pdf ./2011_Science_2282772.pdf

will copy the file `2011_Science_2282772.pdf` from location `/home/chris/work/papers/` to location `/home/chris/work/papers/science/`

- `cp path1/source .` ... copy file`source` residing at location `path1` to the current location, keeping the same filename.

        e.g. [chris@troll science]$ cp /home/chris/work/papers/2011_Science_2282772.pdf .

will copy the file `2011_Science_2282772.pdf` from location `/home/chris/work/papers/` to location `/home/chris/work/papers/science/`

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


## User management

[TODO merge with block below]
Display all users

    getent passwd
or

    cat /etc/passwd 

or

    compgen -u

Add a new user

    # user friendly perl script using 'useradd' 
    sudo adduser [new_username]

or

    # native binary compiled with the system
    sudo useradd [new_username]

Delete user

    sudo userdel [username]

Remove home directory of a removed user recursively

    sudo rm /home/[username] -r

Modify username

    usermod -l [new_username] [old_username]

Change Password

    sudo passwd [username]

Change shell of a user

    sudo chsh [username]

    # if this does not work, try
    sudo usermod -s /bin/bash [username]


If this does not work e.g. because the user was created without a shell, run the following

    sudo usermod -s /bin/bash [username]

Change permissions of a group to the same as the user

    sudo chmod -R g=u


## User and permission handling

Unix systems feature groups and users to handle any access permissions.

### User specific commands


### Users and user specific commands

- change the password of the active user

        passwd

- every user belongs to a user group.

- list all registered users including their userID and their groupID

        cat /etc/passwd

- display all active/available users:

        users

- add a new user w/o a home directory:

        sudo useradd [new_username]

- add a new user and create a home directory and a password for this user:

        sudo useradd -m [new_username] -p [password]

- modify the name of a user

        usermod -l new_username old_username

- check if a user exists by name, list the id of a user and the groups a user is assigned to

        id [username]
        # alternativeley use getent
        getent passwd [username]

- modify the id of a user; use IDs 1000+, ids must be unique.

        usermod -u [newID] [username]

- add a user to an existing group

        useradd -g [groupID/Name] [username]
        # or
        usermod -a -G [groupID/Name] [username]

- remove a user from all groups except their own group

        usermod -G "" [username]

- remove a user from one specific group

        gpasswd -d [username] [groupname]

- work as a different user; can also run commands w/o opening a new shell

        # switch to a different user, opening a new shell, exit shell with 'exit'
        su - [username]

        # run a single command as specific user w/o opening a shell; requires password
        # -m preserves the current environment except for $PATH
        # -c invokes running a command
        su [username] -m -c 'ls -la'

- execute commands with `root` privileges; default user is root which has administrative permissions

        sudo [command]


### Groups

users can belong to groups, permissions can be given via groups 
to all users within a group.

- show all registered groups

        cat /etc/group

- check if a group exists by name

        getent group [groupname]

- display all active/available groups of/for the active user

        groups

- add a new group

        sudo groupadd [groupname]

- change groupID

        groupmod -g [newID] [group]

- delete a group

        groupdel [group]


### File permissions and ownership

`chown` ... change the user and group owners of a file or directory

    chown [username]:[group] [file/dir]

    # if a directory is provided, -R can also change ownership recursively for all children
    chown -R fuseki:docker /some/directory

`chmod` ... change file permissions; define which users and groups 
            are allowed to access, change or execute a file.
            Read up [here](https://www.linux.org/threads/file-permissions-chmod.4124/) 
            on file permissions.

```bash
# general syntax;
# mode ... o ... other users, g ... user group, u ... user
# permission mod ... + ... add permission, - ... remove permission
# permission ... r ... read, w ... write, x ... execute
chmod [USER/PERMISSIONMOD/PERMISSION] [DIR/FILE]
# add file permission read, write and execute for all other users
chmod o+rwx [file/dir]
# remove file permission read, write and execute for all other users
chmod o-rwx [file/dir]
# add file permission read, write and execute for group
chmod g+rwx [file/dir]
# add file permission read, write and execute for user
chmod u+rwx [file/dir]
# change file permissions recursively
chmod -R [MODE] [file/dir]
# change different permissions
chmod u=rwx,g=r,o-rwx [file/dir]
```


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


## Running services with systemctl

`systemctl` is a service that is shipped with the `systemd` suit for handling services on a linux
machine. `systemctl` specifically handles the state of system services (daemons) e.g. starting, stopping, etc.

Start a service ("unit"); usually requires `sudo`

    systemctl start [service]
    # e.g. docker.service
    systemctl start docker.service

Stop a service

    systemctl stop [service]

Restart a service (= stop+start)

    systemctl restart [service]

Reload a service w/o interrupting the service

    systemctl reload [service]

Check the status of a service

    systemctl status [service]

Show all settings of a service

    systemctl show [service]

Enable or disable services to be run automatically; enabled units will start automatically when the system boots

    systemctl [enable/disable] [service]

List all units that have the "failed" status

    systemctl --failed

List all units and its current status

    systemctl list-unit-files

Lists all units; use the `--all` flag to also include disabled services

    systemctl list-units [--all]

systemctl services can be custom made and be put on a timer as well. To list all current timers:

    systemctl list-timers

Inspect systemd unit files; this will also show the location of the unit file itself

    systemctl cat [service]
    # e.g. the docker service unit file
    systemctl cat docker.service

Show the dependencies of a service

    systemctl list-dependencies [--all] [service]

Edit unit files w/o opening the file via its location

    sudo systemctl edit [service]
    # e.g. docker service unit file
    sudo systemctl edit --full docker.service
    # reload the service for the changes to take effect
    sudo systemctl daemon-reload

Find an introduction to systemctl [here](
https://www.digitalocean.com/community/tutorials/systemd-essentials-working-with-services-units-and-the-journal
).

### Handle systemd logs using journalctl

The `journald` daemon follows logs from all running `systemd` services; these journals can be accessed using `journalctl`.

Follow all current systemctl logs

    journalctl -f

Filter the logs by units AND follow e.g. by following the docker daemon

    journalctl -u docker.service -f

Filter logs for multiple units

    journalctl -u docker.service -u apache2.service

Display on the latest `n`, e.g. 100, lines

    journalctl -n 100

Display log in reverse order

    journalctl -r

Filter log for a rough timeframe using `--since`

    # supported: yesterday, today, now, tomorrow
    journalctl --since today
    # use a specific date and time
    journalctl --since "2020-12-12 12:12:12"

Filter log for a specific timeframe

    # use date and time
    journalctl --since "2020-12-12" --until "2020-12-13 13:13"
    # use keywords: n sec ago, min, hour, day, month, year 
    journalctl --since 09:00 --until "1 hour ago"

Display journalctl in a different format e.g. JSON

    # supported: cat, export, json, json-pretty, json-sse, short, short-iso, short-precise, verbose
    journalctl -o json-pretty

Pipe the output to system out e.g. to consume in an automated script or for further filtering

    journalctl --no-pager

Find a more detailed introduction [here](
https://www.digitalocean.com/community/tutorials/how-to-use-journalctl-to-view-and-manipulate-systemd-logs
) or [here](
https://www.loggly.com/ultimate-guide/using-journalctl/
).

### An introduction to systemd and unit files

`systemd` is a service manager for a wide range of Linux distributions. It is used to initialize and
handle system services and provides a logging service. `systemctl` is used to handle the state of 
services, `journalctl` is used to handle logs from the individual services.

At the core of `systemd` services are the `unit` files. These are flat text files containing all
information required to run a specific service. The extension of such a unit file describes
which kind of service can be handled with it.

#### systemd service types

`systemd` supports the following types of services; all corresponding unit files have the file ending as listed below:
- service   ... manage a constantly running service and its dependencies
- timer     ... systemd managed time dependent service analogous to `cron` jobs.
- socket    ... manage activity encountered at a specified socket. Needs an additional `.service` file to handle the required activity.
- path      ... used for path based activation and requires a `.service` file; cf. `socket`.
- target    ... synchronisation between units when booting or changing state
- mount     ... manage mountpoints using systemd
- automount ... requires a `.mount` unit and automatically handles the mountpoints described
- device    ... handling dependencies accessing specific devices
- swap      ... handle system swap space

#### Unit files


#### systemd paths

The default systemd unit files are kept at `/lib/systemd/system` and should not be modified.
Custom systemd unit files should be kept at `/etc/systemd/system`; files or directories in this
directory will overrule files or directories found in the default location.

Ideally use `systemctl` itself to create and modify `unit` files.

Find a detailed introduction [here](
https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files
)


## Running a webserver using apache2

Usually apache2 should be available as systemd service

    sudo systemctl [start stop reload restart] apache2.service

Enable or disable apache2 mods and webservice configurations; an apache2 reload is required

    # enable an apache2 mod
    sudo a2enmod [mod]
    # e.g. the rewrite module
    sudo a2enmod rewrite
    # disable an apache2 mod
    sudo a2dismod [mod]

    # enable a webservice configuration
    sudo a2ensite [conf]
    # disable a webservice configuration
    sudo a2dissite [conf]

After changing a mod or a site, apache requires a reload.

Display loaded modules

    apache2ctl -M
    # alternatively
    apache2ctl -t -D DUMP_MODULES

All modules and sites can be found in the following paths

    /etc/apache2/sites-available
    /etc/apache2/sites-enabled
    /etc/apache2/mods-available
    /etc/apache2/mods-enabled


### Session handling

When connected to a remote machine, it might be worthwhile to create a named session that keeps running if the connection is detached.

- `screen` can be installed via apt-get

        # start a named screen session
        screen -S [some name]
        # start working e.g. start a long running script
    
        # detach from session but keep it running
        Ctrl + d + a
        
        # re-attach to running session
        screen -r [some name]
    
        # exit a screen session and end it
        exit

        # list all running screen sessions
        screen -ls

        # end a specific screen without attaching to it
        screen -XS [some name] quit
        
        # if there are multiple screen sessions with an identical name, screen ls will 
        # show additinal screen ids that can be used to end a specifc session
        screen -XS [screenid.some name] quit


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


To check whether certbot set up automatic renewals on a debian system, run the following and 
check for a certbot renewal job.

    systemctl list-timers

The systemd files can also be checked directly at `/etc/systemd/system/snap.certbot.renew.service` or `.timer`

The certificates issued can be found in the `/etc/letsencrypt/`. Usually the certificates are created in the `/etc/letsencrypt/archive` directory, the latest is symlinked to the `archive` directory from the `/etc/letsencrypt/live` directory. When used with an apache, the apache config should always point to the `live` directory; when an autorenewal job is set up, the apache will always have access to the latest certificate.

The certificates are bound to a domain name, not to an IP address or server host key. So if the server is changed, the certificates can actually be moved to the letsencrypt folders on the new machine and can be used on the fly.

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
        See section below for a detailed introduction.

`scp` ... provides remote access like ssh, but copies files instead of logging
        into the remote machine.

### File copy with "rsync"

`rsync` ... Copy and update all files from a local directory to and at a remote directory
- new files will be copied
- files that were changed locally will overwrite the remote files
- ideally run the command with the `dry-run` flag first to ensure that the update is save
  ```bash
  rsync -v --dry-run --update -e "ssh -i [key location]" -r /local/path/to/folder/ [username]@[remote hostname or IP]:/remote/path/to/parent/folder
  ```

- Useful flags description
  - t ... preserve timestamp; avoid issues when writing back and forth between multiple machines
  - i ... show reason for action
  - v ... verbose
  - r ... recursive
  - u ... update only - do not overwrite newer in target
  - n ... dry run

```bash
# Copy directory COPY_DIR from a local to remote; dry-run, update only, show reason for change, preserve timestamp
rsync -ivrut -e "ssh -i /home/$USER/.ssh/" /home/$USER/COPY_DIR/ $USER@$REMOTE:/home/$USER/COPY_DIR/ -n
```

- itemize output; a good description of the itemize output can be found [here](http://www.staroceans.org/e-book/understanding-the-output-of-rsync-itemize-changes.html)
  ```
  YXcstpoguax  path/to/file
  |||||||||||
  `----------- the type of update being done::
   ||||||||||   <: file is being transferred to the remote host (sent).
   ||||||||||   >: file is being transferred to the local host (received).
   ||||||||||   c: local change/creation for the item, such as:
   ||||||||||      - the creation of a directory
   ||||||||||      - the changing of a symlink,
   ||||||||||      - etc.
   ||||||||||   h: the item is a hard link to another item (requires --hard-links).
   ||||||||||   .: the item is not being updated (though it might have attributes that are being modified).
   ||||||||||   *: means that the rest of the itemized-output area contains a message (e.g. "deleting").
   ||||||||||
   `---------- the file type:
    |||||||||   f for a file,
    |||||||||   d for a directory,
    |||||||||   L for a symlink,
    |||||||||   D for a device,
    |||||||||   S for a special file (e.g. named sockets and fifos).
    |||||||||
    `--------- c: different checksum (for regular files)
     ||||||||     changed value (for symlink, device, and special file)
     `-------- s: Size is different
      `------- t: Modification time is different
       `------ p: Permission are different
        `----- o: Owner is different
         `---- g: Group is different
          `--- u: The u slot is reserved for future use.
           `-- a: The ACL information changed
  ```


### http requests with "curl" (commandline url)

`curl` ... run http requests from the command line

    # run a GET http request
    curl [URL]

    # run a POST http request
    curl -X POST [URL]

    # add content header
    curl -H "Content-Type: application/rdf+xml" [URL]

Interesting for debugging with the Chromium browser:
- "Network" - right click "request" - Copy - Copy as curl

Read up on the http protocol if you are not familiar with it. 

- commandline tool for sending a GET http request (GET is the default http request method for curl)

        curl "http://www.hntoplinks.com"

- include the http response headers: `-i`

        curl -i "http://www.hntoplinks.com"

- add a request header: `-H`

        curl "http://www.hntoplinks.com" -H "Accept: application/json" 

- use a different request method than GET: `-X`

        curl -X POST "http://somewhere.com?value=key"

- add a request body to the request: `-d`

        curl -X POST "http://somewhere.com" -d "value=key"

- add an http form body to the request: `-F`

        curl -X POST "http://somewhere.com" -F user[lname]=Karl

Find a very nice introduction to curl [here](http://conqueringthecommandline.com/book/curl).


## Secure connection and keys 

### ssh (Secure SHell)

- Connect to another machine using secure shell (an encrypted connection to another computer within the network). 
- Makes sense to do large calculations on the server rather than on the local machine.
- Logging on to another machine will most likely require a password.

    ```bash
    ssh [remote_machine]
    # provide username on the remote machine and appropriate password

    e.g.
    [chris@troll work]$ssh server4
    [chris@server4 ~]$

    # the login process can be sped up by already providing the username in the login command
    ssh [username]@[remote_machine]
    ```

- Notice that the name of the machine in the bash shell has changed from `troll` to `server4`
- Use the command `exit` to close the ssh connection to a remote machine.

    ```bash
    e.g.
    [chris@server4 ~]$exit
    [chris@troll ~]$
    ```

### scp (Secure Copy)

- Use a secure connection to copy files from or to a remote machine

  ```bash
    scp [remote_machine_name]:[remote_directory]/[filename] [local_directory]

    e.g.
    [chris@troll work]scp server4:/temp/work/* /home/chris/work/
  ```

- Add the username of a user on the remote server to provide specific permissions for the copy operation

      scp [remote_username]@[remote_machine_name]:[remote_directory] [local_directory]

- Copy directories recursively to copy whole directory trees (`-r` ... recursive)

      scp -r [remote_machine]:[remote_dir]/* [local_dir]

- Copy directories recursively and preserve file metadata (modes, access times etc, `-p` ... preserve)

      scp -rp [remote_machine]:[remote_dir]/* [local_dir]

### SSH keys

- For some secure connections, specific SSH keys are required e.g. to use the ssh option with github.
- if you are not familiar with PGP, read up on your trusty wikipedia page.
- generate ssh keys:

  ```bash
  ssh-keygen
  enter a name (without spaces!) e.g. id_rsa_key_description
  enter a pw pr leave it empty
  // print public key
  cat id_rsa_key_description.pub
  ```

- The created key pair can be found in a hidden `.ssh` folder in the home directory, if no other location has been 
    specified.

- To retrieve the SSH fingerprint of the public key use the following:

      ssh-keygen -lf [location and name of the public key]


### SSH Key Agent

Find a nice introduction [here](http://sshkeychain.sourceforge.net/mirrors/SSH-with-Keys-HOWTO/SSH-with-Keys-HOWTO-6.html) 
and laugh at the passphrase.

SSH keys reside in their folder, every time they are used, the passphrase has to be entered. 
To make them available to other services without having to point services to their proper keys and 
having to enter the pass phrase all the time.

- start an ssh-agent if it is not already started (might need one of the examples below to start properly)
    - BEWARE! when starting the agent, the environment will be reset, meaning any active agent
                is stopped, the new agent will not contain any keys, any keys previously added
                have to be added again! So when in doubt, run `ssh-add -l` first.

  ```bash
  eval "ssh-agent"
  eval "ssh-agent -s"
  eval `ssh-agent -s`
  eval $(ssh-agent)
  ```

- add key to the agent e.g. the key created in example above and enter the keys pass phrase once and never again.

      ssh-add ~/.ssh/id_rsa_key_description

- check which keys are currently managed by the ssh key agent

      ssh-add -l

- even if you have added the key to the ssh key agent, if the key with the corresponding passphrase 
    is not added to the linux keyring, it will prompt for the passphrase upon the first use of the 
    ssh key. If the option is used to store key and phrase in the keyring, this login will be
    done automatically and the prompt will not show up again, when the key is used.

- NOTE: as an important side note, when you have a lot of keys added to your agent, it will
  try all of them against a potential server you want to log in to. If the server has a low
  authentication failure tolerance, then you will be disconnected and potentially barred from
  new attempts for a while. Usually the message `Received disconnect from [IP address] port 22:2: 
  Too many authentication failures for [username]` is a dead giveaway. This can already happen
  when you have more than three ssh keys...
  You can debug this using the verbose setting on the ssh command e.g. `ssh -v username@some.server.com` 


### Convenient ssh access by using .ssh/config

As described above, having too many different ssh keys can lead to login issues. It is 
more convenient to tell the agent which key to offer to a specific server first to 
avoid such a dilemma.

Find a helpful tutorial about creating an ssh config file [here](
https://nerderati.com/2011/03/17/simplify-your-life-with-an-ssh-config-file/
).

- create a `config` file in the `.ssh` folder.
- define a specific Host and point to the ssh key file that should be used.

  ```bash
  Host some.example.org
      IdentityFile ~/.ssh/id_rsa_for_example
  ```

- if login at a specific port or with a different user is required

  ```bash
  Host other.site.com
      User root
      Port 4444
      IdentityFile ~/.ssh/id_rsa_for_site
  ```

## Setup user with sudo access on an ssh accessible server

Modified from [here](https://aws.amazon.com/premiumsupport/knowledge-center/new-user-accounts-linux-instance/).

- ssh to the server
- create new user (add password in the process)

      sudo adduser new_user

- [Optional] add user to the sudoer user group (after the user has been created)

      sudo adduser new_user sudo

- switch to new user, create .ssh folder and authorized key entry with the appropriate permissions for this user

  ```bash
  sudo su new_user
  mkdir /home/new_user/.ssh
  chmod 700 /home/new_user/.ssh
  touch /home/new_user/.ssh/authorized_keys
  chmod 600 /home/new_user/.ssh/authorized_keys
  ```

- open authorized keys with an editor e.g. and paste the required public key string into the file.

  ```bash
  vim /home/new_user/.ssh/authorized_keys
  # "press i"
  # "paste public key string"
  # "press esc and type :x to save changes"
  ```

- [optional] change user password

      passwd

- Now the new_user should be able to ssh into the server.

### ssh security

The [following article](
https://www.baeldung.com/linux/list-connected-ssh-sessions
) gives a couple of pointers where to start looking for ssh logins to a machine.

- check /var/log/auth.log

```bash
# e.g. look for successful sessions
cat /var/log/auth.log | grep "New Session"
# or failed password attempts
cat /var/log/auth.log | grep "Failed password"
# or check how many failed attempts at a specific date
cat /var/log/auth.log | grep "Failed password" | grep "May  9" | wc -l
```

- check logins via the `last` command


## Scripting

Use `test` or `[]` for checks that make sense from a command line perspective
e.g. if a directory or a file exists, which of a file is older etc.
This builtin provides a wide range of available checks, see `man test` for a list.

  ```bash
  # e.g. Check whether a directory exists
  test -d dirname && echo "exists" || echo "does not exist"
  ```


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
- `/etc/group`            ... contains all available groups, and the ids of users that are part of a group
- `/etc/passwd`           ... contains all users with their id, shell preference and home directory

- `/var/logs`             ... contains various logfiles of interest
- `/home/[uname]/.ssh`    ... directory containing user specific ssh keys

### TTYs

    /dev/pts

### Default mount points

A mount point is a link between a disk partition, and the file system on this partition

    cat /etc/fstab

More info on [mount points](http://www.linfo.org/mount_point.html)
Easy, graphic introduction to [partitioning and mount points](
https://www.linuxnix.com/what-is-a-mount-point-in-linuxunix/)
Another introduction to [Linux disk management](
https://www.linuxnix.com/disk-management-in-linux/)


### System wide available executables

    /usr/bin

## Other important system folders

    /proc


## Linux system environment variables
- `$PATH` ... contains all directories which are included when looking for an executable
- `$HOME` ... contains absolute path to the home folder
- `$USER`
- `UID`


###  Global searchpath variable $PATH:

- display all directories currently included in the searchpath:

        echo $PATH

- permanently add directories to `$PATH` by editing `/etc/profile` or `$HOME/.profile` by adding

        export PATH=$PATH:/[directory of choice]

- Symlinks for the operating system:

        /etc/alternatives

- Custom packages and libraries can usually be found in one of the following folders:

        /opt/
        /usr/local/include/
        /usr/local/lib/ & /usr/local/lib/pkgconfig/
        /usr/share/
        /home/[user]/bin/


## Adding custom executable paths in Linux:

- Set up a bin folder that is included in the Linux `$PATH` which contains all the links to starting programs.
- Check out this link for [more information](http://www.troubleshooters.com/linux/prepostpath.htm).
- Folders can easily be added to the beginning, and the end of the variable -
depending on where the application is first found, this will be executed.

Example:
In folder ~ (absolute /home/CurrentUser in our example)

    mkdir bin

Check if path has been automatically added by linux:

    cat $PATH

If not, then execute the following to recompile the .profile file:

    source .profile

Check path again

    cat $PATH

If its still not in there, then add it manually to the beginning of the `$PATH`:

    export PATH=/home/CurrentUser/bin:$PATH

Create symbolic links to executables in custom bin folder. As example add startup shell script of application activator
can be used to easily switch between different distributions of the same application

    cd bin
    ln -s /home/CurrentUser/work/software/activator-1.2.12/activator activator


## Even more useful Bash commands:

### wc (word count)

- counts lines, words and letters within a file

  ```bash
  wc filename 

  e.g.
  [chris@troll work]wc shopping_list.txt
  ```

### top (display active processes)

- Displays all processes running on the currently used machine.
- Exit by pressing `q`

### ps (running process display)

- report a snapshot of currently running processes / programs

  ```bash
  ps

  # list all processes, display in user oriented format
  ps aux
  # list all processes, sort by CPU usage
  ps aux | sort -rnk
  # list all processes, sort by Memory usage
  ```

### stat - file information

- print information about a specific file

      stat [filename]

### nmap - scan domain for open ports

- to check if a server is secure or has open ports, use `nmap`

  ```bash
  nmap [domain]

  # e.g.
  nmap example.com
  ```

### Compression / uncompression of files

- Use `gzip` or `tar` for compression related activities
- Please refer to the manual for details


### Programs for text file handling

- `sort` ... Sorts standard input then outputs the sorted result on standard output.
- `uniq` ... Given a sorted stream of data from standard input, it removes 
duplicate lines of data (i.e., it makes sure that every line is unique).
- `fmt` ... Reads text from standard input, then outputs formatted text on standard output.
- `pr` ... Takes text input from standard input and splits the data into pages with page breaks, 
headers and footers in preparation for printing.
- `head` ... Outputs the first few lines of its input. Useful for getting the header of a file.
- `tail -f` ... Outputs the last few lines of its input. Useful for things like getting the most 
recent entries from a log file.
- `tr` ... Translates characters. Can be used to perform tasks such as upper/lowercase conversions 
or changing line termination characters from one type to another (for example, converting DOS text files 
into Unix style text files).
- `grep` ... Examines each line of data it receives from standard input and outputs every line that contains 
a specified pattern of characters. Find some neat examples [here](http://www.panix.com/~elflord/unix/grep.html)
- `sed` ... Stream editor. Can perform more sophisticated text translations than tr.
- `awk` ... An entire processing language designed for filtering text files, 
more [here](http://www.vectorsite.net/tsawk.html)


## Root access by using `sudo`
[Introduction to sudo](https://www.linux.com/learn/tutorials/306766:linux-101-introduction-to-sudo)

In a nutshell `sudo` is the commandline way to grant a user root access for the following command 
e.g. when installing a software package. It will require a password that is associated with a user 
which has root access.

    sudo [command]
    [sudo] password for [username]:


## Installing packages by using apt (Advanced Packaging Tool)
[Quick apt-get overview](https://en.wikipedia.org/wiki/Advanced_Packaging_Tool)

When working on Debian based Linux systems, apt-get is a convenient way to download and install software packages.
For most of the packages root access is required which means using `sudo apt-get [command]`.

- Update the index to be up to date with all the packages that can be installed via apt-get

        sudo apt-get update

- Install a package e.g. the terminator linux terminal, which is an awesome linux terminal

        sudo apt-get install terminator

- Install a package that is not handled via the normal apt-get package list e.g. the java8 distribution: 
This requires to manually add a repository to the apt-get list of installable packages, update the repository and the install the package.

        sudo add-apt-repository ppa:webupd8team/java
        sudo apt-get update
        sudo apt-get install oracle-java8-installer

- Print installed packages to terminal

        apt --installed list

        # grep to narrow down for specific packages
        apt --installed list | grep "somePackage"

- Display information for specific installed packages (requires exact package name)

        dpkg -s <packagename>

        # or
        dpkg-query -l <packagename>


## Using SFTP with the file browser (files/nautilus)
- ctrl + l
- enter `user@url` ... e.g. `nix@projects.g-node.org`
- enter pass phrase
 

## Finding where a program is installed

    which [program name]

## File operations

- `touch fileName` ... create file "fileName"
- `echo "text" > fileName` ... Overwrite file
- `echo "text" >> fileName` ... Add to file after existing content

## File permissions

- `chmod [options] [permissions] [filename]` ... change file permissions

### Change permissions to read, write and delete for everyone:

    chmod 777 [filename]

Find detailed description and examples [here](http://www.computerhope.com/unix/uchmod.htm)

### Change file permission to executable

    chmod +x [filename]

### Change group permissions
e.g. add write permission to group

    chmod g+w [filename]


# Random usage notes

How to figure out if anyone is connected to a service:

    /var/log/apache2/other_vhosts_access.log
    
    # e.g.
    cat /var/log/apache2/other_vhosts_access.log | grep "GET /login"

Or connect to the web service docker container and run

    watch ss

Connect to one host via another one that is accessible from outside a network

    ssh -A -J username@gateway.org username@[ip address of target in closed network]

An entry in `~/.ssh/config` can automate this process:

    # entry in config file
    Host [hostname]
        User [Username]
        HostName [IP of target machine]
        Proxyjump proxyuser@[proxy IP]

    # ssh and scp should now work directly without providing the proxy
    ssh [username]@[hostname]
    scp [file] [username]@[hostname]:/target/directory

Find out which operating system is running

    uname -a
    lsb_release -a
    cat /etc/*_version
    cat /etc/*-release

Creating dummy files of various sizes with `dd`

    # Create a 1MB file
    dd if=/dev/zero of=[filename] bs=1024 count=0 seek=1024

    # Create a 100MB file
    dd if=/dev/zero of=[filename] bs=1024 count=0 seek=$[1024*100]


## Using different java versions

Currently, there are a couple of java version from two main distributors (Oracle, OpenJava)
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

If you are running sbt projects, and you ever get errors along the line:

'The java installation you have is not up to date
Activator requires at least version 1.6+, you have
version [xyz]'

then you need to switch your java alternatives and reset the JAVA_HOME environment
variable and make sure the variable properly set via `.profile` or `.bash_alias`

e.g. 

    JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64/
    # or 
    JAVA_HOME=/usr/lib/jvm/java-12-oracle/


## Adding additional fonts

The following notes are true for Ubuntu 18

- create a folder in `/usr/share/fonts/truetype/newfonts`
- move any new `.ttf` font files into this folder
- the system should automatically make the new fonts available
- you can check whether they have been added via


        fc-list | grep [name of new font]

- if a font has not been properly added, the font cache might need to
  be refreshed; use the `fc-cache` command in this case.


## SymLinks (Symbolic links) to files or folders

### Create Symlink (symbolic link)

    ln -s [target-filename] [symbolic-filename]

This creates a symbolic link named `[symbolic-filename]` that points to `[target-filename]`
NOTE: ALWAYS use the whole path as `[target-filename]`, do not use relative terms.

    ln -s /home/currentUser/tmp/testLinks/hurra.txt ../hurraLink

### Delete Symlink
Symlinks can simply be deleted by rm. This will not touch the file the link points to.

    rm hurraLink

### Read a link

To show where a link actually leads to use:

  ```bash
  readlink [linkName]
  # e.g. using the link from above
  readlink hurraLink
  ```

## Find text in files using grep

- Find text "NoResultsException" in all files of all subfolders (-R) of the current folder (.)
and print the line number where the match has been found (-n).

        grep -Rn "NoResultsException" .


## netstat: check connections and available sockets
netstat - Print network connections, routing tables, interface statistics, masquerade connections, 
              and multicast memberships

- `netstat -p`      ... show all connections with their program name and pid
- `netstat -l`      ... check connections
- `netstat -lt`     ... check connections showing their local address
- `netstat -ltupn`  ... show all connections with their ports, program name and pid

## iptables: IPv4/v6 inspection and packet filter rules

Interesting to manage forwarding rules

    iptables --help

## List USB devices
    lsusb

- `lsusb` lists all connected usb devices
- `lsusb -v` does the same as above, but includes more details about the devices
- `lsusb -d [vendorID]:[deviceID] -v` gives a verbose description of just the specified device


## Process handling
### Running processes

Use `htop` to display running processes
- press `t` for a treeview of all running processes
- F3 to search for a specific process

### Ending processes

- use `kill` to end a process via its PID; this will leave child processes in a process hierarchy running!

        kill -SIGTERM [PID]

- `kill` can end full process trees

        kill -SIGTERM -- [PID]

## base64

base64 encoding from the commandline

    base64 <<< sometextstuff

base64 decoding from the commandline

    base64 -d <<< c29tZXRleHRzdHVmZgo=

The base64 RFC with the nittygritty details can be found [here](https://tools.ietf.org/html/rfc4648#section-5). 


## Bashrc
- The hidden `.bashrc` file is a script that is executed, whenever a new terminal session is started.
- The file contains configurations for the terminal session. An example would be the shorthand `ll` instead of `ls -l`
- There are two main bashrc files
- The first is found in `/etc/bash.bashrc`, this one applies to all shell sessions
- The second one is found in `/home/[user]/.bashrc`. This one applies only to non-login shell sessions.


## Linux server crash course:

- client and server are both processes, that communicate with each other via SOCKETS.
- processes can only communicate, if they are in the same ADRESS DOMAIN and have the same SOCKET TYPE.
- the two main different address domains are the UNIX DOMAIN (processes live in a common file system) and the INTERNET DOMAIN
(processes live on two hosts anywhere in the internet)
- the address of a socket in the unix domain is a CHARACTER STRING entry in the file system
- the address of a socket in the internet domain is the internet adress of the host machine which is the IP ADDRESS (unique 32bit address).
- Each internet socket address needs a port number on its host (16bit unsigned integer).
- There are port numbers reserved for Unix standard services, port numbers above 2000 are available.
- The mainly used socket type is the STREAM SOCKET. Stream sockets TCP (transmission control protocol).

Find a nice introduction [here](http://www.linuxhowtos.org/C_C++/socket.htm)

### Check automatic server updates 

Check `less /var/log/unattended-upgrades/` whether automatic updates are run.
These can cause problems on a server if they run unchecked.


## Ubuntu keyboard shortcuts making our life easier

- find an extensive list [here](http://askubuntu.com/questions/28086/what-are-unitys-keyboard-and-mouse-shortcuts).

- alt + tab ... switch between open applications in the current workspace
- alt + ^ ... switch between open windows of the current application in the current workspace


# Unix in depth

## Partitions

- find information [here](https://en.wikipedia.org/wiki/Disk_partitioning) 
and [hier](https://de.wikipedia.org/wiki/Partition_(Datentr%C3%A4ger))


## Inodes

- inodes reside in a specially reserved block of the memory - which is usually 10% of memory capacity.
- inodes contain information about files and directories
    - ownership (group and userid)
    - access mode
    - file type
    - device id of the device containing the file
    - size of the file in bytes
    - ctime ... when was the inode last changed
    - mtime ... when was the file last changed
    - atime ... when was the file last accessed
    - link count (how many hard links point to the inode)
    - pointers to datacluster - can also be a pointer to a cluster further pointing to the actual data 
    (if the data is too extensive for one pointer in the inode)
- each inode is identified by an integer number

        // identify a files inode number
        ls -i [filename]

- one file can be linked multiple times. if a link points to an inode number, then the link is a `hard link` 
- if an inode is not referenced by a link, the corresponding data is removed from disk (???) when it is 
no longer used by any process. (or is it rather, that the pointers to the datacluster is removed & therefore free to be written to again?)
- A specific part of the filesystem, the `superblock` contains information about where the inodes themselves are found. 
- when a file is opened the following happens:
    - file system driver reads the superblock to get access to the inodes
    - the root of the inode directory is opened and the inode of the required directory where 
    the file resides in is looked up
    - the inode of the directory is used to look up the inode of the file
    - the inode of the file contains the link to the actual data of the file.

- find wikipedia information [here](https://en.wikipedia.org/wiki/Inode) and [hier](https://de.wikipedia.org/wiki/Inode)


# Move to fitting paragraph

## Redirecting to /dev/null

When redirecting to `/dev/null`, any command line output to `STDOUT` and `STDERR` from a program will be suppressed.

    e.g. the output from wget will be suppressed
    wget -O libgit2.tar.gz -o /dev/null https://github.com/libgit2/libgit2/archive/v0.24.5.tar.gz


## Access System Error logs

Print all logs since the last restart:

    sudo journalctl -b -1


## Hardware information

Display CPU information

    lscpu
    # or
    cat /proc/cpuinfo

Display memory information

    lsmem
    # or
    cat /proc/meminfo

Display attached hardware

    lspci

Display attached usb devices

    lsusb

Display hostname (computer name within network)

    hostname
    # or
    hostnamectl

- `hostnamectl` also displays whether the machine is a physical or a virtual machine.

Display operating system details

    uname -a
    # or
    lsb_release -a
    # or
    hostnamectl

Display mac address

    ip link
    # or
    ifconfig -a

# Command line package update

Update the package index:

    sudo apt-get update

Upgrade installed packages

    sudo apt-get upgrade

Upgrade core packages

    sudo apt-get dist-upgrade


# Command line reboot

Reboot a machine from the command line

    sudo shutdown -r now
    # or
    sudo reboot

## File encryption

Use openssl to encrypt files with a password

- encrypt file
```bash
openssl aes-256-cbc -a -salt -iter 5 -in [plain file] -out [encrypted file].enc
```

- decrypt file
```bash
openssl aes-256-cbc -d -a -iter 5 -in [encrypted file] -out [output plain file]
```


## Safely removing files

First make sure that you hard drive is not an SSD. The methods described below all
overwrite the file content multiple times. On SSDs this not only does not properly
overwrite the actual file data but also lowers the life-time of the device itself.

If you are working on an SSD you can either wipe the whole drive OR work on encrypted
files from the start, if they contain sensitive data.

To garbage collect blocks containing deleted files, look up the `fstrim` command.

### Safe file removal from an HDD

To ensure files are properly deleted, the following CLI commands can be installed and used:

- shred
- wipe
- secure-delete
  - srm ... secure remove
  - sfill ... overwrite free hard drive space
  - sswap ... cleanse swap space
  - sdmem ... cleanse RAM

For an introduction check the following [article](
https://www.howtogeek.com/425232/how-to-securely-delete-files-on-linux/)


## Ubuntu system upgrade

Upgrade an ubuntu system from one LTS to the next by using the following

    sudo apt update
    sudo apt upgrade
    do-release-upgrade

# Exercises
## User handling
-[ ] create user
-[ ] add to group sudo, docker
-[ ] switch user, test sudo, create home ssh
-[ ] remove from one group
-[ ] delete user
-[ ] remove home

## system info
-[ ] display machine information
-[ ] display disk space
-[ ] list crontab
-[ ] access system logs

## session handling
-[ ] create, detach and re-enter a detachable session using screen
