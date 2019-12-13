# when setting up and running the plain scala sbt activator GCA-Web:

  # make sure the correct JAVA version is active
  echo $JAVA_HOME
  # if required set the 1.8 version
  JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64/
  # make sure both java and javac are also set to java 8 via the alternatives.
  # otherwise the compiler will create classes incompatible with the scala compiler
  sudo update-alternatives java
  sudo update-alternatives javac
  cd ${WORK}/GCA-Web

  # MAKE SURE THERE IS NO DOCKER CONTAINER RUNNING

  activator test
  activator run


# when setting up and running the docker base GCA-WEB:
- Recursively copy template folder

  cd ${STAGING}/gca
  CURRDATE=$(date +"%Y%m%d")
  CURRDIR=${CURRDATE}_gca_init
  cp ./gca_init_template ./${CURRDIR} -r
  cd ${CURRDIR}

- fetch latest figures and database and copy them into the template folders `figures`, `figures_mobile`, `banners` and `banners_mobile`

  # copy figures - edit as required
  # scp ${USER}@[backupserver]:[backuplocation]/images/figures/* ./figures/
  # scp ${USER}@[backupserver]:[backuplocation]/images/figures_mobile/* ./figures_mobile/

- if available fetch the latest database dump from a running abstracts service, rename to backup.sql.gz and unzip into `$CURRDIR` 

  # copy database dump - edit as required
  # scp ${USER}@[backupserver]:[backuplocation]/postgres/gca_[variable].sql.gz backup.sql.gz
  gunzip backup.sql.gz

- stop any running containers

    # requires manual set of latest gca directory
    # GCADIR=/web/gca[variable]
    cd ${GCADIR}/env
    docker-compose down
    cd /web

- remove the leftover directories

   # rm /web/gca[variable] -r

- move to the staging directory and run the script

  cd ${STAGING}/gca/${CURRDIR}

  # make sure all settings in .env, application.conf and the init script are properly set
  sudo bash ./gca_initialize.sh .

- cleanup and move the staging directory to the archive folder if everything worked out.

  cd ${STAGING}/gca
  rm ${CURRDIR}/figures/*
  rm ${CURRDIR}/figures_mobile/*
  rm ${CURRDIR}/banners/*
  rm ${CURRDIR}/banners_mobile/*
  mv ${CURRDIR} ./archive

