--------------------- intermediate notes --------------------

# Networking

IP ... internet protocol
inter network communication protocol to enable communication between
two defined addresses. IPv4 addresses.

UDP ... User datagram protocol
inter network data transfer protocol. carries only checksum and the address
of the receiver. does not provide support against data loss.


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


# Linux commands and paths to rehearse

watch

useradd

groupadd

chown

chmod

ssh

scp

systemctl [start stop]

journalctl -f

apache2 [start stop reload restart]

a2ensite a2disite; a2enmod

certbot

nmap

ss

rsync


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

Deduplicate files

    fdupes [dir]
    
    # remove duplicates without asking
    fdupes -dN [dir]


/etc/apache2
/etc/letsencrypt

/etc/group
/etc/passwd

/home/[uname]/.ssh



# Docker variants


docker build -t [containername:label] .

docker run --rm -dit

docker ps

docker images

docker rm [container]

docker rmi [image]

docker logs -f [container]

docker exec -it [container] /bin/bash


docker-compose -p [projectname] up -d

## Notes
- when using volumes, the directories on the host system need to be assigned either 
  to a user that is in the user group or should be assigned to the docker group. 


# Postgres

psql -U[username] -d[dbname]

\dn ... list schemas
\dt ... list tables
\d [table] ... display details of [table]


# Random usage notes

How to figure out if anyone is connected to a service:

    /var/log/apache2/other_vhosts_access.log
    
    # e.g.
    cat /var/log/apache2/other_vhosts_access.log | grep "GET /login"

Or connect to the web service docker container and run

    watch ss
