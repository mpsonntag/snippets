#!/usr/bin/env bash

CRCNS_URL=https://crcns.org/data-sets

curl ${CRCNS_URL} | grep "${CRCNS_URL}/" | grep '  href=' | sed 's/"//g' | sed 's/^\s*href=//g' > crns_main_out

CURR=https://crcns.org/data-sets/vc
OUT=VC

curl ${CURR} | grep "${CURR}/" | grep "<a href" | sed 's/        <a href="//g' | sed 's/"/\/about/g' > crcns_${OUT}_out