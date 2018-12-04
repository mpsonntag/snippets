### Set up gcaweb postgres container from scratch and load DB dump

- fetch the proper docker containers
    docker pull postgres
    docker pull gnode/gca

- start docker container w/o mounting docker-entrypoint folder
  make sure it has a mounted docker-entrypoint folder containing the database dump as a plain sql file

    GCAHOME=/dmp/gca-web
    docker run -dit --rm --name pgres_gca_bee -v $GCAHOME/db_pgres_test/:/var/lib/postgresql/data -v $GCAHOME/db_pgres/:/docker-entrypoint-initdb.d -p 5432:5432 postgres:latest
