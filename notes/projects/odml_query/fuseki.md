## Fuseki documentation
- some setup documentation
- http://www.ddmore.eu/sites/ddmore/files/Fuseki_Server_Installation_0.pdf

## Basic setup
To provide the appropriate prefix there needs to be an edit in:

    FUSEKIHOME/webapp/js/app/qonsole-config.js

adding the line `"odml":     "https://g-node.org/odml-rdf#"` where appropriate.

- fuseki setup
    ```bash
    wget http://archive.apache.org/dist/jena/binaries/apache-jena-fuseki-3.8.0.tar.gz
    tar -xf apache-jena-fuseki-3.8.0.tar.gz
    cd apache-jena-fuseki-3.8.0
    ```

- make sure a suitable run directory is already available somewhere
    ```bash
    export FUSEKI_BASE=/home/$USER/Chaos/DL/fuseki
    ```

Use the following users and permissions to prohibit unwanted modification of 
data via the webinterface in `shiro.ini`.

```bash
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
/specific_file.htm = authcBasic,roles[graphupload]

# Everything else
/**=anon
```

## Docker build
```bash
docker build -t fuseki .
docker image ls
docker run -p 4044:4044 -it -v /home/$USER/Chaos/DL/fuseki:/content fuseki

docker run -dit --rm --name fuseki_bee -p 4044:4044 -v /home/$USER/Chaos/DL/fuseki:/content fuseki
```

## Running fuseki
- starting server at port 3030 from fuseki root:
    ```bash
    ./fuseki start
    ```
- stopping server:
    ```bash
    ./fuseki stop
    ```
- starting the server using `fuseki-server`:
    ```bash
    ./fuseki-server --port=3033
    ```
- starts the server in the background; to stop the server, find the PID and send term signal
    ```bash
    ps aux | grep fuseki
    kill -s 15 [fuseki_pid] 
    ```

## Installing dependencies

- make sure apache is there; install otherwise
    ```bash
    sudo apt-get update
    sudo apt-get install apache2
    ```
- make sure certbot is available, install otherwise
    ```bash
    sudo apt install certbot
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
- add a sites-available entry
    ```bash
    sudo vim /etc/apache2/sites-available/meta.g-node.org
    ```
- stop the apache server before setting up an encryption
    ```bash
    sudo service apache2 stop
    ```
- setup a certificate for the service domain name
    ```bash
    sudo certbot certonly
    ```
- deactivate the default encryption and add the new one
- start apache
    ```bash
    sudo service apache2 start
    ```
- if necessary [install docker-compose](https://docs.docker.com/compose/install/)
    ```bash
    sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    ```

### Initialize the server

Use the `meta_init.sh` script to initialize the meta server:
```bash
 sudo bash meta_init.sh [required_files_dir]
