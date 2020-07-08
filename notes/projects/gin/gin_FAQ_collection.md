## Upload of large files fails

### Q
I am currently trying to update from local to remote, using the command 'gin upload .', on the local machine most files have been changed, removed, etc.
When I run the command, for all large files the command displays:

    `Added to git "path/filename.nii.gz" failed`

While small files, e.g. ending in '.txt', the command displays an OK.

### A
It looks like the installed git package is an old version and git-annex is probably relying on some newer features to version larger files.  This is most likely the source of your issue. If possible, update the git binary on the local machine.

### Further investigation
To pinpoint the issue check the output of the `gin --version` command. This will show the version of the gin client as well as git and git-annex.
It will also be useful to check the client log file. It can be found in the following locations:
- Windows: `C:\Users\<User>\AppData\Local\g-node\gin\gin.log`
- macOS: `/Users/<User>/Library/Caches/g-node/gin/gin.log`
- Linux: `/home/<User>/.cache/g-node/gin/gin.log`

Before checking the log, try to run 'gin upload' again to make sure that the failure and any pertinent information is included in the logfile.
