------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

to provide the appropriate prefix there needs to be an edit in:

FUSEKIHOME/webapp/js/app/qonsole-config.js:

adding the line `"odml":     "https://g-node.org/projects/odml-rdf#"` where appropriate.

fuseki setup

    wget http://archive.apache.org/dist/jena/binaries/apache-jena-fuseki-3.8.0.tar.gz
    tar -xf apache-jena-fuseki-3.8.0.tar.gz
    cd apache-jena-fuseki-3.8.0

// make sure a suitable run directory is already available somewhere

    export FUSEKI_BASE=/home/msonntag/Chaos/DL/fuseki

Use the following users and permissions to prohibit unwanted modification of 
data via the webinterface in `shiro.ini`.

    [main]
    # Development
    ssl.enabled = false 
    
    plainMatcher=org.apache.shiro.authc.credential.SimpleCredentialsMatcher
    iniRealm.credentialsMatcher = $plainMatcher
    
    localhostFilter=org.apache.jena.fuseki.authz.LocalhostFilter
    
    [users]
    # Implicitly adds "iniRealm =  org.apache.shiro.realm.text.IniRealm"
    admin=5, administrator
    upload=6, graphupload
    
    [roles]
    administrator=*
    graphupload=*
    
    [urls]
    ## Control functions open to anyone
    /$/status = anon
    /$/ping   = anon
    # Prohibit creation of new datasets admin only
    /$/datasets   = authcBasic,roles[administrator]
    # Prohibit deletion of a graph admin only
    /$/datasets/** = authcBasic,roles[administrator]
    # Prohibit uploading of data to a graph
    /**/data = authcBasic,roles[graphupload]
    
    # Everything else
    /**=anon

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

    docker build -t fuseki .
    docker image ls
    docker run -p 4044:4044 -it -v /home/msonntag/Chaos/DL/fuseki:/content fuseki

    docker run -dit --rm --name fuseki_bee -p 4044:4044 -v /home/msonntag/Chaos/DL/fuseki:/content fuseki

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

    some setup documentation

    http://www.ddmore.eu/sites/ddmore/files/Fuseki_Server_Installation_0.pdf

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

starting server at port 3030 from fuseki root:

    ./fuseki start

stopping server:

    ./fuseki stop

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

## Setting up the server for fuseki

- make sure apache is there; install otherwise

        sudo apt-get update
        sudo apt-get install apache2

- make sure all required apache modules are active

        sudo a2enmod rewrite
        sudo a2enmod ssl
        sudo a2enmod proxy
        sudo a2enmod proxy_http
        sudo a2enmod proxy_html
        sudo a2enmod http2
        sudo systemctl restart apache2

- add a sites available entry

        sudo vim /etc/apache2/sites-available/meta.g-node.org

- make sure certbot is available, install otherwise

        sudo apt install certbot

- stop the apache server before setting up an encryption

        sudo service apache2 stop

- setup a certificate for the service domain name

        sudo certbot certonly

- deactivate the default encryption and add the new one


- start apache

        sudo service apache2 start

----------------------------------------------------

- setup required users and folders

- create user fuseki and add to docker group

    sudo useradd -M -G docker fuseki

- if it already exists, we can add it to the docker group

    sudo usermod -a -G docker fuseki

- disable login for user

    sudo usermod -L fuseki

- create work folder

    mkdir -p /web/fuseki

- change permissions so our process can write to this folder when starting the service

    sudo chown -R fuseki:docker /web/fuseki

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

Example curls, not all of them working


# this one works
curl -X POST --data "dbType=tdb&dbName=metadb" localhost:4044/$/datasets

curl -i -X POST -H "Content-Type:application/n-quads" --data-binary "@/home/msonntag/Chaos/staging/fuseki/setup/new2.nq" localhost:4044/$/new2/update

curl -X POST localhost:4044/$/backup/metadb

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

Code notes:

The routes for the webapp seem to be defined in

jena/jena-fuseki2/jena-fuseki-webapp/src/main/webapp/WEB-INF/web.xml

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

Access tabs - remove and use as hidden feature:

http://meta.g-node.org:3030/manage.html

http://meta.g-node.org:3030/dataset.html?tab=info
http://meta.g-node.org:3030/dataset.html?tab=edit
http://meta.g-node.org:3030/dataset.html?tab=upload

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

## Apache Sites available for meta 

    <VirtualHost *:80>
            ServerName meta.g-node.org
            ServerAdmin meta@g-node.org
    
            <IfModule mod_rewrite.c>
                   RewriteEngine On
                   RewriteCond %{HTTPS} off
                   RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
            </IfModule>
          <IfModule mod_headers.c>
                    <FilesMatch ".(eot|otf|svg|ttf|woff|woff2)$">
                    Header set Access-Control-Allow-Origin "*"
                    </FilesMatch>
            </IfModule>
    
    RewriteCond %{SERVER_NAME} =meta.g-node.org
    RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
    </VirtualHost>
    
    <VirtualHost *:443>
            ServerName meta.g-node.org
            ServerAdmin dev@g-node.org
    
            SSLEngine On
    
            ProxyPreserveHost    On
            ProxyRequests Off
            ProxyPass / http://172.30.0.3:3030/
            ProxyPassReverse / http://172.30.0.3:3030/
            <IfModule mod_headers.c>
                    <FilesMatch ".(eot|otf|svg|ttf|woff|woff2)$">
                    Header set Access-Control-Allow-Origin "*"
                    </FilesMatch>
            </IfModule>
                    SSLCertificateFile /etc/letsencrypt/live/meta.g-node.org/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/meta.g-node.org/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf
    </VirtualHost>

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

## init script fuseki_init_empty.sh

#!/usr/bin/env bash

# Script to initialize a fuseki server with an empty database

set -eu

# Required paths, files and folders
F_USER=fuseki
F_URL=localhost:4044

F_ROOT=/home/msonntag/Chaos/staging/fuseki/docker/meta
F_HOME=$F_ROOT/service

DOCKER_NAME=fuseki_bee
IMAGE=mpsonntag/fuseki:noport
SHIRO=shiro.ini

echo "Running fuseki setup script ..."
if [[ $# != 1 ]]; then
    echo "... Please provide the path to the fuseki required files folder"
    exit 1
fi

REQFILES=$1

echo "Checking required files ..."
if [[ ! -f "$REQFILES/$SHIRO" ]]; then
    echo "... Could not find file ${REQFILES}/$SHIRO"
    exit 1
fi

echo "Pulling docker image ..."
docker pull $IMAGE

echo "Creating required folders ..."
mkdir -p $F_HOME
mkdir -p $F_ROOT/backup

echo "Copying required files ..."
cp $REQFILES/$SHIRO $F_HOME/$SHIRO

# Create dedicated "fuseki" user and add it to the "docker" group
if id fuseki >/dev/null 2>&1; then
    echo "... User ${F_USER} already exists"
else
    useradd -M -G docker $F_USER
fi
# Disable login for user fuseki
usermod -L $F_USER

# Change ownership of main folder to enable docker access
chown -R $F_USER:docker $F_HOME

echo "Starting service ..."
docker run -dit --rm --name $DOCKER_NAME -p 4044:4044 -v $F_HOME:/content $IMAGE

echo "The fuseki meta service is running ..."

# Read password required to set up database from shiro file
PASS=$(grep -Po "(?<=admin=).*$" ${SHIRO})

# Create a new, empty database
sleep 5
echo "Creating empty database 'metadb' at ${F_URL} ..."
echo
curl -v -u admin:${PASS} -X POST --data "dbType=tdb&dbName=metadb" ${F_URL}/$/datasets
echo

echo "Database created; data needs to be uploaded manually ..."
echo

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

## init script fuseki_init_backup.sh

#!/usr/bin/env bash

# Script to initialize a fuseki server from a whole server backup

set -eu

# Required paths, files and folders
F_USER=fuseki
F_ROOT=/home/msonntag/Chaos/staging/fuseki/docker/test
F_HOME=$F_ROOT/service
DOCKER_NAME=fuseki_bee
IMAGE=mpsonntag/fuseki:latest

# fuseki specific required files and folders
SHIRO=shiro.ini
CFILE=config.ttl
CDIR=configuration
DB=databases


echo "Running fuseki setup script ..."
if [[ $# != 1 ]]; then
    echo "... Please provide the path to the fuseki required files folder"
    exit 1
fi

REQFILES=$1

echo "Checking required directories and files ..."
if [[ ! -f "$REQFILES/$CFILE" ]]; then
    echo "... Could not find file ${REQFILES}/$CFILE"
    exit 1
fi

if [[ ! -f "$REQFILES/$SHIRO" ]]; then
    echo "... Could not find file ${REQFILES}/$SHIRO"
    exit 1
fi

if [[ ! -d "$REQFILES/$CDIR" ]]; then
    echo "... Could not find directory ${REQFILES}/$CDIR"
    exit 1
fi

if [[ ! -d "$REQFILES/$DB" ]]; then
    echo "... Could not find directory ${REQFILES}/$DB"
    exit 1
fi

echo "Creating required folders ..."
mkdir -p $F_HOME
mkdir -p $F_ROOT/backups

echo "Copying required files ..."
cp $REQFILES/$SHIRO $F_HOME/$SHIRO
cp $REQFILES/$CFILE $F_HOME/$CFILE
cp $REQFILES/$CDIR $F_HOME/$CDIR
cp $REQFILES/$DB $F_HOME/$DB

# Create dedicated "fuseki" user and make sure its part of the "docker" group
echo "Handling required user ${F_USER}"
if id $F_USER >/dev/null 2>&1; then
    echo "... User ${F_USER} already exists"

    VAR=$(id fuseki | grep docker)
    if [[ -z $VAR]]; then
        echo "... Adding ${F_USER} to the docker group"
        usermod -a -G docker $F_USER
    fi
else
    useradd -M -G docker $F_USER
fi

# Disable login for user fuseki
usermod -L $F_USER

# Change ownership of main folder to enable docker access
chown -R $F_USER:docker $F_HOME

docker pull $IMAGE
docker run -dit --rm --name $DOCKER_NAME -p 4044:4044 -v $F_HOME:/content $IMAGE

echo "The fuseki service is running"

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

## Backup script fuseki_backup.sh

#!/usr/env/bin bash

set -eu

echo "Running fuseki backup ..."

F_ROOT=/home/msonntag/Chaos/staging/fuseki/docker/test

FUSEKI_BACKUP=$F_ROOT/backup
F_HOME=$F_ROOT/service
F_URL=localhost:4044
FUSEKI_DB=metadb

# Pack up all required files and folders
BACKDATE=$(date +"%Y%m%dT%H%M%S")
ZIPNAME=$FUSEKI_BACKUP/fuseki_$BACKDATE

SHIRO=$F_HOME/shiro.ini
CONF=$F_HOME/config.ttl
DBCONF=$F_HOME/configuration/*
DB=$F_HOME/databases/*

zip -r -X $ZIPNAME $SHIRO $CONF $DBCONF $DB

# Trigger db backup to file

# [xxx] will need auth soon 
curl -X POST $F_URL/$/backup/$FUSEKI_DB

# deduplicate after backups are done
fdupes -dN $FUSEKI_BACKUP
fdupes -dN $F_HOME/backups

# [xxx] Add scp to offsite backup server
