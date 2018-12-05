### Set up gcaweb postgres container from scratch and load DB dump

- define and fetch the proper docker containers
    GCAPGRESIMG=postgres:11
    GCAIMG=mpsonntag/gca-web:latest

    docker pull $GCAPGRESIMG
    docker pull $GCAIMG

- start docker container w/o mounting docker-entrypoint folder
  make sure it has a mounted docker-entrypoint folder containing the database dump as a plain sql file

    GCAHOME=/home/msonntag/Chaos/dmp/gca-web
    GCAPGRESDB=$GCAHOME/db_pgres_test/
    GCAPGRESSCRIPTS=$GCAHOME/db_pgres/
    GCAPGRES=pgres_gca_bee
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