```
Before running the script make sure all required files
are available in a directory and the appropriate server URL and docker image
have been set in the respective files.

The script will automatically setup the required folder structure,
copy any required files, download and start the appropriate docker image.

The script supports two different setup schemes and will ask the user
at the very beginning which one should be run:

a) Setup an empty server (Option: `Initialize meta server from backup files (yes/no): no`)
   In this case the directory where the script is run from requires
   the following files:
   - `.env` containing required docker environmental variables
   - `docker-compose.yml` containing the docker setup
   - `shiro.ini` containing the security settings of the fuseki server and ideally an updated admin password
   - `meta_backup.sh` ideally already set as an executable script
   This will create an empty fuseki meta server and will try to create
   a persistent empty database named `metadb`.
b) Setup a server from an existing database (Option: `Initialize meta server from backup files (yes/no): yes`)
   In this case the required files directory needs to contain the
   additional file `config.ttl` and the directories `configuration` and `database` containing
   the graph database from an earlier backup.
c) NOTE: when run as a Docker container, the fuseki server will create multiple `tdb.lock` files 
     for the server setup and each hosted graph. These lock files contain the PID the fuseki server runs
     as and is not cleaned up when the docker container is stopped! Since these files are linked 
     to the outside to make the graph persistent, it can happen, that on an update to the docker container
     the PID of the running server will no longer match the PID of the lock files.
     Due to this the Docker container will remove all `tdb.lock` files on startup.

Both init schemas will by default create all required directories in
`/web/meta`, create and setup the required user, copy all required files and
set the required permissions and pull and start the specified docker container.


### Backup Cronjob

- make sure zip is installed; install otherwise...
    ```bash
    sudo apt-get update
    sudo apt-get install zip
    ```
- make sure fdupes is installed, install otherwise...
    ```bash
    sudo apt-get install fdupes
    ```
- make sure the meta_backup script is executable
    ```bash
    chmod +x meta_backup.sh
    ```
- adjust the source and target directories as well as keyname and user as required 
  in `meta_backup.sh` which by default can be found at `/web/meta/scripts`.

- run `meta_backup.sh` at least once manually before setting up a cronjob
  to ensure all variables are valid and the ssh keys are properly setup for usage.

- add a crontab job for meta as the root user
    ```bash
    sudo crontab -e
    ```
- Backup every 10min and add status output to a logfile:
    ```bash
    */10 * * * * /web/meta/scripts/meta_backup.sh 2>&1 >> /web/meta/log/meta_backup.log
    ```
- logs about cronjobs can be checked via:
    ```bash
    grep CRON /var/log/syslog
    ```
- setup required users and folders

- create user fuseki and add to docker group
    ```bash
    sudo useradd -M -G docker meta
    ```
- if it already exists, we can add it to the docker group
    ```bash
    sudo usermod -a -G docker meta
    ```
- disable login for user
    ```bash
    sudo usermod -L meta
    ```
- create work folder
    ```bash
    mkdir -p /web/meta
    ```
- change permissions so our process can write to this folder when starting the service
    ```bash
    sudo chown -R meta:docker /web/meta
    ```
- run docker command:
    ```bash
    METAIMG=gnode/meta:latest
    METANAME=meta
    # use the port only in local tests, not for deployment!
    docker run -dit --rm --name $METANAME -p 4044:4044 -v $F_HOME:/content $METAIMG
    ```

## Fuseki version notes

To obtain the latest version run the following

```bash
docker run -dit --rm --name metabla -p 4044:4044 gnode/meta:latest
docker exec -it metabla /bin/sh
sh ./fuseki-server --version
```

## Data upload notes:

Currently, upload of larger files causes a Bad Gateway 502 error.

Checking `sudo watch tail /var/log/apache2/error.log` returns the message

     [proxy_http:error] [pid 21173] [client <IP>] AH01097: pass request body failed 
     to <IP> (<IP>) from <IP> (), referer: https://meta.dev.g-node.org/dataset.html?tab=upload&ds=/metadb

Updating the timeout in the apache config file does not yield any positive result:

    ProxyPass / http://172.23.0.3:4044/ connectiontimeout=180 timeout=180

Might also be a problem with an upload size limit (`LimitRequestBody`) or with using an
    apache like server behind an apache and we need to try using a different apache 
    proxy module - using `mod_proxy_ajp` instead of `mod_proxy`:

    https://stackoverflow.com/questions/13003282/apache-multipart-post-pass-request-body-failed

### Example curls
```bash
curl -X POST --data "dbType=tdb&dbName=metadb" localhost:4044/$/datasets

curl -i -X POST -H "Content-Type:application/n-quads" --data-binary "@/home/$USER/Chaos/staging/fuseki/setup/new2.nq" localhost:4044/$/new2/update

curl -X POST localhost:4044/$/backup/metadb
```

## Code notes:

The routes for the webapp seem to be defined in

    jena/jena-fuseki2/jena-fuseki-webapp/src/main/webapp/WEB-INF/web.xml

## Access tabs - remove and use as hidden feature:
- http://meta.g-node.org:3030/manage.html
- http://meta.g-node.org:3030/dataset.html?tab=info
- http://meta.g-node.org:3030/dataset.html?tab=edit
- http://meta.g-node.org:3030/dataset.html?tab=upload

## Apache Sites available for meta 
```xml
<VirtualHost *:80>
    ServerName meta.dev.g-node.org
    ServerAdmin dev@g-node.org
    
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
    
    RewriteCond %{SERVER_NAME} =meta.dev.g-node.org
    RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>

