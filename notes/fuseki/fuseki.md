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

    sudo useradd -M -G docker gca

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

Code notes:

The routes for the webapp seem to be defined in

jena/jena-fuseki2/jena-fuseki-webapp/src/main/webapp/WEB-INF/web.xml

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
