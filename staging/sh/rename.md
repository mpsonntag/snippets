#!/usr/bin/env bash

# File unzips postgres db backup files, renames them and zips
# them again to the original name.
# Usage e.g. bash psqlren.sh .


if [ $# != 1 ]; then
    echo "... Postgres dump file directory required"
    echo "    exiting..."
    exit 1
fi

if [ ! -d $1 ]; then
    echo "... $1 is not a valid directory"
    echo "    exiting..."
    exit 1
fi

DIR="$(readlink -f $1)"
FILES=$DIR/*.sql.gz

for f in $FILES
do
  csf=${f%".gz"}
  new="$(dirname $f)/dump.sql"

  gunzip -v $f
  mv -v $csf $new
  gzip -v $new
  mv -v $new".gz" $f
  echo
done
