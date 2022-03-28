# GIN-DOI deployment tests

The following describes how a new gin-doi release can be tested in a test deployment or the live environment. Currently, all necessary files and a copy of this script can be found in the [G-Node/doi_deployment_test](https://gin.g-node.org/G-Node/doi_deployment_test/) repository on gin. In the future these files should also be included in the [github gin-doi code repo](https://github.com/G-Node/gin-doi).

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
  ... license file used for DOI requests; replace this file
- LICENSE_invalid
  ... license file with an invalid header - should be caught by the DOI server on request
- LICENSE_valid
  ... valid CC0 license
- datacite.yml
  ... datacite file used for DOI requests; replace this file
- datacite_01_broken.yml
  ... a datacite file that is not a valid yaml file; checks broken yaml response
- datacite_02_invalid.yml
  ... a datacite file that contains invalid and unsupported datacite entries leading to a rejection
      of the DOI request. This file should catch all invalid entries leading to a request rejection.
- datacite_03_issues.yml
  ... a datacite file containing all entries that will lead to a successful DOI request,
      but will elicit warning messages to the admin. This file should cover all admin warnings.
- datacite_04_valid.yml
  ... a datacite file leading to a clean DOI request


## Deployment tests
The following describes the full rundown of all deployment tests. These tests require
a full test setup of a GIN server, a DOI server and a GIN CLI set up to work with these
instances.

### Pre-requisites
- ensure the GIN client is set up to work with the `dev` instance of GIN before starting the tests. (check below for an example how to set up the gin client to work with dev)
- copy the contents of this directory and upload them to the GIN server instance.
- ensure the repository is public.
- ensure there is no DOI copy of this repository; if there is one, delete it.
- ensure there is no repository named "doi_deptest_doidev"; if there is one, delete it; this ensures that the large data files and the git history of the main test repository will remain clean and test against branches can also be done without too much overhead.
- fork the repository to "doi_deptest_doidev"


### Check missing or broken datacite.yml file and missing LICENSE file responses
-[ ] check there is no option to request a DOI on GIN; make the original repository public via the settings
-[ ] check there still is no option to request a DOI on GIN due to missing datacite file
-[ ] locally clone the forked repository
```bash
gin get [username]/doi_deptest_doidev
cd doi_deptest_doidev
```

-[ ] use the `datacite_01_broken.yml` file and upload; reload the GIN page; request DOI

```bash
cp datacite_01_broken.yml datacite.yml
gin commit .
gin upload datacite.yml
```

-[ ] check the error messages for missing LICENSE file and missing/invalid DOI file and proper information on the nature of the broken yaml issue
  - `The LICENSE file is missing the required master branch [...]`
  - `The DOI file is missin in the master branch or not valid [...]`
  - `[...] error while reading DOI info: yaml: line xx: mapping values [...]`

-[ ] use the `datacite_04_valid.yml` file and upload; reload GIN page; request DOI

```bash
cp datacite_04_valid.yml datacite.yml
gin commit .
gin upload datacite.yml
```

-[ ] check DOI request failure due to missing LICENSE file:
    - `The LICENSE file is missing the required master branch [...]`


### Check invalid datacite.yaml responses
-[ ] use `LICENSE_invalid` and `datacite_02_invalid.yml` files and upload; reload GIN page; request DOI

```bash
cp LICENSE_invalid LICENSE
cp datacite_02_invalid.yml datacite.yml
gin commit .
gin upload datacite.yml LICENSE
```

-[ ] check DOI request failures:
    - No title provided.
    - Not all authors valid. Please provide at least a last name and a first name.
    - No description provided.
    - No valid license provided. Please specify a license URL and name and make sure it matches the license file in the repository.
    - Not all Reference entries are valid. Please provide the full citation and type of the reference.
    - ResourceType must be one of the following: Dataset, Software, DataPaper, Image, Text
    - Reference type (RefType) must be one of the following: IsSupplementTo, IsDescribedBy, IsReferencedBy, IsVariantFormOf


### Test formal datacite.yml issues and git submodules warnings
-[ ] use the datacite_03_issues.yml file and upload; reload GIN page; request DOI

```bash
cp datacite_03_issues.yml datacite.yml
touch .gitmodules
gin commit .
gin upload datacite.yml .gitmodules
```

-[ ] check that the DOI request was valid
-[ ] check that the git submodules warning is displayed at the top of the page
-[ ] submit DOI request and check that both the admin email and the DOIMetadata issue contain the following warning messages
    - Repository contains submodules
    - Author 1 (PersonB) has unknown ID:
    - Author 2 (PersonC) has ORCID-like unspecified ID: 0000-0002-7937-1095
    - Author 3 (PersonD) has unknown ID: idonotexist:1234
    - Author 4 (PersonE) has empty ID value: ORCID:
    - Authors 7 (PersonH) and 8 (PersonI) have the same ID: orcid:0000-0001-6744-1159
    - Author 5 (PersonF) ID was not found at the ID service: orcid:0000-0003-2524-3853
    - Author 6 (PersonG) ID was not found at the ID service: ResearcherID:D-1234-5678
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
    - Annex content size (0 bytes) vs zip size (48 KiB)

-[ ] check that reference 4 value has been excluded from the created XML file on the DOI server
-[ ] check that the zip file on the server has the appropriate size
-[ ] check that references 14 and 15 have been added in the created XML file on the DOI server with an amended DOI id.


### Test valid datacite yaml test and registration procedure
-[ ] add random data files for the annex
-[ ] add valid datacite yaml, valid and matching LICENSE file and upload; reload GIN page; request DOI

```bash
mkdir data
head -c 11M /dev/urandom > data/sampleA.bin
rm .gitmodules
cp datacite_04_valid.yml datacite.yml
cp LICENSE_valid LICENSE
gin commit .
gin upload .
```

-[ ] check that no errors are displayed and no git submodules warning is displayed at the top of the request overview page
-[ ] request the DOI
-[ ] check that the DOIMetadata issue does not contain warning messages 
-[ ] check that the second admin email only contains the annex content vs zip size notice
-[ ] check that the repository on the DOI server is present in the doiprep folder

-[ ] upload another file to the gin repository

```bash
head -c 11M /dev/urandom > data/sampleB.bin
gin commit .
gin upload .
```

-[ ] use the doichecklist file found in the corresponding server doiprep folder to register this request as a semi-automated DOI request.  Alternatively use the `doichecklist.py` script from the gin.g-node.org/G-Node/gin-scripts repository to register this request as a semi-automated DOI request. Make sure to update the `doichecklist.yml` config file to match the dev server environment.
-[ ] check the DOI fork upload log for an annex upload.
-[ ] during the DOI fork upload the logfile should show that the repository was not at the expected commit. The commit hashes should point to the DOI request commit and the commit that post DOI request committed the `data/sampleB.bin` file.


### Test locked content
-[ ] Lock a binary content file, commit and upload the changes and request a new DOI

```bash
gin lock data/sampleB.bin
gin commit .
gin upload .
```

-[ ] check the admin email
    - warns about the repository being already forked
    - informs about the annex and the zip size
-[ ] check that the server doiprep folder contains a `doi_deptest_doidev_unlocked` directory
-[ ] check that `sampleB.bin` is locked in the `doi_deptest_doidev` and unlocked in the `doi_deptest_doidev_unlocked` directory
-[ ] check that the zip file contains all required data

#### Optional locked content size cutoff test
-[ ] make sure the server has a cutoff size of 1 GB set in the server configuration
-[ ] add files adding to over 1GB, lock these files, upload and request a DOI

```bash
head -c 250M /dev/urandom > data/sampleC.bin
head -c 250M /dev/urandom > data/sampleD.bin
head -c 250M /dev/urandom > data/sampleE.bin
head -c 250M /dev/urandom > data/sampleF.bin
gin commit .
gin lock data/sampleC.bin
gin lock data/sampleD.bin
gin lock data/sampleE.bin
gin lock data/sampleF.bin
gin commit .
gin upload .
```

- [ ] check the admin email notices for errors and warnings:
    - error: locked files found, zip creation skipped, repo size unsupported
    - warnings: repo already forked by DOI, annex size message
- [ ] check the server
  - no zip file in the `doi` folder
  - only the `doi_deptest_doidev` directory in the `doiprep` folder
  - checklist available


### Branch check
- [ ] check that a DOI request cannot be made from a branch other than master. It is a bit of a hastle, but it has happend before; so lets make sure this is caught.

```bash
gin git checkout -b main
rm data -r
gin commit .
gin upload .
```

- [ ] access the `doi_deptest_doidev` settings page, access the `branches` section and set the default branch to `main`; then delete the `master` branch and request a new DOI.

```bash
gin git branch -D master
gin git push origin :master
```

- [ ] check that a proper page is displayed and the error message contains:
  - `Could not access the repository master branch [...]`


### Cleanup
-[ ] delete all sub-directories in the doi and doiprep on the dev server
-[ ] delete the doi_deptest_doidev repository via the dev GIN page
-[ ] delete any potential DOI forks via the dev GIN page


### Set up the gin client to work with the development server

- use the appropriate gin.dev.g-node.org settings, values below are exemplary

```bash
gin add-server --web https://gin.dev.g-node.org:443 --git git@gin.dev.g-node.org:9999 dev
gin use-server dev
gin login yourdevuser
```

- don't forget to switch back to using the "normal" gin server once the tests on dev are done
