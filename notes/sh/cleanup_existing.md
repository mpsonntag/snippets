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

for IMAGE in $SOURCEPATH/*; do
    FBASE=$(basename $IMAGE)
    FTARGET=${TARGETPATH}${FBASE}
    if [[ -f $FTARGET ]]; then
        echo "File ${FBASE} already exists, removing from ${TARGETPATH}"
        rm $FTARGET
    fi
done
