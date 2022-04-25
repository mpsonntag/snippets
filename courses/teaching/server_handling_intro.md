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
