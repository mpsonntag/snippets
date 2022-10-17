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

### Pre-requisites

