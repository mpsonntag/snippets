#!/usr/bin/env bash

CURR=https://crcns.org/data-sets/vc
OUT=VC

curl ${CURR} | grep "${CURR}/" | grep "<a href" | sed 's/        <a href="//g' | sed 's/"/\/about/g' > crcns_${OUT}_out