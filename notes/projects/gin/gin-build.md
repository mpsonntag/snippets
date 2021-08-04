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


## Keeping GOGS up with upstream
- currently all custom GIN code is either comment marked or moved to their own files/functions.
- cherry pick each commit from `GOGS/master` to our branch.
- run `build` after the commit to catch obvious merge problems
- check for reference with this PR: https://github.com/G-Node/gogs/pull/88

- the current workflow to add new gin features
  - add it to the `live` branch
  - test
  - deploy
  - merge the `live` branch into `master`
  - merge `master` into `live`


## local deployment notes

- run a local gogs service from a staging directory with the following structure:

```bash
+ config/
+ data/
+ docker-compose.yml
```

- minimal local docker-compose.yml

```yaml
version: '3.3'
services:
  web:
    image: gnode/gin-web:local
    volumes:
      - ${PWD}/data:/data:rw
      - ${PWD}/config:/gogs-custom:rw
    environment:
      - PUID=${USEROWN}   # set to user owning directories mapped to container exterior
      - PGID=${GROUPOWN}  # set to group owning directories mapped to container exterior
      - GOGS_CUSTOM=/gogs-custom
    restart: unless-stopped
    networks:
      net:
        ipv4_address: 172.30.0.10
        aliases:
          - ginweb
networks:
  net:
    ipam:
      driver: default
      config:
        - subnet: 172.30.0.0/16
```

- run `docker-compose up -d` from `docker-compose.yml` file directory
- make sure all files in the staging directories are owned by the user set for the docker project
- if not, `sudo chown [username]:[usergroup] -R config/` and `sudo chown [username]:[username] -R data/`
- go to http://[IP from docker-compose]:3000
- run through the gogs service setup
    - select SQLite3 for local testing and postgres for all other
    - use `/data/gogs.db` for local db persistence
    - set domain and http port, leave ssh and do not select built in server ssh
    - logging ... select enable console log; prints messages to the console which in a docker container shows up in the docker logs
    - email settings ... ???
    - admin account settings ... add a user a the first admin; if this is not set up, the first user created will be an admin
- update the created `~/staging/config/app.ini` with any required keys
- `app.ini` critical keys description

        [repository]
        FORCE_PRIVATE = True
        // use setting 0 to make disallow repository creation
        MAX_CREATION = 0
        // the following two settings are actually no longer supported and the code has been removed from the codebase
        // they were both to determine the file size of displaying files online either directly or raw until asking for a captcha
        RAW_CAPTCHA_MIN_FILE_SIZE
        CAPTCHA_MIN_FILE_SIZE

        [security]
        // once set, do not change the secure key
        COOKIE_USERNAME = gin_user
        COOKIE_REMEMBER_NAME = gin_user_remember

        [email]
        // could set to true to decrease spaminess
        USE_PLAIN_TEXT = True

        [service]
        // the time in minutes until the email account activation code is invalid
        ACTVIE_CODE_LIVE_MINUTES

        [prometheus]
        // required for some monitoring features

        [i18n]
        // could be narrowed down to en only


## gin build issues

take care not to use `go-bindata/go-bindata`: https://github.com/gogs/gogs/blob/main/docs/dev/local_development.md#ubuntu

use `go get -u github.com/kevinburke/go-bindata/...` instead

