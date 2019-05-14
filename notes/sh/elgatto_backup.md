#!/bin/bash
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

echo "    Removing old files..."
if [ -d $TARGETPATH"/DC" ]; then
    echo -n "    Removing '${TARGETPATH}/DC' (y/n):"
    read -s CHOICE
    echo

    if [ ! $CHOICE ]; then
        echo "... Exiting (no choice)"
        exit 0
    fi

    if [ $CHOICE != "y" ]; then
        echo "... Exiting (${CHOICE})"
        exit 0
    fi

    rm $TARGETPATH/DC -rv
fi
printf "... Removal done!\n\n"

echo "    Copying directory ${SOURCEPATH}..."
cp -rv $SOURCEPATH $TARGETPATH

printf "\n... Copying done!\n"
