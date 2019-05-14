#!/usr/bin/env bash

set -eu

echo "Running GCA backup"

# Home folder containing data base, config files and figures
GCAHOME=/web/gcadev
GCAIMAGES=$GCAHOME/images/
GCABACKUP=$GCAHOME/backup

GCAWEB=gcadev_gcaweb_1
GCAPGRES=gcadev_gcadb_1

GCABACKDATE=$(date +"%Y%m%dT%H%M%S")
echo $GCABACKDATE
GCADUMP=$GCABACKUP/gca_$GCABACKDATE.sql

# Database backup
docker exec $GCAPGRES rm -fv /tmp/dump.sql
echo "Running pg_dump"
docker exec $GCAPGRES pg_dump -d play -U play -f /tmp/dump.sql
docker cp $GCAPGRES:/tmp/dump.sql $GCADUMP

gzip -vn $GCADUMP

echo "Running deduplication on $GCABACKUP..."
fdupes -dN $GCABACKUP/

LOGDIR=$GCAHOME/logs
echo "Copying service logs to $LOGDIR"
docker logs -t $GCAPGRES > ${LOGDIR}/${GCAPGRES}_${GCABACKDATE}.log
docker logs -t $GCAWEB > ${LOGDIR}/${GCAWEB}_${GCABACKDATE}.log

echo "Done!"
