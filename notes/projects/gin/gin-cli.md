# gin-cli notes

## paths
- global settings are found in `$HOME/.config/g-node/gin`
- logs are found in `$HOME/.cache/g-node/gin`

### Windows
- logs are found in `ls %localappdata%/g-node/gin/gin.log`

### Run tests

- make sure git annex version 7+ is available where the test are being run
- NOTE that `sudo apt-get install git-annex` will currently install version 6 which is incompatible
- installation to a suitable [software directory]:
    ```bash
    cd [dir/of/choice]
    wget https://downloads.kitenet.net/git-annex/linux/current/git-annex-standalone-amd64.tar.gz
    tar xf git-annex-standalone-amd64.tar.gz
    # make the binaries available via the PATH variable
    export PATH=$PATH:$PWD/git-annex.linux
    ```

- clone the main repository
- fetch the submodule containing the tests
  ```bash
  git submodule update --init --recursive
  ```

- start the test gin servers: `./tests/start-server`
- run the tests: `./tests/run-all-tests`
