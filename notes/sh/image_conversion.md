#!/usr/bin/env bash

set -eu

if [[ $# != 2 ]]; then
    echo "... Input and output directories required"
    echo "    exiting..."
    exit 1
fi

SOURCEPATH=$1
TARGETPATH=$2
FORMAT="JPEG"
QUALITY="60%"

echo "... using ${SOURCEPATH} and ${TARGETPATH}"

if [[ ! -d $TARGETPATH ]]; then
    echo "... Cannot find target: ${TARGETPATH}"
    exit 1
fi

if [[ ! -d $SOURCEPATH ]]; then
    echo "... Cannot find source: ${SOURCEPATH}"
    exit 1
fi 

echo "Converting images in ${SOURCEPATH} in ${TARGETPATH}"
echo "Image format: ${FORMAT}, Quality: ${QUALITY}"

for IMAGE in $SOURCEPATH/*; do
    FBASE=$(basename $IMAGE)
    convert ${IMAGE} -verbose -quality ${QUALITY} ${FORMAT}:${TARGETPATH}${FBASE}
done
