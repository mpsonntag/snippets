## GIN development and maintenance notes

### gin-web build process

General notes on 
- in a new go project, run `go mod init` from the project root to automatically create the `go.mod` file listing all project dependencies.
- `go build` also creates and updates the `go.mod` file as well as the `go.sum` file.
- use `go -u get ./...` to force a dependencies update.
- changes to the `go.mod` file are only appended but not cleaned up with respect to unused dependencies. Run `go mod tidy` to clean up an existing `go.mod` file.

- check the `Makefile` at the project root for assets compilation of non go files.
- a build compiles these files into generated go files that are then used by the service; e.g. `internal/assets/public/public_gen.go`. The catch is that these files will differ when merging upstream changes into a branch. Ideally re-compiling will properly update, but it might be necessary to delete the existing files.
- for a re-build these are the gogs host dependencies for a local build; take care not to use `go-bindata/go-bindata`: https://github.com/gogs/gogs/blob/main/docs/dev/local_development.md#ubuntu; use `go get -u github.com/kevinburke/go-bindata/...` instead.

- make sure the go version and the go tool version are up to date and have the same version number
- run `make` to ensure that the build runs without problems; `make` will create the custom files mentioned above.
- after running `make` or `make test`, `go.mod` and `go.sum` might have changed; in this case run `go mod tidy`.
- if a `make` run ever fails and functions in the code are supposedly missing, force the generation of all `_gen.go` files again running `make generate`.


### Keeping gnode/gogs up with gogs/gogs - general notes
- most custom GIN code should be either comment marked or moved to their own files/functions.
- cherry pick each commit from `gogs/gogs:main` to our branch.
- run `build` after a cherry-pick to catch obvious merge problems.
- check this PR as reference: https://github.com/G-Node/gogs/pull/88

- the current workflow to add new GIN features
  - add features to the `live` branch
  - test
  - deploy
  - merge the `live` branch into `master`
  - merge `master` into `live`
  
- upstream merge workflow
  - merge gogs `main` branch into the gnode gogs branch `upmaster`
  - check `git merge-base master upmaster`
  - check `tig [latest master commit]..[latest upmaster commit]`
  - the process is cherry-pick and not rebase! find the latest gnode/gogs master commit and make sure to find the same in `upmaster`, then go from there (as reference see github.com/G-Node/gogs/pull/88)
  - every couple of picked commits run `make` and `go build` to make sure nothing breaks
  - every ~60 commits deploy and test the G-Node specific features including DOI

- Identify a list of GIN specific commits
  ```bash
  # checkout the live branch that contains the latest tested version of gin-web
  git checkout live
  # compare the branch to the upmaster branch, that contains gogs/gogs only commits
  git cherry -v upmaster
  ```

#### gogs/gogs to g-node/gogs cherry pick preparations

```bash
# todo: add lines to clone gin-web and add gogs as remote
# fetch all branches from gnode/gogs and gogs/gogs
git fetch --all
# checkout gin-web master
git checkout upstream/master
# find latest commit from gogs and note the title
git log --oneline --graph
# checkout gogs main branch we keep in the gin-web repo
git checkout upstream/upmaster
# fetch the latest changes in the gogs/gogs main branch
# be aware that this branch is not necessarily runnable!
# might be worth to actually check the gogs releases and checkout the main branch at the latest release commit.
git pull gogs main
# find the commit that corresponds to the gin-web master commit identifier above
git log --oneline --graph
# get the full git log list-of-commits from the gin-web master commit until the latest gogs/main commit
# todo add command for the description above
git checkout master
# start cherry picking the list of commits from earliest to latest
```

#### gogs/gogs to g-node/gogs cherry pick process

- before doing an actual pick, check the commit to see and note the files that have been touched for later merge conflict resolve.
    ```bash
    git show --name-only [commit]
    ```
- on merge conflicts in `_gen` files run the following from the root of the repository.
    ```bash
    make
    # checkout all files that have not been touched by this commit
    git checkout [...]
    # resolve any further merge conflicts
    # if there is a large list of files, continuously `git add ...` the resolved files to not loose track of which have already been resolved.
    git cherry-pick --continue
    ```

#### Common merge conflict examples

gogs/gogs specific imports have to be adjusted for usage in g-node/gogs. When imports are affected by a commit, these imports have to be first adjusted and then moved to the G-Node project.