<VirtualHost *:443>
    ServerName meta.dev.g-node.org
    ServerAdmin dev@g-node.org
    
    SSLEngine On
    SSLCertificateFile /etc/letsencrypt/live/meta.dev.g-node.org/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/meta.dev.g-node.org/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf
    
    ProxyPreserveHost    On
    ProxyRequests Off
    ProxyPass / http://172.23.0.3:4044/
    ProxyPassReverse / http://172.23.0.3:4044/
    <IfModule mod_headers.c>
        <FilesMatch ".(eot|otf|svg|ttf|woff|woff2)$">
            Header set Access-Control-Allow-Origin "*"
        </FilesMatch>
    </IfModule>
</VirtualHost>
```

# Docker compose .env file
```bash
COMPOSE_PROJECT_NAME=meta
F_ROOT=/web/meta
METAIMG=gnode/meta
```

# Docker compose file
```yaml
version: "3.3"
services:

  meta:
    image: ${METAIMG}
    networks:
      metanet:
        ipv4_address: 172.23.0.3
    volumes:
      - content:/content:rw
    restart: always
    stdin_open: true

volumes:
  content:
    driver: "local"
    driver_opts:
      type: "none"
      o: "bind"
      device: "${F_ROOT}/service"

networks:
  metanet:
    ipam:
      driver: default
      config:
        - subnet: 172.23.0.0/16
```

## Fuseki initialisation script
```bash
#!/usr/bin/env bash
# Script to initialize a fuseki server
set -eu
# Required paths, files and folders
F_USER=meta
F_URL=localhost:4044

F_ROOT=/web/meta
F_HOME=$F_ROOT/service
F_ENV=$F_ROOT/env
F_BACKUP=$F_ROOT/backup
F_SCRIPTS=$F_ROOT/scripts
F_LOG=$F_ROOT/log

# Fuseki specific files and folders
SHIRO=shiro.ini
BACKUPSCRIPT=meta_backup.sh

CFILE=config.ttl
CDIR=configuration
DB=databases

METAIMG=gnode/meta

echo "Running fuseki meta service setup script ..."

