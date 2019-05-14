#!/bin/bash
# File unzips postgres db backup files, renames them and zips
# them again to the original name.

FILES=/home/msonntag/Chaos/DL/tmp/test/*.sql.gz

for f in $FILES
do
  gunzip $f
  curr="$(basename $f)"
  currsql=${curr%".gz"}
  new="$(dirname $f)/dump.sql"
  mv -v $f $new
  gzip -v $new
  mv -v $new".gz" $f
done
