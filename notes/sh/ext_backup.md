#!/usr/env/bin bash

# Simple copy backup file for a specific directory

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
    echo "... Cannot find target: ${TARGETPATH}"
    exit 1
fi

if [ ! -d $SOURCEPATH ]; then
    echo "... Cannot find source: ${SOURCEPATH}"
    exit 1
fi 

echo "... Using target: ${TARGETPATH}"
echo "... Using source: ${SOURCEPATH}"

echo "    Update directory ${SOURCEPATH}..."
cp -vuLr $SOURCEPATH $TARGETPATH

printf "\n... Update done!\n"
