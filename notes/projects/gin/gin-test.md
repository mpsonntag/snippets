# Test scheme for the gin services

## Server landscape
- gin.dev.g-node.org
- doi.dev.g-node.org
- gintest.dev.g-node.org
- doitest.dev.g-node.org

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
