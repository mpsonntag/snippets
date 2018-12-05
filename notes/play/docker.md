### Set up gcaweb postgres container from scratch and load DB dump

- fetch the proper docker containers
    docker pull postgres
    docker pull gnode/gca

- start docker container w/o mounting docker-entrypoint folder
  make sure it has a mounted docker-entrypoint folder containing the database dump as a plain sql file

    GCAHOME=/home/msonntag/Chaos/dmp/gca-web
    GCAPGRES=pgres_gca_bee
    docker run -dit --rm --name $GCAPGRES -v $GCAHOME/db_pgres_test/:/var/lib/postgresql/data -v $GCAHOME/db_pgres/:/docker-entrypoint-initdb.d -p 5432:5432 postgres:latest

- connect to database postgres and create the roles we will need, play and roplay as well as a database,
  that shall contain our data.

    docker exec -it $GCAPGRES psql -Upostgres -dpostgres -c "CREATE ROLE play WITH LOGIN PASSWORD 'play';"
    docker exec -it $GCAPGRES psql -Upostgres -dpostgres -c "CREATE ROLE roplay WITH LOGIN PASSWORD 'play';"
    docker exec -it $GCAPGRES psql -Upostgres -dpostgres -c "CREATE DATABASE play OWNER play;"

- run the database dump file as user play within the new database play.

    docker exec -it $GCAPGRES psql -dplay -a -f /docker-entrypoint-initdb.d/dump.sql

- stop the container

    docker stop $GCAPGRES

- create a common network for our containers

    GCANET=gcanet
    docker network create $GCANET

- now we start and link the gca-web container to the postgres container

    docker run -dit --rm --name $GCAPGRES --network=$GCANET -v $GCAHOME/db_pgres_test/:/var/lib/postgresql/data -p 5432:5432 postgres:latest

    GCA=gca_bee
    GCAIMAGE=latest
    docker run -dit --rm --name $GCA --network=$GCANET -v $GCAHOME/conf_dev_pgres/:/srv/gca/conf/ -v $GCAHOME/fig_gca/:/srv/gca/figures/ -v $GCAHOME/fig_m_gca/:/srv/gca/figures_mobile/ -p 9000:9000 mpsonntag/gca-web:$GCAIMAGE

- NOTES:
    - make the play framework config file has the proper IP address or name of the postgres docker container set
        e.g. `db.default.url="jdbc:postgresql://172.17.0.2:5432/play"`
        or  `db.default.url="jdbc:postgresql://pgres_gca_bee:5432/play"`
    - when an update of the DB schema is required, make sure the play framework config file 
        has the persistence setting `jpa.default=defaultPersistenceUnit`.

## Create and fetch database dumps

    docker exec -it pgres_gca_bee pg_dump -d play -U play -f /tmp/dump.sql
    GCADUMP=/home/msonntag/Chaos/dmp/gca-web/gca_dump_$(date +"%Y%m%dT%H%M%S").sql
    docker cp pgres_gca_bee:/tmp/dump.sql $GCADUMP
    gzip $GCADUMP
