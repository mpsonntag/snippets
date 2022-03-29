### test new server version

- make sure the server version number has been updated
- change to the doi git directory, make sure all fmt and tests are run, if required fix any issues and commit

```bash
golint ./...
go vet ./...
go fmt ./...
go test ./... -p 1
```

- build a server binary and a docker container; push the container

```bash
make
docker build -t gnode/gin-doi:dev
docker push gnode/gin-doi:dev
```

- move to the dev server and fetch the new version
- if required update the server config file

```bash
docker pull gnode/gin-doi:dev
```

- once everything is prepared, move to the docker-compose folder and restart the service; keep the logs open

```bash
docker-compose down
docker-compose up -d
docker-compose logs -f --tail=100
```

- run all required tests as described in the opsdocs `doi/deployment_tests.md` file or the gin `G-Node/doi_deployment_test` repository.

#### Updates in "checklist.go"

if the "checklist.go" file has been updated
- update the corresponding template in G-Node/gin-scripts/doichecklist.py
- update the version number of G-Node/gin-scripts/doichecklist.py to match the go server binary version number.
- test that the checklist output of go server binary and python script are identical:

```bash
./gindoid make-checklist
mv [created file] [created file].go
python doichecklist.py
diff [created file] [created file].go
```

- if diff only shows differences in the randomly created screen session names, the scripts create an identical output.

#### Updates to the deployment test scheme

If the deployment test scheme was updated, propagate these changes to all relevant directories:
- GIN G-Node/opsdosc/doi/deployment_tests.md
- GIN G-Node/doi_deployment_test
- dev GIN G-Node/doi_deployment_test
- GIN G-Node/gin-scripts


### Deployment preparations

When all tests have been successfully completed, run the following steps to prepare for a live deployment

- prepare the live docker containers; use the date when the new container will be deployed

```bash
docker tag [dev image id] gnode/gin-doi:latest
docker tag [dev image id] gnode/gin-doi:live-YYYY-MM-DD
docker push gnode/gin-doi:latest
docker push gnode/gin-doi:live-YYYY-MM-DD
```

- make sure the tested github changes have been merged into master and prepare a matching tag in the gin-doi git repository

```bash
git tag -a live-YYYY-MM-DD -m "GIN DOI Live-YYYY-MM-DD"
```

- move to the live server
- if the config has to be changed, move to the doi config folder and prepare a config file marked with the deployment day

```bash
cp doienv doienv.live-YYYY-MM-DD
vim doienv.live-YYYY-MM-DD  # make required changes
```

- pull the docker containers 

```bash
docker pull gnode/gin-doi:latest
docker pull gnode/gin-doi:live-YYYY-MM-DD
```

- copy the latest `gindoid` binary to the `data/doiprep` folder


### Live deployment and cleanup

- if required use the new config file

```bash
cp doienv-YYYY-MM-DD doienv
```

- on the DOI live server move to the docker-compose directory and restart the service; latch onto the logs to check if the service is running correctly

```bash
docker-compose down
docker-compose up -d
docker-compose logs -f --tail=200
```

- Log into gin.g-node.org, fork G-Node/doi_deployment test and run the tests again against the live DOI server; exclude the above locked content size test

- remove the created directories from `doi/10.12751` and `doiprep/10.12751`
- close any related GIN issues on the G-Node/DOIMetadata/issues repository

- now that everything is running without issue, finally push the git tag to the github gin-doi repo to finalize the release

```bash
git push upstream live-YYYY-MM-DD
```
