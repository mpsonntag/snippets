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


## Files with a specific file ending are not uploaded

### Q
I am trying to upload files to a GIN repository, but files with a specific file ending e.g. "tif" or "nii" are not uploaded.

### A
GIN is based on git and will respect if files have been excluded from git. Check if there is a ".gitignore" file at the root of your repository where these files have been excluded.


## Modification of a dataset published with GIN-DOI

### Q
Once a DOI is issued for a dataset, can this dataset be modified in the future? I.e., can new data be added?

### A
The brief answer is, that the original GIN repository that was used to create the registered dataset can be changed after it has been used for a DOI publication. Further changes in the original GIN repository do not introduce changes in the published DOI dataset.
Further there is no automatic way to update the DOI dataset after the DOI has been issued. We can issue a different DOI for the same data repository if changes need need to be published as well.


## "Broken pipe" upload issue

### Q
On uploading to gin, we encounter the following error, what is the issue and how can it be resolved.

    :: Uploading
     Compressing OK
     Connection to gin.g-node.org closed by remote host.
    fatal: the remote end hung up unexpectedly
    fatal: sha1 file '<stdout>' write error: Broken pipe
    fatal: the remote end hung up unexpectedly
      Pushing to origin failed.
    git-annex: sync: 1 failed
    
    [error] 1 operation failed

### A
This error can occur when too many small files (each size < 10 MB) with a total sum size of > 4GiB have been committed with a single commit. Try splitting such a commit into multiple smaller ones so that the total sum size of committed files is below 4 GiB.

The reason behind this issue is, that only files with size > 10MB are checked into git annex that handles large files well. Files with a smaller size are still checked into git, which does not handle many or large files nearly as well as git annex does. In the described case, git cannot handle the sum size of files any longer and will fail on upload.


## Slow upload speed

### Q - My Upload speed is slow, what can you do

I experience uploading speed of about 1-2 MiB/s. Can you help increase the upload speed?

### A
With respect to upload speed, there is not really anything we can do or debug from our end. The service can handle and has handled upload speeds of 20MiB/s-100MiB/s in the past depending on the connection.