- Import fix example of an import that was deleted upstream:
    ```bash
    <<<<<<< HEAD
        "github.com/G-Node/gogs/internal/conf"
        "github.com/G-Node/gogs/internal/db/errors"
        "github.com/G-Node/gogs/internal/lazyregexp"
        "github.com/G-Node/gogs/internal/tool"
    =======
        "gogs.io/gogs/internal/conf"
        "gogs.io/gogs/internal/lazyregexp"
        "gogs.io/gogs/internal/tool"
    >>>>>>> 9e9ca6646... refactor: unify error handling in routing layer
    ```

    1) remove the import from the G-Node list of imports that was first removed by the upstream imports
    ```bash
    <<<<<<< HEAD
        "github.com/G-Node/gogs/internal/conf"
        "github.com/G-Node/gogs/internal/lazyregexp"
        "github.com/G-Node/gogs/internal/tool"
    =======
        "gogs.io/gogs/internal/conf"
        "gogs.io/gogs/internal/lazyregexp"
        "gogs.io/gogs/internal/tool"
    >>>>>>> 9e9ca6646... refactor: unify error handling in routing layer
    ```

    2) remove the upstream imports and leave only the G-Node ones
    ```bash
    "github.com/G-Node/gogs/internal/conf"
    "github.com/G-Node/gogs/internal/lazyregexp"
    "github.com/G-Node/gogs/internal/tool"
    ```

- import fix example of an import that was added upstream:
    ```bash
    <<<<<<< HEAD
        "github.com/G-Node/gogs/internal/conf"
    =======
        "gogs.io/gogs/internal/conf"
        "gogs.io/gogs/internal/errutil"
    >>>>>>> 9e9ca6646... refactor: unify error handling in routing layer
    ```

    1) add the import on the G-Node list of imports
    ```bash
    <<<<<<< HEAD
        "github.com/G-Node/gogs/internal/conf"
        "github.com/G-Node/gogs/internal/errutil"
    =======
        "gogs.io/gogs/internal/conf"
        "gogs.io/gogs/internal/errutil"
    >>>>>>> 9e9ca6646... refactor: unify error handling in routing layer
    ```

    2) remove the upstream imports
    ```bash
    "github.com/G-Node/gogs/internal/conf"
    "github.com/G-Node/gogs/internal/errutil"
    ```

- show diff between upstream and our state for a specific file to identify GIN specific code snippets in large changes
    ```bash
    git diff 6437d01 master -- public/js/gogs.js
    ```

#### Unsorted notes

setting up gogs on dev
    - problem of the gogs ORM connecting to the database in the database container
snippet: connect to DB from outside the container
    psql -h 172.24.0.1 -U postgres -d gin
problem is with the new ORM - might be that the latest state of gogs does not work yet at all (there is still an open ORM PR)
    - we should always only merge in gogs upstream changes when a release comes out to
avoid ending up in a non working state
    - check the gogs release branch or the gogs releases directly
G-Node/gogs
    - git branches ... use gogs-cherry-pick to keep up to date with the upstream changes
ok. plan
    - keep the gogs-cherry-pick up with gogs main to
docker tagging
    - gin-web:live-YYYY-MM-DD       ... to tag the version that is actually deployed
    - gin-web:cherry-YYYY-MM-DD     ... to tag the version that is to be tested with gogs upstream changes


- gin user specific code in files to document:
  internal/db/user.go
  - func IsBlockedDomain(email string) bool {


-[x] GIN (GOGS)
  - gogs update integration
    - now all add code is either comment marked or moved to their own files/functions
    - now cherry pick each commit from gogs/master to our branch
    - run build after the commit to catch obvious merge problems
    - check for reference with this PR: https://github.com/G-Node/gogs/pull/88


dumdribille  3:17 PM
git cherry  from the live branch towards current master  should tell which commits to cherry-pick from live, right?
3:18
I can pack that into the current PR as well
3:18
maybe ideally before removing the dav code
achilleas  3:24 PM
Not sure what git cherry live master would show exactly in this case.  git log 4cbb0d4..live are the commits in live that diverge from master.
3:26
git cherry master live shows me 19 commits.
git log --oneline $(git merge-base live master)..live shows me 26. (updated: local clone was out of date) (edited) 
dumdribille  3:26 PM
cherry does the same as log but without the merge commits it seems


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


### GIN build issues

Take care not to use `go-bindata/go-bindata`: https://github.com/gogs/gogs/blob/main/docs/dev/local_development.md#ubuntu
Use `go get -u github.com/kevinburke/go-bindata/...` instead.
