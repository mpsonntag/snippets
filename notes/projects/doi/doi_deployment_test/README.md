# GIN-DOI deployment checklist

This document describes the manual tests that should be run in the
dev and test deployment before deploying a new version of the 
gin-doi server to the live machine.

Make sure to push and deploy the latest build to the dev and test 
environment and keep an eye on the gin-doi logfile before starting to
run the tests:

```bash
# Run the command from the folder containing the gin-doi docker-compose file
docker-compose logs -f --tail=200
```


## Test directory contents
This directory contains all files required to run a minimal set of manual
tests from a running GIN instance to a running GIN-DOI instance.
Upload the content of this directory to the running GIN instance and use
it to simulate DOI requests and the appropriate responses to failure and 
success. The undocumented files simulate data files and test download, upload
and packaging of git and annex files.

The repository contains the following files:
- LICENSE
  ... license file used for the DOI requests; copy over this file
- LICENSE_invalid
  ... license file with an invalid header - should be caught by the DOI server on request
- LICENSE_valid
  ... valid CC0 license
- datacite.yml
  ... datacite file used for the DOI requests; copy over this file
- datacite_01_broken.yml
  ... a datacite file that is not a valid yaml file; checks broken yaml response
- datacite_02_invalid.yml
  ... a datacite file that contains invalid datacite entries leading to a rejection of the
      DOI request. This file should catch all invalid entries leading to a request rejection.
- datacite_03_unsupported.yml
  ... a datacite file that contains unsupported datacite field value entries leading to a
      rejection of the DOI request.
      Due to implementation reasons still separated from the previous step.
- datacite_04_dubious.yml
  ... a datacite file containing all entries that will lead to a successful DOI request,
      but will elicit warning messages to the admin. This file should cover all admin warnings.
- datacite_05_valid.yml
  ... a datacite file leading to a clean DOI request


## Deployment tests
The following describes the full rundown of all deployment tests. These tests require
a full test setup of a GIN server, a DOI server and a GIN CLI set up to work with these
instances.

### Pre-requisites
- ensure the GIN client is set up to work with the test instance of GIN before starting the tests.
- copy the contents of this directory and upload them to the GIN server instance.
- ensure the repository is public.
- ensure there is no DOI copy of this repository; if there is one, delete it.

### Missing and broken datacite.yml file; Missing LICENSE file
-[ ] remove LICENSE and datacite.yml file and upload
```bash
rm LICENSE
rm datacite.yml
gin commit .
gin upload .
```
-[ ] switch to the GIN repo and check missing DOI request link due to missing datacite file

-[ ] add datacite file and upload; reload the GIN page; request DOI
```bash
cp datacite_01_broken.yml datacite.yml
gin commit .
gin upload datacite.yml
```
-[ ] check DOI request failure due to broken datacite file:
    `error while reading DOI info: yaml [...]`

-[ ] add valid datacite file and upload; reload GIN page; request DOI
```bash
cp datacite_05_valid.yml datacite.yml
gin commit .
gin upload datacite.yml
```
-[ ] check DOI request failure due to missing LICENSE file:
    `The LICENSE file is missing. The full text of the license is required to be in the repository when publishing`

### Invalid datacite.yaml test
-[ ] add invalid LICENSE and unsupported datacite file and upload; reload GIN page; request DOI
```bash
cp LICENSE_invalid LICENSE
cp datacite_02_invalid.yml datacite.yml
gin commit .
gin upload datacite.yml
gin upload LICENSE
```
-[ ] check DOI request failures:
    - No title provided.
    - Not all authors valid. Please provide at least a last name and a first name.
    - No description provided.
    - No valid license provided. Please specify a license URL and name and make sure it matches the license file in the repository.
    - Not all Reference entries are valid. Please provide the full citation and type of the reference.

### Unsupported datacite.yaml test
-[ ] add unsupported datacite file and upload; reload GIN page; request DOI
```bash
cp datacite_03_unsupported.yml datacite.yml
gin commit .
gin upload datacite.yml
```
-[ ] check DOI request failures:
    - ResourceType must be one of the following: Dataset, Software, DataPaper, Image, Text
    - Reference type (RefType) must be one of the following: IsSupplementTo, IsDescribedBy, IsReferencedBy, IsVariantFormOf

