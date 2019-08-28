#!/usr/bin/env bash

set -eu

if [[ $# != 2 ]]; then
    echo "... Input and output directories required"
    echo "    exiting..."
    exit 1
fi

SOURCEPATH=$1
TARGETPATH=$2

# Output format for JPEG and GIF is JPEG; use quality 50%
J_QUALITY="50%"

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

for IMAGE in $SOURCEPATH/*; do
    FBASE=$(basename $IMAGE)
    FMTYPE=$(mimetype -b $IMAGE)
    if [[ $FMTYPE == "image/jpeg" ]]; then
        convert ${IMAGE} -verbose -quality ${J_QUALITY} JPEG:${TARGETPATH}${FBASE}
    fi
    if [[ $FMTYPE == "image/png" ]]; then
        convert ${IMAGE} -verbose -quality ${J_QUALITY} JPEG:${TARGETPATH}${FBASE}
        # unfortunately does not compress as much as we had hoped so 
        # its disabled for now.
        # optipng ${IMAGE} -out ${TARGETPATH}${FBASE}
    fi
    if [[ $FMTYPE == "image/gif" ]]; then
        convert ${IMAGE} -verbose -quality ${J_QUALITY} JPEG:${TARGETPATH}${FBASE}
    fi
done

du -hs ${SOURCEPATH}
du -hs ${TARGETPATH}
