## Update existing DOI

If the metadata of a DOI is changed under some circumstances it is acceptable to change to content
without issuing a full new DOI. e.g. if only the license changes from a stricter to a more open license.

In this case the following scripts describe the full update procedure. Replace specific IDs or folders as required.

### Update procedure scripts

  - unzip zip file
```bash
cd /data/doiprep
sudo mkdir -vp rezip/g-node.wvr3jf
screen -S neurogroup_tuni-459ce
sudo su root
sudo unzip /data/doi/10.12751/g-node.wvr3jf/10.12751_g-node.wvr3jf.zip -d /data/doiprep/rezip/g-node.wvr3jf/ > /data/doiprep/rezip/wvr3jf_unzip.log
```
  - once done
```bash
## remove this step in final script version
sudo mv /data/doiprep/rezip/g-node.wvr3jf/wvr3jf_unzip.log /data/doiprep/rezip
```
  - download latest repo version to srv6
```bash
cd /data/doiprep/rezip
# check gin-cli logged in as doi
sudo gin servers
# fetch the upstream repository - git only; no annex content
sudo gin get NeuroGroup_TUNI/Comparative_MEA_dataset
cd Comparative_MEA_dataset
# define tag
TAGNAME=10.12751/g-node.wvr3jf
# add and set doi remote
gin add-remote doi gin:doi/Comparative_MEA_dataset
gin use-remote doi
# remove tag from doi remote 
gin git tag -d $TAGNAME
gin git push --delete doi
# upload new commits to doi
gin upload .
# re-create tag at latest commit
gin git tag $TAGNAME
gin git push --tags doi
```
  - copy new files to zip directory
```bash
cd /data/doiprep/rezip
SOURCE=/data/doiprep/rezip/Comparative_MEA_dataset
TARGET=/data/doiprep/rezip/g-node.wvr3jf
sudo cp $SOURCE/LICENSE $TARGET/LICENSE
sudo cp $SOURCE/README.md $TARGET/README.md
sudo cp $SOURCE/datacite.yml $TARGET/datacite.yml
sudo cp $SOURCE/Data/LICENSE.txt $TARGET/Data/LICENSE.txt
```
  - create new zip file
```bash
screen -r neurogroup_tuni-459ce
cd /data/doiprep/rezip/Comparative_MEA_dataset
zip /data/doiprep/rezip/10.12751_g-node.wvr3jf.zip -Z store -x "*.git*" -r . > /data/doiprep/rezip/wvr3jf_zip.log
```
  - handle modified zip file
```bash
DOIPREP=/data/doiprep/rezip
DOIHOST=/data/doi/10.12751/g-node.4zw2lt
ZIPNAME=10.12751_g-node.4zw2lt
# Make hosted zip file mutable again
sudo chattr -i $DOIHOST/$ZIPNAME.zip
# Rename old zipfile but keep for now
sudo mv $DOIHOST/$ZIPNAME.zip $DOIHOST/old_$ZIPNAME.zip
# Move new zip file to hosting location
sudo mv $DOIPREP/$ZIPNAME.zip $DOIHOST/$ZIPNAME.zip
# Make new zip file immutable
sudo chattr +i $DOIHOST/$ZIPNAME.zip
# Remove old zipfile
sudo rm $DOIHOST/old_$ZIPNAME.zip
```
  - cleanup
```bash
screen -XS neurogroup_tuni-459ce quit
sudo rm /data/doiprep/rezip -r
```
