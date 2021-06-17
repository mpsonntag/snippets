#!/usr/bin/env bash

CRCNS_URL=https://crcns.org/data-sets

# fetch main category URLs
curl ${CRCNS_URL} | grep "${CRCNS_URL}/" | grep '  href=' | sed 's/"//g' | sed 's/^\s*href=//g' > crns_main_out

CURR=https://crcns.org/data-sets/vc
OUT=vc

# fetch sub category URLs
curl ${CURR} | grep "${CURR}/" | grep "<a href" | sed 's/^\s*<a href="//g' | sed 's/"/\/about/g' > crcns_${OUT}_out

# fetch xml id from about page
# there are two variants of the "about" page - plain "/about" and /about-{set-id}
ABOUT=https://crcns.org/data-sets/vc/pvc-12/about
ABOUT_ALT=https://crcns.org/data-sets/vc/pvc-13/about-pvc-13

curl ${ABOUT} | grep "doi.org"

# fetch xml from datacite
https://api.datacite.org/dois/application/vnd.datacite.datacite+xml/10.6080/k0nk3c7j
