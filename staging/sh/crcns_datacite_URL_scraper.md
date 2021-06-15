#!/usr/bin/env bash

CRCNS_URL=https://crcns.org/data-sets

# fetch main category URLs
curl ${CRCNS_URL} | grep "${CRCNS_URL}/" | grep '  href=' | sed 's/"//g' | sed 's/^\s*href=//g' > crns_main_out

CURR=https://crcns.org/data-sets/vc
OUT=VC

# fetch sub category URLs
curl ${CURR} | grep "${CURR}/" | grep "<a href" | sed 's/^\s*<a href="//g' | sed 's/"/\/about/g' > crcns_${OUT}_out


# fetch xml from datacite
https://api.datacite.org/dois/application/vnd.datacite.datacite+xml/10.6080/k0nk3c7j
