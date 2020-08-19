#!/usr/bin/env bash

# Simple copy file backup to an external source from a local directory

set -eu

echo "... Running backup script..."

if [ $# != 1 ]; then
    echo "Please provide the name of the target media"
    exit 1
fi

DRIVENAME=$1

TARGETPATH=/media/$USER/$DRIVENAME
SOURCEPATH=$HOME/Chaos/DC

if [ ! -d $TARGETPATH ]; then
    echo
    echo "    Please provide the name of the target media"
    echo
fi

if [ ! -d $SOURCEPATH ]; then
    echo "... Cannot find source: ${SOURCEPATH}"
    exit 1
fi 

echo "... Target directory: ${TARGETPATH}"
echo "... Source directory: ${SOURCEPATH}"

echo "    Update directory ${TARGETPATH}..."
cp -vuLr $SOURCEPATH $TARGETPATH

echo
echo "... Update done!"
echo
