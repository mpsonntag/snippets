#!/usr/bin/env bash

CRCNS_URL=https://crcns.org/data-sets
FILE_MAIN=crcns_main
FILE_CATEGORY_URLS=crcns_categories
FILE_DOI_URLS=crcns_dois
DATACITE_XML_DIR=datacite

#-- fetch main category URLs
curl ${CRCNS_URL} | grep "${CRCNS_URL}/" | grep '  href=' | sed 's/"//g' | sed 's/^\s*href=//g' > ${FILE_MAIN}

#-- fetch all subcategory links
LINES_MAIN=$(cat $FILE_MAIN)
#-- reset categories file
echo "" > ${FILE_CATEGORY_URLS}
for LINE in $LINES_MAIN
do
  echo "... handling dataset category $LINE"
  #-- append to common file
  curl ${LINE} | grep "${LINE}/" | grep "<a href" | sed 's/^\s*<a href="//g' | sed 's/"/\//g' >> ${FILE_CATEGORY_URLS}
  #-- add to separate files
  #FILE_CURR_CATEGORY=$(echo ${LINE} | sed 's/https:\/\/crcns.org\/data-sets\///g')
  #curl ${LINE} | grep "${LINE}/" | grep "<a href" | sed 's/^\s*<a href="//g' | sed 's/"/\//g' > crcns_category_${FILE_CURR_CATEGORY}
done

#-- fetch xml id from about page
#-- there are two variants of the "about" page - plain "/about" and /about-{set-id}
#-- reset DOI URLs file
echo "" > ${FILE_DOI_URLS}
LINES_CATEGORIES=$(cat $FILE_CATEGORY_URLS)
for LINE in ${LINES_CATEGORIES}
do
  echo "... handling ${LINE}" >> ${FILE_DOI_URLS}
  #-- handle "/about" link variant
  curl ${LINE}/about | grep "doi.org/10.6080" | awk -F "dx.doi.org/" '{print $2}' | awk -F "<" '{print $1}' >> ${FILE_DOI_URLS}
  #-- handle "/about-[set-id]" link variant
  CURR_ID=$(echo $LINE | sed 's/https:\/\/crcns.org\/data-sets\/[a-zA-Z]*\///g')
  curl ${LINE}/about-${CURR_ID} | grep "doi.org/10.6080" | awk -F "dx.doi.org/" '{print $2}' | awk -F "<" '{print $1}' >> ${FILE_DOI_URLS}
done

#-- fetch datacite xml files
LINES_DOI=$(cat $FILE_DOI_URLS)
for LINE in ${LINES_DOI}
do
  if [[ ${LINE} = 10.6080* ]]; then
    CURR_ID=$(echo ${LINE} | sed 's/10.6080\///g' | sed 's/\s*$//g')
    curl https://api.datacite.org/dois/application/vnd.datacite.datacite+xml/10.6080/${CURR_ID} > ${DATACITE_XML_DIR}/${CURR_ID}.xml
  fi
done
