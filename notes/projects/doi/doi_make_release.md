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

