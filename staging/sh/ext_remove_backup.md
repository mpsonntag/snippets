#!/usr/bin/env bash

# Simple copy file backup for a specific directory; removes old files before copy

set -eu

echo "... Running backup script..."

if [ $# != 1 ]; then
    echo "Please provide the name of the target media"
    exit 1
fi

DRIVENAME=$1

TARGETPATH=/media/$USER/$DRIVENAME
SOURCEPATH=$HOME/Chaos/DC

if [ ! -d "$TARGETPATH" ]; then
    echo "... Cannot find target: ${TARGETPATH}"
    exit 1
fi

if [ ! -d "$SOURCEPATH" ]; then
    echo "... Cannot find source: ${SOURCEPATH}"
    exit 1
fi 

echo "... Using target: ${TARGETPATH}"
echo "... Using source: ${SOURCEPATH}"

echo "    Removing old files..."
if [ -d "$TARGETPATH""/DC" ]; then
    echo -n "    Removing '${TARGETPATH}/DC' (y/n):"
    read -sr CHOICE
    echo

    if [ ! "$CHOICE" ]; then
        echo "... Exiting (no choice)"
        echo
        exit 0
    fi

    if [ "$CHOICE" != "y" ]; then
        echo "... Exiting (use only 'y' to continue: ${CHOICE})"
        echo
        exit 0
    fi

    rm "$TARGETPATH"/DC -rv
fi
echo
echo "... Removal done!"
echo

echo "    Copying directory ${SOURCEPATH}..."
cp -rv "$SOURCEPATH" "$TARGETPATH"

echo
echo "... Copy done!"
echo
