### GCA-Web initial setup script

- preparation: set up required folders, copy backup database sql, figures and play config folder

        # Home folder containing data base, config files and figures
        GCAHOME=/web/gca

        # Set up project data base folders 
        GCAPGRESDB=$GCAHOME/postgres/
        GCAPGRESSCRIPTS=$GCAHOME/scripts/

        # Play framework setup
        GCACONF=$GCAHOME/conf/
        GCAIMAGES=$GCAHOME/images
        GCAFIG=$GCAIMAGES/figures/
        GCAFIGMOBILE=$GCAIMAGES/figures_mobile/

        # Create all required directories
        mkdir -p $GCAPGRESDB
        mkdir -p $GCAPGRESSCRIPTS

        mkdir -p $GCACONF
        mkdir -p $GCAFIG
        mkdir -p $GCAFIGMOBILE
        mkdir -p $GCAHOME/backup

        # MANUAL PART
        # copy the GCA backup script as `backup.sql` into folder `/web/gca/scripts`
        #   e.g. sudo su gca -c 'cp /home/backup/gca/postgres/dump.sql /web/gca/scripts/backup.sql'
        # copy figures into folder `/web/gca/figures`
        #   e.g. sudo su gca -c 'cp /home/backup/gca/figures/* /web/gca/images/figures/'
        # Add the file `application.prod.conf` with all required settings to `/web/gca/conf`;
        #   see notes for details and get it from the gca gin repository.
        #   e.g. sudo su gca -c 'cp /home/backup/gca/conf/application.prod.conf /web/gca/conf/application.prod.conf'

- define and fetch the proper docker containers

        GCAPGRESIMG=postgres:11
        GCAIMG=mpsonntag/gca-web:latest
    
        sudo docker pull $GCAPGRESIMG
        sudo docker pull $GCAIMG

- Make sure the folder `$GCAPGRESSCRIPTS` has a mounted docker-entrypoint folder containing the database dump 
  as a plain sql file named `backup.sql`.
  The docker command needs to be run twice, the first one sets up an empty postgres db, the second one starts it properly.

        GCAPGRES=pgres_gca_bee
        sudo docker run -dit --rm --name $GCAPGRES -v $GCAPGRESDB:/var/lib/postgresql/data -v $GCAPGRESSCRIPTS:/docker-entrypoint-initdb.d -p 5432:5432 $GCAPGRESIMG
        sudo docker run -dit --rm --name $GCAPGRES -v $GCAPGRESDB:/var/lib/postgresql/data -v $GCAPGRESSCRIPTS:/docker-entrypoint-initdb.d -p 5432:5432 $GCAPGRESIMG

- connect to database postgres and create the roles `play` and `roplay` as well as a `play` database,
  that shall contain our data.

        # Add password as required
        sudo docker exec -it $GCAPGRES psql -Upostgres -dpostgres -c "CREATE ROLE play WITH LOGIN PASSWORD '';"
        sudo docker exec -it $GCAPGRES psql -Upostgres -dpostgres -c "CREATE ROLE roplay WITH LOGIN PASSWORD '';"
        sudo docker exec -it $GCAPGRES psql -Upostgres -dpostgres -c "CREATE DATABASE play OWNER play;"

- run the database dump file as user play within the new database play.

        sudo docker exec -it $GCAPGRES psql -Uplay -dplay -a -f /docker-entrypoint-initdb.d/backup.sql

- stop the container

        sudo docker stop $GCAPGRES

- create a common network for our containers

        GCANET=gcanet
        sudo docker network create $GCANET

- now we start and link the gca-web container to the postgres container

        sudo docker run -dit --rm --name $GCAPGRES --network=$GCANET -v $GCAPGRESDB:/var/lib/postgresql/data -p 5432:5432 $GCAPGRESIMG

        GCA=gca_bee
        sudo docker run -dit --rm --name $GCA --network=$GCANET -v $GCACONF:/srv/gca/conf/ -v $GCAFIG:/srv/gca/figures/ -v $GCAFIGMOBILE:/srv/gca/figures_mobile/ -p 9000:9000 $GCAIMG

- NOTES:
    - make the play framework config file has the proper IP address or name of the postgres docker container set
        e.g. `db.default.url="jdbc:postgresql://172.17.0.2:5432/play"`
        or  `db.default.url="jdbc:postgresql://pgres_gca_bee:5432/play"`
    - when an update of the DB schema is required, make sure the play framework config file 
        has the persistence setting `jpa.default=defaultPersistenceUnit`.


## Create and fetch database dumps

    docker exec -it $GCAPGRES pg_dump -d play -U play -f /tmp/dump.sql
    GCADUMP=$GCAHOME/gca_dump_$(date +"%Y%m%dT%H%M%S").sql
    docker cp pgres_gca_bee:/tmp/dump.sql $GCADUMP
    gzip $GCADUMP

- and backup the figures as well

        tar -zcvf $GCAHOME/gcafig_$(date +"%Y%m%dT%H%M%S").tar.gz $GCAFIG


# Fetching conference and abstract information

- Use the python gca-client script; NOTE: the client currently only works with Python 2.
- For fetching conferences login is not required.

        ./gca-client http://abstracts.g-node.org conference [conferenceShort] > [output].json
        # example for local tests
        ./gca-client http://127.0.0.1:9000 conference BC17 > conf.dev.bc17.json

- When fetching abstracts, login is required. It needs to be provided via a netrc file:

        # Create .netrc file if it does not exist yet
        touch /home/[user]/.netrc
        # Add entry to the netrc file in the following manner:
        vim /home/[user]/.netrc
        
        machine [IP address or DNS]
        user [username]
        login [password]
        
        # example for local tests
        machine 127.0.0.1:9000
        user ms@bio.lmu.de
        password somethingSecret

        # This file must only be accessible to the logged in user; chmod if required.
        sudo chmod 600 /home/[user]/.netrc

