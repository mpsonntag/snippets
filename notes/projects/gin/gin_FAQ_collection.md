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


## How to delete a branch

### Q
I'm trying to delete a branch I added by mistake to https://gin.g-node.org/[repo] and am unable to do so. Can you please kindly direct me to how I may do this?

### A
Deleting branches on the gin website is currently not supported.

Deleting a branch is possible using the gin client to send the git remote branch deletion command.

If you are unfamiliar with git or the gin client you can find installation instructions for the client here: https://gin.g-node.org/G-Node/Info/wiki/GIN+CLI+Setup
and a basic usage tutorial here: https://gin.g-node.org/G-Node/Info/wiki/GIN+CLI+Usage+Tutorial

To delete the branch, you will need to have the repository cloned to a local directory, then from within the repository run the following command:
gin git push -d origin branchname

where "branchname" is of course the name of the branch you want to delete.


## An upload via the webpage shows no progress or has stopped

### Q

I have been trying to upload data onto a repository but it seems to have stopped adding commits.
Is there a limit on how much we can upload to a repository?

### A

Uploads through the website should work without issue, but for large, long running uploads there is always a greater risk of the connection timing out or being interrupted and subsequent uploads will need to start over. To reduce the chance of long running uploads through the web form, we recommend submitting large repositories in small chunks and low file numbers to avoid timeouts.

As an alternative to the web upload the GIN command line client GIN-cli will resume a broken upload and makes it easier to keep track of what has been uploaded and what remains to be sent, which is important when uploading multiple files in multiple directories. To this end we recommend using the GIN client for large uploads instead of the web interface.
