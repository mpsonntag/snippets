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


### Dubious datacite yaml test
-[ ] add dubious datacite entries file and upload; reload GIN page; request DOI
```bash
cp datacite_04_dubious.yml datacite.yml
gin commit .
gin upload datacite.yml
```
-[ ] check that the DOI request was valid
-[ ] check that both the admin email and the DOIMetadata issue contain the following warning messages
    - Author 1 (MisterB) has ORCID-like unspecified ID: 0000-0002-7937-1095
    - Authors 2 (MadamC) and 3 (MisterD) have the same ID: orcid:0000-0003-2524-3853
    - Author 5 (MadamF) has unknown ID: idonotexist:1234
    - Author 6 (MisterG) has empty ID value: ORCID:
    - Abstract may be too short: 24 characters
    - License file content header not found: 'This is not right Cr...'
    - License URL/Name mismatch: 'CC0 1.0 Universal'/'Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public License'
    - License name/file header mismatch: 'Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public License'/''
    - Couldn't find funder ID for funder "Only funder ID is here"
    - Couldn't find funder ID for funder "new style ID"
    - Couldn't find funder ID for funder "old style ID"
    - Reference 2 uses refType 'IsReferencedBy'
    - Reference 4 has no related ID type: '10.12751/g-node.6953bb'; excluded from XML file
    - Reference 5 uses refType 'IsReferencedBy'
    - Reference 9 uses old 'Name' field instead of 'Citation'
    - ResourceType is "DataPaper" (expected Dataset)
-[ ] Check that reference 4 has been excluded from the created XML file on the DOI server


### Valid datacite yaml test and registration procedure test
- add valid datacite yaml, valid and matching LICENSE file and upload; reload GIN page; request DOI
```bash
cp datacite_05_valid.yml datacite.yml
cp LICENSE_valid LICENSE
gin commit .
gin upload datacite.yml
gin upload LICENSE
```
-[ ] check that the DOI request was valid
-[ ] check that the DOIMetadata issue does not contain warning messages and that no warning email has been sent.
-[ ] check that the repository on the DOI server is present in the doiprep folder

-[ ] upload another file to the gin repository
```bash
touch tmp.yml
gin commit .
gin upload tmp.yml
```
-[ ] use the `doichecklist.py` script from the gin.g-node.org/G-Node/gin-scripts to register this request as a semi-automated DOI request. Make sure to update the `doichecklist.yml` config file to match the dev server environment.
-[ ] check the DOI fork upload log for an annex upload.
-[ ] note during the DOI fork upload that the logfile should show, that the repository was not at the
    expected commit. The commit hashes should point to the DOI request commit and the commit that post DOI request committed the `tmp.yml` file.
