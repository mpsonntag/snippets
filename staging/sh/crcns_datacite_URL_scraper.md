#!/usr/bin/env bash

CRCNS_URL=https://crcns.org/data-sets
FILE_MAIN=crcns_main
FILE_CATEGORY_URLS=crcns_categories
FILE_DOI_LOG=crcns_doi_id_log
FILE_DOI_ID=crcns_doi_id
DATACITE_XML_DIR=datacite

#-- prepare output directory
mkdir -vp $(pwd)/datacite

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
done

#-- fetch xml id from about page
#-- there are two variants of the "about" page - plain "/about" and /about-{set-id}
#-- reset DOI id files; log file is kept for back checks which ids might be missing
echo "" > ${FILE_DOI_ID}
echo "" > ${FILE_DOI_LOG}
LINES_CATEGORIES=$(cat $FILE_CATEGORY_URLS)
for LINE in ${LINES_CATEGORIES}
do
  CURR_ID=$(echo $LINE | sed 's/https:\/\/crcns.org\/data-sets\/[a-zA-Z\-]*\///g')
  echo "... handling (${CURR_ID}) ${LINE}" >> ${FILE_DOI_LOG}
  #-- handle "/about" link variant
  curl ${LINE}/about | grep "doi.org/10.6080" | awk -F "doi.org/" '{print $2}' | awk -F "<" '{print $1}' | tee -a ${FILE_DOI_ID} >> ${FILE_DOI_LOG}
  #-- handle "/about-[set-id]" link variant
  curl ${LINE}/about-${CURR_ID} | grep "doi.org/10.6080" | awk -F "doi.org/" '{print $2}' | awk -F "<" '{print $1}' | tee -a ${FILE_DOI_ID} >> ${FILE_DOI_LOG}
done

#-- fetch datacite xml files
LINES_DOI=$(cat $FILE_DOI_ID)
for LINE in ${LINES_DOI}
do
  if [[ ${LINE} = 10.6080* ]]; then
    CURR_ID=$(echo ${LINE} | sed 's/10.6080\///g' | sed 's/\s*$//g')
    curl https://api.datacite.org/dois/application/vnd.datacite.datacite+xml/10.6080/${CURR_ID} > ${DATACITE_XML_DIR}/${CURR_ID}.xml
  fi
done

#-- check README for details on deviating URL syntax and datasets not published via datacite
#-- fetch datacite files for datasets with deviating URL syntax
curl https://api.datacite.org/dois/application/vnd.datacite.datacite+xml/10.6080/K0H12ZXD > ${DATACITE_XML_DIR}/K0H12ZXD.xml
curl https://api.datacite.org/dois/application/vnd.datacite.datacite+xml/10.6080/K0B27SHN > ${DATACITE_XML_DIR}/K0B27SHN.xml
curl https://api.datacite.org/dois/application/vnd.datacite.datacite+xml/10.6080/K0ZW1HVD > ${DATACITE_XML_DIR}/K0ZW1HVD.xml
curl https://api.datacite.org/dois/application/vnd.datacite.datacite+xml/10.6080/K0V40S4D > ${DATACITE_XML_DIR}/K0V40S4D.xml
curl https://api.datacite.org/dois/application/vnd.datacite.datacite+xml/10.6080/K0VM49GF > ${DATACITE_XML_DIR}/K0VM49GF.xml
curl https://api.datacite.org/dois/application/vnd.datacite.datacite+xml/10.6080/K0NK3BZJ > ${DATACITE_XML_DIR}/K0NK3BZJ.xml
curl https://api.datacite.org/dois/application/vnd.datacite.datacite+xml/10.6080/K0R49NQV > ${DATACITE_XML_DIR}/K0R49NQV.xml
curl https://api.datacite.org/dois/application/vnd.datacite.datacite+xml/10.6080/K05D8PS8 > ${DATACITE_XML_DIR}/K05D8PS8.xml
curl https://api.datacite.org/dois/application/vnd.datacite.datacite+xml/10.6080/K0VQ30V9 > ${DATACITE_XML_DIR}/K0VQ30V9.xml
curl https://api.datacite.org/dois/application/vnd.datacite.datacite+xml/10.6080/K04B2ZJ5 > ${DATACITE_XML_DIR}/K04B2ZJ5.xml
