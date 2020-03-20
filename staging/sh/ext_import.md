#!/usr/bin/env bash

# Simple copy script from an external source to a local directory

set -eu

echo "... Running backup script..."

if [ $# != 1 ]; then
    echo
    echo "    Please provide the name of the target media"
    echo
    exit 1
fi

DRIVENAME=$1

TARGETPATH=$HOME/Chaos/
SOURCEPATH=/media/$USER/$DRIVENAME/DC

if [ ! -d $TARGETPATH ]; then
    echo "... Cannot find target: ${TARGETPATH}"
    exit 1
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
