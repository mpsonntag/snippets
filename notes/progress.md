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

gunzip

tar


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
