#!/usr/bin/env bash

# Simple copy script from an external source to a local directory

set -eu

echo "... Running backup script..."

if [ $# != 1 ]; then
    echo "Please provide the name of the target media"
    exit 1
fi

DRIVENAME=$1

TARGETPATH=$HOME/Chaos/DC
SOURCEPATH=/media/$USER/$DRIVENAME

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

