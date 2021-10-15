# Test scheme for the gin services

## Server landscape
- gin.dev.g-node.org
- doi.dev.g-node.org
- gintest.dev.g-node.org
- doitest.dev.g-node.org

## Test setup variants
- running tests via an off-site CI is probably not a good idea
- create a test repo, that integrates tests against the test environment.
- this repo should include tests against all relevant projects:
  - gogs
  - gin-cli
  - doi
- will probably be cumbersome at first, since it is run locally and requires manual steps
- if time permits could be automatized using a frontend test engine like selenium

- this means tests are either pure Python or a mixture of Python and go.
- the repo should be built upon the gin-cli test repo that already exists.

## Basic gin-web tests

- download G-Node/gin-cli-releases repo
- get content of an annex file
- copy to doitest, commit
- gin upload
- request doi for doitest

## Database change considerations

- check whether changes in the OR mapper remove existing columns
- if yes, fetch Update statements before deploying a new OR version
    -> in the current case identify all columns that contain unlisted and create update statements for the new database scheme.
