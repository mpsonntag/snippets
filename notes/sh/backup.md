#!/bin/bash

# Simple copy backup file for a specific directory

set -eu

echo "-- Running backup script..."

DRIVENAME = $1

if [! $DRIVENAME ]; then
    echo "Please provide the name of the target media"
    exit 0
fi

TARGETPATH=/media/$USER/$DRIVENAME
SOURCEPATH=$HOME/Chaos/DC

if [! -d $TARGETPATH ]; then
    echo "Cannot find target: "$TARGETPATH
    exit 0
fi

if [! -d $SOURCEPATH ]; then
    echo "Cannot find source: "$SOURCEPATH
    exit 0
fi 

echo "    -- Removing old files..."
if [ -d $TARGETPATH"/DC" ]; then
    rm $TARGETPATH/DC -rv
fi

echo "    -- Copying directory..."
cp -rv $SOURCEPATH $TARGETPATH

echo "\n    -- Copying done..."
