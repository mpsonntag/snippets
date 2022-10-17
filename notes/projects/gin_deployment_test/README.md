# GIN deployment tests

The following describes how a new gin release can be tested in a test deployment or the 
live environment. Currently, all necessary files and a copy of this script can be found 
in the [G-Node/gin_deployment_test](https://gin.g-node.org/G-Node/gin_deployment_test/) 
repository on gin.

This document describes the manual tests that should be run in the dev and test 
deployment before deploying a new version of the gin-doi server to the live machine.

Make sure to push and deploy the latest build to the dev and test environment and keep 
an eye on the gin-doi logfile before starting to run the tests:

```bash
# Run the command from the folder containing the gin-web docker-compose file
docker-compose logs -f --tail=200
```


## Test directory contents
This directory contains all files required to run a minimal set of manual tests towards a 
running GIN instance.

## Deployment tests
The following describes the full rundown of all deployment tests. These tests require
a full test setup of a GIN server and a GIN CLI set up to work with the GIN instances.


Test that the normal client commands are working

```bash
mkdir gintest
cd gintest
# use the gin dev server
gin use-server dev
gin info
gin servers
gin repos
gin repos doi
gin repos deploy
gin repos deployadmin
# additional command checks
```

```bash
gin login deployadmin
gin get msonntag/validtest
cd validtest/
gin get-content .
vim bla
gin commit .
gin upload
cd ..
gin logout
```


```bash
gin login gin-valid
gin repos deploy
gin get deploy/writerepo
cd writerepo/
# test non annex data
vim test.txt
gin commit . -m "add text file"
gin upload
mkdir data
mv test.txt data/
gin commit . -m "Move text file"
gin upload .
# file version tests
gin version data/test.txt
git log --oneline --graph
gin version [use previous commit hash]
gin version data/test.txt
head -c 11M /dev/urandom > data/sampleA.bin
gin commit . -m "add annex file"
gin commit .
gin upload .
gin version data/sampleA.bin
head -c 13M /dev/urandom > data/sampleA.bin
gin commit . -m "update sampleA file size"
gin upload .
gin version data/sampleA.bin
gin upload .
gin get-content .
gin version data/sampleA.bin
cd ..
gin logout
# clone the same repo as a different name to check versions across users and different versions of the repository
cd writerepo_ginvalid/
gin login gin-valid
gin download .
gin get-content .
gin version data/sampleA.bin
gin get-content .
vim data/addfile.txt
gin commit . -m "Check add file commit author"
cd ..
gin logout
```


```bash
conda create -n datalad python=3.9 -y
conda info --envs
conda activate datalad
pip install datalad
conda install -c conda-forge git-annex -y
datalad create datalad_test
```


```bash
# login as ginadmin
gin login ginadmin
# fetch the gin_deployment repo
gin get G-Node/gin_deployment_test
gin logout
```

```bash
gin logout
gin get deploy/readrepo
```

### Pre-requisites

