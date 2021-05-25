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
