# gin-cli notes

## upload speed
It's on a gigabit line, so if you're really close (or on the internal network), you can pretty much saturate that during a push.  Like I can get almost 100 MiB/s from my old workstation in the office.
1:34
let me see how fast I can upload from home
1:36
from home I can upload at 15~20 MiB/s.  It fluctuates a lot, but that's about my connection speed.  So his 2 MiB/s upload is on his end or just down to the route between him and the LRZ (edited) 
1:36
Hard limit on everything for gin is gigabit though

## paths
- global settings are found in `$HOME/.config/g-node/gin`
- logs are found in `$HOME/.cache/g-node/gin`

    - Windows: `C:\Users\<User>\AppData\Local\g-node\gin\gin.log`
    - macOS: `/Users/<User>/Library/Caches/g-node/gin/gin.log`
    - Linux: `/home/<User>/.cache/g-node/gin/gin.log`Before checking the log, try to run 'gin upload' again to make sure that the failure 

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
