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
