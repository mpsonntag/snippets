## gin-web build process
- in a new go project, run `go mod init` in the project root to automatically create the `go.mod` file listing the project dependencies.
- `go build` also creates and updates the `go.mod` file as well as the `go.sum` file.
- use `go -u get ./...` to force an update on the dependencies.
- changes to the `go.mod` file are only appended but not cleaned up with respect to unused dependencies. Run `go mod tidy` to clean up an existing `go.mod` file.

- check the `Makefile` at the project root for assets compilation of non go files.
- a build compiles these files into generated go files that are then used by the service; e.g. `internal/assets/public/public_gen.go`. The catch is that these files will differ when merging upstream changes into a branch. Ideally re-compiling will properly update, but it might be necessary to delete the existing files.
- for the re-build these are the gogs host dependencies for a local build; take care not to use `go-bindata/go-bindata`: https://github.com/gogs/gogs/blob/main/docs/dev/local_development.md#ubuntu; use `go get -u github.com/kevinburke/go-bindata/...` instead.

- make sure the go version and the go tool version are up to date and have the same version number
- run `make` to ensure that the build runs without problems; `make` will create the custom files mentioned above.


## gin build issues

take care not to use `go-bindata/go-bindata`: https://github.com/gogs/gogs/blob/main/docs/dev/local_development.md#ubuntu

use `go get -u github.com/kevinburke/go-bindata/...` instead

