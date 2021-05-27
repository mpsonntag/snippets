## Update existing DOI

If the metadata of a DOI is changed under some circumstances it is acceptable to change to content
without issuing a full new DOI. e.g. if only the license changes from a stricter to a more open license.

In this case the following scripts describe the full update procedure. Replace specific IDs or folders as required.

### Update procedure scripts

Use the following bash script to create a script checklist file; adjust the variables
at the beginning of the file and the list of files to copy into the new zip file in the middle of the script.

```bash
# unique 6-letter id of the doi: g-node.[id]
DOIID=__someid__
# repo owner in gin.g-node.org/[repo owner]/[reponame]
REPOOWNER=__somerepoowner__
# repo name in gin.g-node.org/[repo owner]/[reponame]
REPONAME=__somereponame__

DOIROOT=/data/dev/gin/doidata/doi
REZIPDIR=/data/dev/gin/doidata/rezip
# File this script will be written to; will replace an existing file
SCRIPTFILE=${REZIPDIR}/rezip_script_${DOIID}

DOIDIR=${DOIROOT}/10.12751/g-node.${DOIID}
ZIPNAME=10.12751_g-node.${DOIID}
TAGNAME=10.12751/g-node.${DOIID}

echo "# prepare rezip working directory" > ${SCRIPTFILE}
echo "sudo mkdir -vp ${REZIPDIR}" >> ${SCRIPTFILE}

echo "" >> ${SCRIPTFILE}
echo "- unzip zip file; exit 'screen' with Alt+a+d without ending the session" >> ${SCRIPTFILE}
echo "" >> ${SCRIPTFILE}
echo "screen -S ${REPOOWNER}-${DOIID}-rezip" >> ${SCRIPTFILE}
echo "sudo su root" >> ${SCRIPTFILE}
echo "sudo unzip ${DOIDIR}/${ZIPNAME}.zip -d ${REZIPDIR}/g-node.${DOIID}/ > ${REZIPDIR}/${DOIID}_unzip.log" >> ${SCRIPTFILE}

echo "" >> ${SCRIPTFILE}
echo "- download latest repo version" >> ${SCRIPTFILE}
echo "" >> ${SCRIPTFILE}
echo "cd ${REZIPDIR}" >> ${SCRIPTFILE}
echo "# check gin-cli logged in as doi - note the set server alias - should be gin" >> ${SCRIPTFILE}
echo "sudo gin servers" >> ${SCRIPTFILE}
echo "# fetch the upstream repository - git only; no annex content" >> ${SCRIPTFILE}
echo "sudo gin get ${REPOOWNER}/${REPONAME}" >> ${SCRIPTFILE}
echo "cd ${REPONAME}" >> ${SCRIPTFILE}
echo "# check current remotes" >> ${SCRIPTFILE}
echo "sudo gin remotes" >> ${SCRIPTFILE}
echo "# define tag" >> ${SCRIPTFILE}
echo "# add and set doi remote - make sure to use the correct server alias as prefix e.g. "gin:"" >> ${SCRIPTFILE}
echo "sudo gin add-remote doi gin:doi/${REPONAME}" >> ${SCRIPTFILE}
echo "sudo gin use-remote doi" >> ${SCRIPTFILE}
echo "# remove tag from doi remote" >> ${SCRIPTFILE}
echo "sudo gin git tag -d ${TAGNAME}" >> ${SCRIPTFILE}
echo "sudo gin git push --delete doi ${TAGNAME}" >> ${SCRIPTFILE}
echo "# upload new commits to doi" >> ${SCRIPTFILE}
echo "sudo gin upload ." >> ${SCRIPTFILE}
echo "# re-create tag at latest commit" >> ${SCRIPTFILE}
echo "sudo gin git tag ${TAGNAME}" >> ${SCRIPTFILE}
echo "sudo gin git push --tags doi" >> ${SCRIPTFILE}

echo "" >> ${SCRIPTFILE}
echo "- copy new files to zip directory" >> ${SCRIPTFILE}
echo "" >> ${SCRIPTFILE}
echo "cd $REZIPDIR" >> ${SCRIPTFILE}
echo "# edit and add files as required" >> ${SCRIPTFILE}
echo "sudo cp $REZIPDIR/$REPONAME/LICENSE $REZIPDIR/g-node.$DOIID/LICENSE" >> ${SCRIPTFILE}
echo "sudo cp $REZIPDIR/$REPONAME/README.md $REZIPDIR/g-node.$DOIID/README.md" >> ${SCRIPTFILE}

echo "" >> ${SCRIPTFILE}
echo "- create new zip file (use exact same command as the 'makezip' script does to keep it consistent)" >> ${SCRIPTFILE}
echo "" >> ${SCRIPTFILE}
echo "screen -r ${REPOOWNER}-${DOIID}-rezip" >> ${SCRIPTFILE}
echo "cd ${REZIPDIR}/g-node.${DOIID}" >> ${SCRIPTFILE}
echo "zip ${REZIPDIR}/${ZIPNAME}.zip -Z store -x '*.git*' -r . > ${REZIPDIR}/${DOIID}_zip.log" >> ${SCRIPTFILE}
echo "# check the zip file after the procedure is done" >> ${SCRIPTFILE}
echo "unzip -vl ${REZIPDIR}/${ZIPNAME}.zip" >> ${SCRIPTFILE}

echo "" >> ${SCRIPTFILE}
echo "- handle modified zip file" >> ${SCRIPTFILE}
echo "" >> ${SCRIPTFILE}
echo "# Make hosted zip file mutable again" >> ${SCRIPTFILE}
echo "sudo chattr -i ${DOIDIR}/${ZIPNAME}.zip" >> ${SCRIPTFILE}
echo "# Rename old zipfile but keep for now" >> ${SCRIPTFILE}
echo "sudo mv ${DOIDIR}/${ZIPNAME}.zip ${DOIDIR}/old_${ZIPNAME}.zip" >> ${SCRIPTFILE}
echo "# Move new zip file to hosting location" >> ${SCRIPTFILE}
echo "sudo mv ${REZIPDIR}/${ZIPNAME}.zip ${DOIDIR}/${ZIPNAME}.zip" >> ${SCRIPTFILE}
echo "# Make new zip file immutable" >> ${SCRIPTFILE}
echo "sudo chattr +i ${DOIDIR}/${ZIPNAME}.zip" >> ${SCRIPTFILE}
echo "# check manual download from https://doi.gin.g-node.org/${TAGNAME}" >> ${SCRIPTFILE}
echo "# Remove old zipfile" >> ${SCRIPTFILE}
echo "sudo rm ${DOIDIR}/old_${ZIPNAME}.zip" >> ${SCRIPTFILE}

echo "" >> ${SCRIPTFILE}
echo "- cleanup" >> ${SCRIPTFILE}
echo "" >> ${SCRIPTFILE}
echo "screen -XS ${REPOOWNER}-${DOIID}-rezip quit" >> ${SCRIPTFILE}
echo "sudo rm ${REZIPDIR}/g-node.${DOIID} -r" >> ${SCRIPTFILE}
echo "sudo rm ${REZIPDIR}/${REPONAME} -r" >> ${SCRIPTFILE}
echo "sudo rm ${REZIPDIR}/*.log" >> ${SCRIPTFILE}

echo "" >> ${SCRIPTFILE}
echo "- manually update 'doi.xml' and 'index.html' to reflect the introduced changes:" >> ${SCRIPTFILE}
echo "" >> ${SCRIPTFILE}
echo "cd ${DOIDIR}" >> ${SCRIPTFILE}

echo "" >> ${SCRIPTFILE}
echo "# commit changes after editing is done" >> ${SCRIPTFILE}
echo "cd ${DOIROOT}" >> ${SCRIPTFILE}
echo "sudo git add ${DOIDIR}/doi.xml" >> ${SCRIPTFILE}
echo "sudo git add ${DOIDIR}/index.html" >> ${SCRIPTFILE}
echo "sudo git commit -m 'Update dataset: ${TAGNAME}'" >> ${SCRIPTFILE}
echo "" >> ${SCRIPTFILE}
```
