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