- Now everything is set up to fetch abstracts

        ./gca-client http://abstracts.g-node.org abstracts [conferenceShort] > [output].json
        # example for local tests
        ./gca-client http://127.0.0.1:9000 abstracts BC17 > abs.dev.bc17.json

- Fetch figures dependent on the abstract of a conference

        ./gca-select [output].json figures.uuid | xargs ./gca-client http://abstracts.g-node.org image --path=[someLocalPath]
        # example for local tests
        ./gca-select abs.dev.bc17.json figures.uuid | xargs ./gca-client http://127.0.0.1:9000 image --path=gca-web/fig_bc17/

# Backup Cronjobs

https://tecadmin.net/crontab-in-linux-with-20-examples-of-cron-schedule/

`gca_backup.sh` file

    #!/usr/bin/env bash

    # Home folder containing data base, config files and figures
    GCAHOME=/web/gca

    # Project data base folders 
    GCAPGRESDB=$GCAHOME/postgres/

    # Play framework setup
    GCACONF=$GCAHOME/conf/
    GCAIMAGES=$GCAHOME/images/

    GCAPGRES=pgres_gca_bee

    GCABACKUP=$GCAHOME/backup
    GCABACKDATE=$(date +"%Y%m%dT%H%M%S")
    GCADUMP=$GCABACKUP/gca_$GCABACKDATE.sql

    mkdir -p $GCABACKUP

    # Database backup
    docker exec -it $GCAPGRES pg_dump -d play -U play -f /tmp/dump.sql
    docker cp $GCAPGRES:/tmp/dump.sql $GCADUMP
    gzip $GCADUMP

    # Image folder backup
    tar -zcvf $GCABACKUP/gcaimages_$GCABACKDATE.tar.gz $GCAIMAGES

Daily backup cronjob at 4am:

    0 4 * * * /bin/bash /home/msonntag/Chaos/dmp/gca-web/scripts/gca_backup.sh

Test backup every five minutes

    */5 * * * * /bin/bash /home/msonntag/Chaos/dmp/gca-web/scripts/gca_backup.sh


## Systemctl for postgres and play reboot startup

https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units
https://medium.com/@benmorel/creating-a-linux-service-with-systemd-611b5c8b91d6

`gca_pgres_start.sh` file

    #!/usr/bin/env bash

    GCAHOME=/web/gca
    GCAPGRESSCRIPTS=$GCAHOME/scripts
    . $GCAPGRESSCRIPTS/gca_env.sh

    docker run -i --rm --name $GCAPGRES --network=$GCANET -v $GCAPGRESDB:/var/lib/postgresql/data -p 5432:5432 $GCAPGRESIMG

`gca_pgres.service` file

    [Unit]
    Description=Postgres service for the GCA-Web website
    After=network.target
    StartLimitIntervalSec=0
    
    [Service]
    Type=simple
    Restart=always
    RestartSec=5
    ExecStart=/bin/bash /home/msonntag/Chaos/dmp/gca-web/scripts/pgres_gca_start.sh
    
    [Install]
    WantedBy=multi-user.target

`gca_start.sh` file

    #!/usr/bin/env bash

    GCAHOME=/web/gca
    GCAPGRESSCRIPTS=$GCAHOME/scripts
    . $GCAPGRESSCRIPTS/gca_env.sh

    docker run -dit --rm --name $GCA --network=$GCANET -v $GCACONF:/srv/gca/conf/ -v $GCAFIG:/srv/gca/figures/ -v $GCAFIGMOBILE:/srv/gca/figures_mobile/ -p 9000:9000 $GCAIMG

`gca.service` file

    [Unit]
    Description=Play server for the GCA-Web website
    After=network.target
    After=gca_pgres.service
    StartLimitIntervalSec=0
    
    [Service]
    Type=simple
    Restart=on-failure
    RestartSec=5
    ExecStart=/bin/bash /home/msonntag/Chaos/dmp/gca-web/scripts/gca_start.sh
    
    [Install]
    WantedBy=multi-user.target


### General environment variable script

`gca_env.sh` file
    #!/usr/bin/env bash

    # Docker network
    GCANET=gcanet

    # Home folder containing data base, config files and figures
    GCAHOME=/web/gca

    # Project data base folders 
    GCAPGRESDB=$GCAHOME/postgres/
    GCAPGRES=pgres_gca_bee
    GCAPGRESIMG=postgres:11

    # Play framework setup
    GCACONF=$GCAHOME/conf/
    GCAFIG=$GCAHOME/figures/
    GCAFIGMOBILE=$GCAHOME/figures_mobile/
    GCA=gca_bee
    GCAIMG=mpsonntag/gca-web:latest


## Setting up the required systemd files for restart

    sudo vim /etc/systemd/system/pgres_gca.service
    # paste unit from above and save
    # check if the service works
    sudo systemctl start pgres_gca.service
    # check the status
    systemctl status pgres_gca.service
    # Startup the service on restart
    sudo systemctl enable pgres_gca.service

    # And the same for gca
    sudo vim /etc/systemd/system/gca.service
    sudo systemctl start gca.service
    systemctl status gca.service
    sudo systemctl enable gca.service


ToDo
----
[ ] test email from docker
[ ] merge docker changes into master and favabs and push to upstream
[ ] create release before favabs merge and push to upstream
[ ] deploy current master to dev;
[ ] redeploy with favabs play container and test
[ ] merge favabs into master
[ ] write setup environment script
[ ] backup to gate
   - add backup user to gate
   - create backup ssh key on machine
   - use rsync with this ssh key to copy on backup times
   - add backup ssh public key to ~/.ssh/
