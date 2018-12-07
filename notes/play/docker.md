### Set up gcaweb postgres container from scratch and load DB dump

- define and fetch the proper docker containers
    GCAPGRESIMG=postgres:11
    GCAIMG=mpsonntag/gca-web:latest

    docker pull $GCAPGRESIMG
    docker pull $GCAIMG

- start docker container w/o mounting docker-entrypoint folder
  make sure it has a mounted docker-entrypoint folder containing the database dump as a plain sql file
  The docker command needs to be run twice, the first one sets up the postgres db, the second one starts it properly.

    GCAHOME=/home/msonntag/Chaos/dmp/gca-web
    GCAPGRESDB=$GCAHOME/db_pgres_test/
    GCAPGRESSCRIPTS=$GCAHOME/db_pgres/
    GCAPGRES=pgres_gca_bee
    docker run -dit --rm --name $GCAPGRES -v $GCAPGRESDB:/var/lib/postgresql/data -v $GCAPGRESSCRIPTS:/docker-entrypoint-initdb.d -p 5432:5432 $GCAPGRESIMG
    docker run -dit --rm --name $GCAPGRES -v $GCAPGRESDB:/var/lib/postgresql/data -v $GCAPGRESSCRIPTS:/docker-entrypoint-initdb.d -p 5432:5432 $GCAPGRESIMG

- connect to database postgres and create the roles we will need, play and roplay as well as a database,
  that shall contain our data.

    docker exec -it $GCAPGRES psql -Upostgres -dpostgres -c "CREATE ROLE play WITH LOGIN PASSWORD '';"
    docker exec -it $GCAPGRES psql -Upostgres -dpostgres -c "CREATE ROLE roplay WITH LOGIN PASSWORD '';"
    docker exec -it $GCAPGRES psql -Upostgres -dpostgres -c "CREATE DATABASE play OWNER play;"

- run the database dump file as user play within the new database play.

    docker exec -it $GCAPGRES psql -Uplay -dplay -a -f /docker-entrypoint-initdb.d/dump.sql

- stop the container

    docker stop $GCAPGRES

- create a common network for our containers

    GCANET=gcanet
    docker network create $GCANET

- now we start and link the gca-web container to the postgres container

    docker run -dit --rm --name $GCAPGRES --network=$GCANET -v $GCAPGRESDB:/var/lib/postgresql/data -p 5432:5432 $GCAPGRESIMG

    GCACONF=$GCAHOME/conf_dev_pgres/
    GCAFIG=$GCAHOME/fig_gca/
    GCAFIGMOBILE=$GCAHOME/fig_m_gca/
    GCA=gca_bee
    docker run -dit --rm --name $GCA --network=$GCANET -v $GCACONF:/srv/gca/conf/ -v $GCAFIG:/srv/gca/figures/ -v $GCAFIGMOBILE:/srv/gca/figures_mobile/ -p 9000:9000 $GCAIMG

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

    GCAPGRES=pgres_gca_bee
    GCAHOME=/home/msonntag/Chaos/dmp/gca-web
    GCAFIG=$GCAHOME/fig_gca/
    GCABACKUP=$GCAHOME/backup
    GCABACKDATE=$(date +"%Y%m%dT%H%M%S")
    GCADUMP=$GCABACKUP/gca_$GCABACKDATE.sql

    mkdir -p $GCABACKUP
    docker exec -it $GCAPGRES pg_dump -d play -U play -f /tmp/dump.sql
    docker cp $GCAPGRES:/tmp/dump.sql $GCADUMP
    gzip $GCADUMP
    tar -zcvf $GCABACKUP/gcafig_$GCABACKDATE.tar.gz $GCAFIG

Daily backup cronjob at 4am:

    0 4 * * * /bin/bash /home/msonntag/Chaos/dmp/gca-web/scripts/gca_backup.sh

Test backup every five minutes

    */5 * * * * /bin/bash /home/msonntag/Chaos/dmp/gca-web/scripts/gca_backup.sh


## Systemctl for postgres and play reboot startup

https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units
https://medium.com/@benmorel/creating-a-linux-service-with-systemd-611b5c8b91d6

`gca_pgres_start.sh` file

    #!/usr/bin/env bash

    GCANET=gcanet
    GCAHOME=/home/msonntag/Chaos/dmp/gca-web
    GCAPGRES=pgres_gca_bee
    GCAPGRESIMG=postgres:11
    GCAPGRESDB=$GCAHOME/db_pgres_test/

    docker run -dit --rm --name $GCAPGRES --network=$GCANET -v $GCAPGRESDB:/var/lib/postgresql/data -p 5432:5432 $GCAPGRESIMG

`gca_pgres.service` file

    [Unit]
    Description=Postgres service for the GCA-Web website
    After=network.target
    StartLimitIntervalSec=0
    
    [Service]
    Type=simple
    Restart=always
    RestartSec=5
    ExecStart=/bin/bash /home/msonntag/Chaos/dmp/gca-web/scripts/gca_pgres_start.sh
    
    [Install]
    WantedBy=multi-user.target
