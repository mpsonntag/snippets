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
  - download latest repo version to srv6
```bash
cd /data/doiprep/rezip
# check gin-cli logged in as doi - note the set server alias - should be gin
sudo gin servers
# fetch the upstream repository - git only; no annex content
sudo gin get NeuroGroup_TUNI/Comparative_MEA_dataset
cd Comparative_MEA_dataset
# check current remotes
sudo gin remotes
# define tag
TAGNAME=10.12751/g-node.wvr3jf
# add and set doi remote - make sure to use the correct server alias as prefix e.g. "gin:"
sudo gin add-remote doi gin:doi/Comparative_MEA_dataset
sudo gin use-remote doi
# remove tag from doi remote 
sudo gin git tag -d $TAGNAME
sudo gin git push --delete doi $TAGNAME
# upload new commits to doi
sudo gin upload .
# re-create tag at latest commit
sudo gin git tag $TAGNAME
sudo gin git push --tags doi
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
  - create new zip file (use exact same command as the "makezip" script does to keep it consistent)
```bash
screen -r neurogroup_tuni-459ce
cd /data/doiprep/rezip/g-node.wvr3jf
zip /data/doiprep/rezip/10.12751_g-node.wvr3jf.zip -Z store -x "*.git*" -r . > /data/doiprep/rezip/wvr3jf_zip.log
```
  - handle modified zip file
```bash
DOIPREP=/data/doiprep/rezip
DOIHOST=/data/doi/10.12751/g-node.wvr3jf
ZIPNAME=10.12751_g-node.wvr3jf
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
  - manually update `doi.xml` and `index.html` to reflect the introduced changes:
```bash
cd /data/doi/10.12751/g-node.wvr3jf
# commit changes after editing is done
cd /data/doi
sudo git add /data/doi/10.12751/g-node.wvr3jf/doi.xml
sudo git add /data/doi/10.12751/g-node.wvr3jf/index.html
sudo git commit -m "Update dataset: 10.12751/g-node.wvr3jf"
```
