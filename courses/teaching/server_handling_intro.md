# Working with servers

## Basic requirements 

It's quite helpful to be familiar with the following tools and commands:

commands:
    ssh, scp, getent, groupadd, useradd, chmod, chown, usermod, ln, screen

tools:
    vim, systemctl, journalctl, crontab, apache2, letsencrypt, docker, docker-compose, rsync, curl

Basic files and directories
    
    /etc/group
    /etc/passwd

    /etc/apache2
    /etc/letsencrypt
    /var/logs
    /etc/alternatives


## Secure connection and keys 

### ssh (Secure SHell)

- Connect to another machine using secure shell; an encrypted connection to another computer within the network. 
- Logging on to another machine will most likely require a password.

        ssh [remote_machine]
        # provide username on the remote machine and appropriate password

        e.g.
        [chris@troll work]$ssh server4
        [chris@server4 ~]$

        # the login process can be sped up by already providing the username in the login command
        ssh [username]@[remote_machine]

- Notice that the name of the machine in the bash shell has changed from `troll` to `server4`
- Use the command `exit` to close the ssh connection to a remote machine.

        e.g.
        [chris@server4 ~]$exit
        [chris@troll ~]$

### scp (Secure Copy)

- Use a secure connection to copy files from or to a remote machine

        scp [remote_machine_name]:[remote_directory]/[filename] [local_directory]

        e.g.
        [chris@troll work]scp server4:/temp/work/* /home/chris/work/

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

        ssh-keygen
        enter a name (without spaces!) e.g. id_rsa_key_description
        enter a pw pr leave it empty
        // print public key
        cat id_rsa_key_description.pub

- The created key pair can be found in a hidden `.ssh` folder in the home directory, if no other location has been 
    specified.

- To retrieve the SSH fingerprint of the public key use the following:

        ssh-keygen -lf [location and name of the public key]

### SSH Key Agent

Find a nice introduction [here](
http://sshkeychain.sourceforge.net/mirrors/SSH-with-Keys-HOWTO/SSH-with-Keys-HOWTO-6.html
) 
and laugh at the passphrase.

SSH keys reside in their folder, every time they are used, the passphrase has to be entered. 
To make them available to other services without having to point services to their proper keys and 
having to enter the pass phrase all the time.

- start an ssh-agent if it is not already started (might need one of the examples below to start properly)
    - BEWARE! when starting the agent, the environment will be reset, meaning any active agent
                is stopped, the new agent will not contain any keys, any keys previously added
                have to be added again! So when in doubt, run `ssh-add -l` first.

        eval "ssh-agent"
        eval "ssh-agent -s"
        eval `ssh-agent -s`
        or
        eval $(ssh-agent)

- add key to the agent e.g. the key created in example above and enter the keys pass phrase once and never again.

        ssh-add ~/.ssh/id_rsa_key_description

- check which keys are currently managed by the ssh key agent

        ssh-add -l

- even if you have added the key to the ssh key agent, if the key with the corresponding passphrase 
    is not added to the linux keyring, it will prompt for the passphrase upon the first use of the 
    ssh key. If the option is used to store key and phrase in the keyring, this login will be
    done automatically, and the prompt will not show up again, when the key is used.

- NOTE: as an important side note, when you have a lot of keys added to your agent, it will
  try all of them against a potential server you want to log in to. If the server has a low
  authentication failure tolerance, then you will be disconnected and potentially barred from
  new attempts for a while. Usually the message `Received disconnect from [IP address] port 22:2: 
  Too many authentication failures for [username]` is a dead giveaway. This can already happen
  when you have more than three ssh keys...
  You can debug this using the verbose setting on the ssh command e.g. `ssh -v username@some.server.com` 

### Convenient ssh access by using .ssh/config

As described above, having too many different ssh keys can lead to not being able to login somewhere.
Its even easier to tell the agent which key to offer to a specific server first to avoid that dilemma.

A nice tutorial for that can be found [here](
https://nerderati.com/2011/03/17/simplify-your-life-with-an-ssh-config-file/
).

- Create a `config` file in the `.ssh` folder.
- Define a specific Host and point to the ssh key file that should be used.

    Host some.example.org
        IdentityFile ~/.ssh/id_rsa_for_example

- If you want to login at a specific port or with a different user than your current one:

Host other.site.com
    User root
    Port 4444
    IdentityFile ~/.ssh/id_rsa_for_site


## Setup user with sudo access on an SSH accessible server

Modified from [here](
https://aws.amazon.com/premiumsupport/knowledge-center/new-user-accounts-linux-instance/
).

- ssh to the server
- create new user (add password in the process)

        sudo adduser new_user

- [Optional] add user to the sudoer user group (after the user has been created)

        sudo adduser new_user sudo

- switch to new user, create .ssh folder and authorized key entry with the appropriate permissions for this user

        sudo su new_user
        mkdir /home/new_user/.ssh
        chmod 700 /home/new_user/.ssh
        touch /home/new_user/.ssh/authorized_keys
        chmod 600 /home/new_user/.ssh/authorized_keys

- open authorized keys with an editor e.g. and paste the required public key string into the file.

        vim /home/new_user/.ssh/authorized_keys
        "press i"
        "paste public key string"
        "press esc and type :x to save changes"

- [optional] change user password

        passwd

- Now the new_user should be able to ssh into the server.


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


## Installing server dependencies

### Installation and setup of Apache

- make sure apache is there; install otherwise

    ```bash
    sudo apt-get update
    sudo apt-get install apache2
    ```

- make sure all required apache modules are active

    ```bash
    sudo a2enmod rewrite
    sudo a2enmod ssl
    sudo a2enmod proxy
    sudo a2enmod proxy_http
    sudo a2enmod proxy_html
    sudo a2enmod http2
    sudo systemctl restart apache2
    ```

- make sure apache is set to restart on machine reboot

    ```bash
    # check the restart on boot status; status should read "enabled":
    # "loaded (loaded (/lib/systemd/system/apache2.service; enabled; ..."
    sudo systemctl status apache2.service
    # if it reads "disabled" run the following
    sudo systemctl enable apache2.service
    ```

- add a sites-available entry

    ```bash
    sudo vim /etc/apache2/sites-available/[domain]
    ```

### Apache setup to serve static pages

If apache is supposed to serve static pages, it might be required to add additional grants to the `/etc/apache2/apache2.conf` file. Add this information in case the apache spits out a 403 forbidden message if it should already be serving the static pages.
```bash
<Directory /path/to/served/directory/>
    AllowOverride All
    Require all granted
    Options Indexes FollowSymLinks MultiViews
    Order deny,allow
    Allow from all
</Directory>
```

### Installation and setup of certbot for SSL encryption

Compare with the [letsencrypt documentation](
https://letsencrypt.org/docs/
) for the latest state of the tool and how to use it.

- make sure that a DNS entry is available for the IP where the service should be reached.
- make sure certbot is available, install otherwise - the following script is an example
  for Ubuntu 18 using Apache2; check the [installation documentation](
  https://certbot.eff.org/
  ) for installation specifics 
  of the latest version.
    ```bash
    # cleanup previous versions
    sudo apt-get remove certbot
    sudo snap install --classic certbot
    # make sure certbot is available to all users
    sudo ln -s /snap/bin/certbot /usr/bin/certbot
    ```
- enable the required apache config - make sure all config files have the `.conf` file extension
  ```bash
  sudo a2ensite [domain]
  ```
- check that all configs are valid
  ```bash
  sudo apache2ctl configtest
  ```
- stop the apache server before setting up an encryption
    ```bash
    sudo service apache2 stop
    ```

- if this is the very first time using certbot, make sure to temporarily remove 
  the `Include /etc/letsencrypt/options-ssl-apache.conf` and `SSLCertificate...`
  lines from the apache config file.

- setup a certificate for the service domain name
    ```bash
    sudo certbot certonly --apache
    # one can also try the dry run first
    sudo certbot certonly --apache --dry-run
    ```
- alternatively set up letsencrypt certificates for a specific domain
    ```
    sudo certbot
    # Select domain name to create the certificate for e.g. own.example.org
    # Use option "Secure".
    # This creates certificate files in `/etc/letsencrypt/live/own.example.org/` 
    # and adds an apache2 sites available entry in /etc/apache2/sites-available/000-default-le-ssl.conf
    # and also enables this configuration for apache2.

    # Unload this certificate from the apache sites enabled
    sudo a2dissite 000-default-le-ssl.conf

    # Make sure the paths to the "SSLCertificateFile" and "SSLCertificateKeyFile" in
    # /etc/apache2/sites-enabled/own.example.org.conf point to the correct letsencrypt files
    # e.g. /etc/letsencrypt/live/own.example.org/fullchain.pem.

    # Then reload apache2 to make the encryption available. If this does not help yet, restart the apache
    # service and close and restart the browser.
    sudo systemctl reload apache2
    # or
    sudo systemctl restart apache2
    ```

- check the apache status; issues can arise, if the certbot apache was not shut down properly; in this case, the apache service will not restart the first time, but has to be restarted twice.
    ```
    sudo systemctl restart apache2
    ```

- Note: Browsers usually need a restart to properly accept renewed certificates.

To check whether certbot set up automatic renewals on a debian system, run the following and 
check for a certbot renewal job.

    systemctl list-timers

The systemd files can also be checked directly at `/etc/systemd/system/snap.certbot.renew.service` or `.timer`

The certificates issued can be found in the `/etc/letsencrypt/`. Usually the certificates are created in the `/etc/letsencrypt/archive` directory, the latest is symlinked to the `archive` directory from the `/etc/letsencrypt/live` directory. When used with an apache, the apache config should always point to the `live` directory; when an auto-renewal job is set up, the apache will always have access to the latest certificate.

The certificates are bound to a domain name, not to an IP address or server host key. So if the server is changed, the certificates can actually be moved to the letsencrypt folders on the new machine and can be used on the fly.


### Installation and setup of docker and docker-compose

- make sure docker is installed; if not, install docker using the official [docker documentation](
  https://docs.docker.com/engine/install/
  ).

- make sure docker is set up to use a mountpoint with sufficient space. To this end symlink the default docker container directory to a directory with sufficient space.

    ```bash
    // make sure no containers are running and stop the docker daemon
    sudo systemctl stop docker
    sudo cp -a /var/lib/docker /data/docker
    sudo mv /var/lib/docker /var/lib/docker_old
    sudo ln -s /data/docker /var/lib/docker
    sudo systemctl start docker
    ```

- make sure that the docker service will restart when the machine itself is coming up.

    ```bash
    sudo systemctl enable docker
    # check the restart on boot status; status should read "enabled":
    # "loaded (/lib/systemd/system/docker.service; enabled; ..."
    sudo systemctl status docker.service
    ```

- if required [install docker-compose](
  https://docs.docker.com/compose/install/
  )

- docker-compose can be installed via pip: make sure Python is available and pip is installed. If not install, pip first.

    ```bash
    # install pip
    sudo apt update
    sudo apt install python3-pip
    # now install docker-compose via pip
    sudo pip install docker-compose
    ```

- alternatively it can also be downloaded and made available
    ```bash
    $DOCKER_COMPOSE_VERSION=[set required version]
    sudo curl -L "https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    ```

### Apache and Docker

All docker-compose files should be set up with a fixed IP address. This way, if the machine a docker container runs on is restarted, the IP a restarted docker container is using will be the same as before the restart. The apache configuration needs to point to this specified IP address.

If for any reason this set up cannot be used and a machine or a docker container has restarted, the IP address in the apache config file has to be updated to the new IP address the docker container is now running at:

- make sure the appropriate apache2 configuration exists and is enables. It might be 
  necessary to update the apache2 configuration to the current IP of the running 
  docker container.

    ```
    # Check IP address of the current running docker container
    sudo docker inspect -f "{{ .NetworkSettings.Networks.gcanet.IPAddress }}" $DOCKER_CONTAINER_NAME

    # Check "ProxyPass" and "ProxyPassReverse" IPs in apache config file
    cat /etc/apache2/sites-enabled/[domain].conf

    # If the IP was changed, reload the apache service
    sudo systemctl reload apache2
    ```

## Server environment

### Resolving "locale" issues

It may occur, that during the installation locale messages like the one described below consistently pop up: 
```bash
perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
  LANGUAGE = "en_US:en",
  LC_ALL = (unset),
  LC_TIME = "de_DE.UTF-8",
  LC_MONETARY = "de_DE.UTF-8",
  LC_ADDRESS = "de_DE.UTF-8",
  LC_TELEPHONE = "de_DE.UTF-8",
  LC_NAME = "de_DE.UTF-8",
  LC_MEASUREMENT = "de_DE.UTF-8",
  LC_IDENTIFICATION = "de_DE.UTF-8",
  LC_NUMERIC = "de_DE.UTF-8",
  LC_PAPER = "de_DE.UTF-8",
  LANG = "C"
     are supported and installed on your system.
perl: warning: Falling back to the standard locale ("C").
perl: warning: Setting locale failed.
```

To resolve such locale issues, additionally install the required local, but keep `en-US.UTF-8` as the default setting:
```bash
sudo dpkg-reconfigure locales
```

# Additional useful tools and commands

## Session handling

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

## Checking for server ports

`nmap` ... show ports of a running server - easy security check for open ports; close any unexpected ones...

    # e.g.
    nmap example.org

## Networking commands

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

