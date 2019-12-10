#!/usr/bin/env bash

set -eu

if [[ $# != 2 ]]; then
    echo "... Source and target directories required"
    echo "    exiting..."
    exit 1
fi

SOURCEPATH=$1
TARGETPATH=$2

echo "... using ${SOURCEPATH} and ${TARGETPATH}"

if [[ ! -d $TARGETPATH ]]; then
    echo "... Cannot find target: ${TARGETPATH}"
    exit 1
fi

if [[ ! -d $SOURCEPATH ]]; then
    echo "... Cannot find source: ${SOURCEPATH}"
    exit 1
fi 

echo "WARNING: This will remove same name files from ${TARGETPATH}"
echo -n "Type 'Y' to continue': "
read -s GO_ON
echo

if [[ $GO_ON != "Y" ]]; then
    echo "Did not read 'Y', aborting ...'"
    exit 1
fi

echo ""

for IMAGE in $SOURCEPATH/*; do
    FBASE=$(basename $IMAGE)
    FTARGET=${TARGETPATH}${FBASE}
    if [[ -f $FTARGET ]]; then
        echo "File ${FBASE} already exists, removing ..."
        rm $FTARGET
    fi
done
