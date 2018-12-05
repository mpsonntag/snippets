### Set up gcaweb postgres container from scratch and load DB dump

- fetch the proper docker containers
    docker pull postgres
    docker pull gnode/gca

- start docker container w/o mounting docker-entrypoint folder
  make sure it has a mounted docker-entrypoint folder containing the database dump as a plain sql file

    GCAHOME=/home/msonntag/Chaos/dmp/gca-web
    GCAPGRES=pgres_gca_bee
    docker run -dit --rm --name $GCAPGRES -v $GCAHOME/db_pgres_test/:/var/lib/postgresql/data -v $GCAHOME/db_pgres/:/docker-entrypoint-initdb.d -p 5432:5432 postgres:latest

- connect to the postgres db as user postgres in the running container

    docker exec -it $GCAPGRES /bin/bash
    psql -U postgres -d postgres

- connect to database postgres and create the roles we will need, play and roplay as well as a database,
  that shall contain our data.

    CREATE ROLE play WITH LOGIN PASSWORD 'play';
    CREATE ROLE roplay WITH LOGIN PASSWORD 'play';
    CREATE DATABASE play OWNER play;

- exit the database and reconnect as user play; run the database dump file.
    psql -U play
    \i /docker-entrypoint-initdb.d/dump.sql

- exit and stop the container

- now we start and link the gca-web container to the postgres container

    docker run -dit --rm --name $GCAPGRES -v $GCAHOME/db_pgres_test/:/var/lib/postgresql/data -p 5432:5432 postgres:latest

    GCA=gca_bee
    GCAIMAGE=latest
    docker run -dit --rm --link $GCAPGRES:pgres --name $GCA -v $GCAHOME/conf_dev_pgres/:/srv/gca/conf/ -v $GCAHOME/fig_gca/:/srv/gca/figures/ -v $GCAHOME/fig_m_gca/:/srv/gca/figures_mobile/ -p 9000:9000 mpsonntag/gca-web:$GCAIMAGE

- NOTES:
    - make the play framework config file has the proper IP address of the postgres docker container set
        e.g. `db.default.url="jdbc:postgresql://172.17.0.2:5432/play"`.
    - when an update of the DB schema is required, make sure the play framework config file 
        has the persistence setting `jpa.default=defaultPersistenceUnit`.