if [[ $# != 1 ]]; then
    echo "... Please provide the path to the required files folder"
    exit 1
fi

REQFILES=$1
```

### Define initialization scheme
```bash
echo
echo -n "Initialize meta server from backup files (yes/no): "
read -s FROMBACKUP
echo $FROMBACKUP

if [[ ! $FROMBACKUP == "yes" && ! $FROMBACKUP == "no" ]]; then
    echo "... Please enter 'yes' or 'no'"
    exit 1
fi

if [[ $FROMBACKUP == "yes" ]]; then
    echo "Restoring from backup ..."
else
    echo "Initializing empty server ..."
fi

echo
echo "Checking required files and directories ..."
if [[ ! -f "$REQFILES/$SHIRO" ]]; then
    echo "... Could not find file ${REQFILES}/$SHIRO"
    exit 1
fi

if [[ ! -f "$REQFILES/$BACKUPSCRIPT" ]]; then
    echo "... Could not find file ${REQFILES}/$BACKUPSCRIPT"
    exit 1
fi

if [[ ! -f "$REQFILES/.env" ]]; then
    echo "... Could not find file ${REQFILES}/.env"
    exit 1
fi

if [[ ! -f "$REQFILES/docker-compose.yml" ]]; then
    echo "... Could not find file ${REQFILES}/docker-compose.yml"
    exit 1
fi

if [[ $FROMBACKUP == "yes" ]]; then
    if [[ ! -f "$REQFILES/$CFILE" ]]; then
        echo "... Could not find file ${REQFILES}/$CFILE"
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
fi

echo
echo "Pulling docker image ${METAIMG} ..."
docker pull $METAIMG

echo
echo "Creating required folders ..."
mkdir -pv $F_HOME
mkdir -pv $F_ENV
mkdir -pv $F_BACKUP
mkdir -pv $F_SCRIPTS
mkdir -pv $F_LOG

echo
echo "Copying required files ..."
cp -v $REQFILES/$SHIRO $F_HOME/$SHIRO
cp -v $REQFILES/$BACKUPSCRIPT $F_SCRIPTS/$BACKUPSCRIPT
cp -v $REQFILES/.env $F_ENV/.env
cp -v $REQFILES/docker-compose.yml $F_ENV/docker-compose.yml

if [[ $FROMBACKUP == "yes" ]]; then
    cp -v $REQFILES/$CFILE $F_HOME/$CFILE
    cp -rv $REQFILES/$CDIR $F_HOME/$CDIR
    cp -rv $REQFILES/$DB $F_HOME/$DB
fi
```

### Create dedicated "meta" user and make sure its part of the "docker" group
```bash
echo
echo "Handling required user ${F_USER} ..."
if id $F_USER >/dev/null 2>&1; then
    echo "... User ${F_USER} already exists"

    VAR=$(id ${F_USER} | grep docker)
    if [[ -z $VAR ]]; then
        echo "... Adding ${F_USER} to the docker group"
        usermod -a -G docker $F_USER
    fi
else
    useradd -M -G docker $F_USER
fi
```

### Disable login for meta user
```bash
usermod -L $F_USER
```

### Change ownership of main folder to enable docker access
```bash
chown -R $F_USER:docker $F_HOME

echo
echo "Starting meta service ..."

cd $F_ENV
docker-compose -p meta up -d

echo
echo "The fuseki meta service is running ..."

if [[ ! $FROMBACKUP == "yes" ]]; then
    # Read password required to set up database from shiro file
    PASS=$(grep -Po "(?<=admin=).*$" $F_HOME/${SHIRO})

    # Create a new, empty database
    sleep 5
    echo
    echo "Creating empty database 'metadb' at ${F_URL} ..."
    echo
    curl -v -u admin:${PASS} -X POST --data "dbType=tdb&dbName=metadb" ${F_URL}/$/datasets
    echo

    echo "Database created; data needs to be uploaded manually ..."
    echo
fi
```

## Backup script fuseki_backup.sh
```bash
#!/usr/bin/env bash

set -eu

echo "Running fuseki meta service backup ..."

F_ROOT=/web/meta
F_HOME=$F_ROOT/service
F_BACKUP=$F_ROOT/backup

F_URL=localhost:4044
F_DB=metadb

# Backup all required files and folders for a restore action
BACKDATE=$(date +"%Y%m%dT%H%M%S")
ZIPNAME=$F_BACKUP/meta_$BACKDATE

SHIRO=$F_HOME/shiro.ini

# zip all required folders without file attributes to allow deduplication
echo
echo "Running file based backup ..."
(cd ${F_HOME} && zip -r -X $ZIPNAME shiro.ini config.ttl configuration/* databases/*)

# Trigger db backup to file; read db password from shiro file
echo
echo "Running graph based backup ..."
PASS=$(grep -Po "(?<=admin=).*$" ${SHIRO})
curl -u admin:$PASS -X POST $F_URL/$/backup/$F_DB

# Make sure the graph backup is done before we run fdupes
sleep 15

# Deduplicate after backups are done
echo
echo "Running deduplication ..."
fdupes -dN $F_BACKUP
fdupes -dN $F_HOME/backups

# Make sure fdupes is done before we run an rsync
sleep 15

# Backup to gate
echo
echo "Copying archives to [target] ..."
#rsync -v -e "ssh -i [key]" -r --ignore-existing $F_BACKUP/ [user]@[target]/backups/meta/database
#rsync -v -e "ssh -i [key]" -r --ignore-existing $F_HOME/backups/ [user]@[target]/backups/meta/graph

echo
echo "The fuseki meta service backup is done ..."
echo
```
