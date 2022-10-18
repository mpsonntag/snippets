## FAQ

### Overview
- [Common DOI questions](#Common-DOI-questions)
- [General GIN questions](#General-GIN-questions)
- [Find answers to common GIN Web questions](#Common-GIN-Web-questions)
- [Find answers to common GIN client questions](#Common-GIN-Client-questions)
- [General Troubleshooting](#Troubleshooting)

### Specific DOI questions
- [How can I get a DOI for my data?](#how-can-i-get-a-doi-for-my-data)
- [How can I modify a dataset published with GIN-DOI](#How-can-I-modify-a-dataset-published with-GIN-DOI)

### General GIN questions 
- [How can I access the data?](#how-can-i-access-the-data)
- [Is there a list of all GIN client commands?](#is-there-a-list-of-all-gin-client-commands)
- [Can I invite other collaborators who are not registered with GIN?](#can-i-invite-other-collaborators-who-are-not-registered-with-gin)
- [Can I share a repository with a collaborator or journal using a private link or access token?](#can-i-share-a-repository-with-a-collaborator-or-journal-using-a-private-link-or-access-token)
- [Do I have to use git-annex?](#do-i-have-to-use-git-annex)
- [Can I use GIN as a data provider for my research consortium/institute/department/working group with many collaborators and potentially a lot of terabytes of data?](#can-i-use-gin-as-a-data-provider-for-my-research-consortiuminstitutedepartmentworking-group-with-many-collaborators-and-potentially-a-lot-of-terabytes-of-data)


## Specific GIN Web questions
- [An upload via the webpage shows no progress or has stopped](#An-upload-via-the-webpage-shows-no-progress-or-has-stopped)
- [How to delete a branch](#How-to-delete-a-branch)

## Specific GIN Client questions
- [Answers to client setup questions](#GIN-Client-setup-questions)
- [Answers to client usage questions](#GIN-Client-usage-questions)
- [GIN CLI says "nothing to do" but there are files missing on the server](#GIN-CLI-says-nothing-to-do-but-there-are-files-missing-on-the-server)
- [GIN CLI fails to upload with general error](#GIN-CLI-fails-to-upload-with-general-error)
- [Using the GIN client behind a proxy](#Using-the-GIN-client-behind-a-proxy)
- [Slow upload speed](#Slow-upload-speed)
- [Files with a specific file ending are not uploaded](#Files-with-a-specific-file-ending-are-not-uploaded)
- [How to Unannex files](#How-to-Unannex-files)
- [Large local directory size after file deletion](#Large-local-directory-size-after-file-deletion)
- [Dropping file content removes content from more than the specified file](#Dropping-file-content-removes-content-from-more-than-the-specified-file)
- [A file upload has failed](#A-file-upload-has-failed)
- [Broken pipe upload issue](#Broken-pipe-upload-issue)
- [Unspecified client error message [error] 1 operation failed](#Unspecified-client-error-message-[error]-1-operation-failed)
- [Disconnect reading sideband packet upload issue](#Disconnect-reading-sideband-packet-upload-issue)

## Troubleshooting
- [I found a bug, something is not working, or "I don't know what to do"](#i-found-a-bug-something-is-not-working-or-i-dont-know-what-to-do)
- [Why do I see files with some strange text like "annex" or "WORM" instead of file content?](#why-do-i-see-files-with-some-strange-text-like-annex-or-worm-instead-of-file-content)

---

### Common DOI questions

#### How can I get a DOI for my data?
See details [here](wiki/DOIfile).
##### Short overview:
* [Create a repository] (https://gin.g-node.org/G-Node/Info/wiki/Web+Interface#creating-a-repository)
* Upload data (using the [Website](https://gin.g-node.org/G-Node/Info/wiki/Web+Interface#uploading-files), our client, or git{annex})
* Create a [DOI request](wiki/DOIfile#structuring-the-doi-request-file) file (`datacite.yml`)
* Set repository to [public] (https://gin.g-node.org/G-Node/Info/wiki/Web+Interface#repository-settings)
* Hit doi button


#### How can I modify a dataset published with GIN-DOI
Once a DOI is issued for a dataset, can this dataset be modified in the future? I.e., can new data be added?

*Answer*

The original GIN repository that was used to create the registered dataset can be changed after it has been used for a DOI publication. Further changes in the original GIN repository do not introduce changes in the published DOI dataset.
Further there is no automatic way to update the published DOI dataset after the DOI has been issued. Simply request a new DOI using the updated data repository if changes need to be published as well.

---

### General GIN questions

#### How can I access the data?
At GIN we believe that there should ideally be several ways to achieve the same thing. So to access the data you can:
* Download the data file by file using the [web interface](wiki/Web+Interface#downloading-files)
* Download the data using git and git-annex
* Download the data using the [GIN client](wiki/GIN+CLI+Setup#quickstart)
* Download the data using [WebDAV](wiki/Dav)
* Download the Data as zip, tar or gin archive (big files are not included and can be fetched later using one of the methods above)


#### Is there a list of all GIN client commands?
Of course there is! [Here!](wiki/GIN+CLI+Help)


#### Can I invite other collaborators who are not registered with GIN?
Yes, you can! Here is how:
1. Navigate to the main page of your repository. Your url should look like this `gin.g-node.org/<your_username>/<your_repository>` and you should see all the files contained within your repository.
2. Click on the Settings button in the top right-hand corner, which will lead you to your repository settings.
3. Within your repository settings, you need to click on the Collaboration tab on the left side.
4. This will leave you with two options:
    - Add a new collaborator: This is for users who are registered with GIN
    - Invite a collaborator: This is for non-registered users. This is what you are looking for! But be aware that sharing your repository and hence your data via email is much less safe than sharing it only with already registered users. This is why we recommend sharing your repository only via the first option.


#### Can I share a repository with a collaborator or journal using a private link or access token?
At the moment, it is not possible to share a **private** repository with someone who does not have a GIN account. There are, however, several options you can use to grant access without requesting that others sign up themselves.

- Create a new GIN account for the purpose of sharing your repository. You can add that account as a [collaborator](wiki/Web+Interface#collaboration) of your repository and provide the password to your collaborator or along with your submission to a journal. The account may be [deleted](wiki/Web+Interface#deleting-a-repository) afterwards if needed.
- Using the [collaboration page](wiki/Web+Interface#collaboration) of  your repository settings, you can automatically set up such a sharing account and send an invitation E-mail.
- If the [visibility](wiki/Web+Interface#basic-settings) of a repository is set to public and it is not listed, only those who happen to somehow know to the repository link will be able to view its contents. Please be aware that this option may leave your data vulnerable, as it can not be excluded that others may gain access to the link without your knowledge.


#### Do I have to use git-annex?
Strictly speaking No.  A better answer, however, would probably be: It depends on the size of your data!

* If you have only small files, just use gin as a normal [git](https://git-scm.com/) hosting provider.
* If you have big files, download our [local GIN client](wiki/GIN+CLI+Usage+Tutorial) for your operating system. Then, you can access and upload your data (unlimited file size) using the GIN command line client. Alternatively to the GIN client, you can use [git](https://git-scm.com/) and [git annex](https://git-annex.branchable.com/) directly to upload and manage large files! Be sure to check the [usage notes](wiki/Some+Notes+On+Git+Annex).


#### Can I use GIN as a data provider for my research consortium/institute/department/working group with many collaborators and potentially a lot of terabytes of data?
Sure! However, if you need **guaranteed** access to a lot of free storage we expect that you cover the additional costs associated with it. Please [get in touch](wiki/contact) with us about the details. Also, consider that data transfer takes its time. You can of course also set up your own gin server [in-house](wiki/In+House). We are happy to be of assistance, if necessary.

---

## Common GIN Web questions

### An upload via the webpage shows no progress or has stopped

I have been trying to upload data onto a repository but, it seems to have stopped adding commits. Is there a limit on how much we can upload to a repository?  

*Answer*

Uploads through the website should work without issue, but for large, long running uploads there is always a greater risk of the connection timing out or being interrupted and subsequent uploads will need to start over. To reduce the chance of long running uploads through the web form, we recommend submitting large repositories in small chunks and low file numbers to avoid timeouts.

As an alternative to the web upload the GIN command line client GIN-cli will resume a broken upload and makes it easier to keep track of what has been uploaded and what remains to be sent, which is important when uploading multiple files in multiple directories. To this end we recommend using the GIN client for large uploads instead of the web interface.


### How to delete a branch
I'm trying to delete a branch I added by mistake to https://gin.g-node.org/[repo] and am unable to do so. Can you please kindly direct me to how I may do this?

*Answer*

Deleting branches on the GIN website is currently not supported.

Deleting a branch is possible using the GIN commandline client to send the git remote branch deletion command.

If you are unfamiliar with git or the gin client you can find installation instructions for the client [here](https://gin.g-node.org/G-Node/Info/wiki/GIN+CLI+Setup) and a basic usage tutorial [here](https://gin.g-node.org/G-Node/Info/wiki/GIN+CLI+Usage+Tutorial).

To delete the branch, you will need to have the repository cloned to a local directory, then from within the repository run the following command:

```bash
gin git push -d origin branchname
```

where `branchname` is of course the name of the branch you want to delete.


## Common GIN Client questions

### GIN Client setup questions

#### GIN CLI says nothing to do but there are files missing on the server
Sometimes due to a misconfiguration or a network issue, git-annex might fail to contact the GIN server, while git commands still work. This can make the application incorrectly assume that the GIN server does not support git-annex and disable annex support for it. If this is the case, then the configuration file for the repository, which can be found at `.git/config` inside the local repository directory, will have a line that reads `annex-ignore=true`.

Git annex support can be re-enabled for the remote by removing the line. Alternatively, the following command, when run from inside the repository, will also toggle the setting to its correct value.

```bash
git config remote.origin.annex-ignore false
```

If your remote is not named `origin`, make sure to use the correct name in the command.


#### GIN CLI fails to upload with general error
Under certain circumstances, the GIN CLI can fail to upload (or download) data without giving clear errors about what's going on.
A few common scenarios for this happening are described below.

##### Outdated dependencies
GIN CLI uses git and git-annex to manage repositories. These applications also require a number of common utilities such as SSH and OpenSSL. If old versions of these are already installed on the system, they may behave in different ways than how GIN CLI expects. This is more common on Windows. The GIN CLI Bundle provides all these programs, however other versions of the same programs may exist on the system as well.

If you used the `set-global.bat` file to [make GIN CLI available everywhere](https://gin.g-node.org/G-Node/Info/wiki/GIN+CLI+Setup#windows), you can try using the `gin-shell.bat` instead. If the problem does not occur when running `gin upload` or `gin download --content` in `gin-shell.bat`, then the problem may be fixed permanently by editing the `set-global.bat`.

Open the file in a text editor and find the following line:
```bat
echo %path%|find /I "%curdir%">nul || setx path "%path%;%ginbinpath%;%gitpaths%"
```

Change it to the following:
```bat
echo %path%|find /I "%curdir%">nul || setx path "%ginbinpath%;%gitpaths%;%path%"
```

Then double click the file to fix the system path.
This change will make the GIN CLI version of the programs have higher priority than the other versions.

##### Diagnosing other issues
Some errors don't provide clear error messages through GIN CLI, but can point towards the root of the issue if the underlying git and git-annex commands are used on their own. If you are having trouble uploading or downloading files and the above solution didn't help, the following command might provide more information:
```
gin annex sync
```

To upload and download all annexed data as well, run:
```
gin annex sync --content
```

Feel free to contact us for further assistance in one of the following ways:
- Open an issue [on the GIN issue tracker](https://gin.g-node.org/G-Node/Info/issues).
- Send an email to [**gin@g-node.org**](mailto:gin@g-node.org).


#### Using the GIN client behind a proxy
GIN CLI communicates with the GIN server in two ways:
1. HTTP(S) for API calls to perform actions such as login, creating repositories on the server, listing repositories, etc.
2. Git over SSH for downloading data (pulling) from and uploading data (pushing) to the repository.

Each method requires separate settings for working with proxies.
For git, the proxy must support SSH communication, which isn't always the case with web proxies.

##### Web proxy
Since GIN CLI runs on the command line, the system proxy settings, which are typically meant for web browsing, don't apply.
Instead, the environment variables `HTTP_PROXY` and `HTTPS_PROXY` need to be set.
The method varies based on operating system and command shell:
- Windows:
  - Temporarily for cmd.exe: `set HTTP_PROXY=proxy.host:port` and `set HTTPS_PROXY=proxy.host:port` (where `proxy.host` is the address of your proxy server and `port` is the port).
  - Temporarily for PowerShell: `$Env:HTTP_PROXY = "proxy.host:port"` and `$Env:HTTPS_PROXY = "proxy.host:port"` (where `proxy.host` is the address of your proxy server and `port` is the port).
  - Globally and permanently: see [this guide](https://www.onmsft.com/how-to/how-to-set-an-environment-variable-in-windows-10).
- Linux and macOS:
  - Temporarily: `export HTTP_PROXY=proxy.host:port` and `export HTTPS_PROXY=proxy.host:port` (where `proxy.host` is the address of your proxy server and `port` is the port).
  - Permanently: This depends on the shell you are using. The commands `export HTTP_PROXY=proxy.host:port` and `export HTTPS_PROXY=proxy.host:port` (where `proxy.host` is the address of your proxy server and `port` is the port) should be added to your shell's startup script, e.g., `~/.bashrc` for bash, `~/.zshrc` for ZSH.

##### Git/SSH
For git to use the proxy server through SSH, the SSH configuration settings need to be edited.
There is no straightforward, single configuration for setting configuring SSH through a proxy.
Please consult with your lab or institution administrator for how to configure SSH to work through the proxy.


### GIN Client usage questions

#### Slow upload speed
I experience uploading speed of about 1-2 MiB/s. Can you help increase the upload speed?

*Answer*
With respect to upload speed, there is not really anything we can do or debug from our end. The service can handle and has handled upload speeds of 20MiB/s-100MiB/s in the past depending on the connection.


#### Files with a specific file ending are not uploaded
I am trying to upload files to a GIN repository, but files with a specific file ending e.g. "tif" or "nii" are not uploaded.

*Answer*

GIN is based on git and will respect if files have been excluded from git. Check if there is a `.gitignore` file at the root of your repository where these files have been excluded.


#### How to Unannex files
I committed one file too many. How do I get the file out of the annex before uploading?

*Answer*
An annexed file can be removed from the annex and from gin tracking using the following command.

```bash
gin git annex unannex [path/filename]
```

Note that a commit is required to fully remove a file from gin tracking. Also note that currently if the file content is not locally available, there will be no message at all and the commit will not change the status.
Make sure to `gin get-content [path/filename]` first, if the content is only available remotely. You can check which files have no local content by running `gin ls`.


#### Large local directory size after file deletion
I removed large files from my project that I did not need any longer. Still my directory requires too much disk space.

*Answer*
When files are deleted from the project, they still remain in the history. If for example a file got deleted by mistake in the past, you can go back and restore it.  
The deleted file will always remain on the server, but if you want to free up the space locally, there are two ways to deal with this situation:
- If you have not deleted a large file yet, first remove the file content from your local gin store by using the `gin remove-content [large_file]` command. Now you can safely delete the file without any leftover space occupied in your local history. You can still checkout an earlier commit and retrieve this file from the server.
- If you have already deleted this file without removing the file content first, you can free up this space by locally removing your gin directory and clone it again from the server. Just make sure you commit and upload any unsaved changes before doing this.


#### Dropping file content removes content from more than the specified file
I dropped the file content of one file and suddenly the content of multiple files got removed!

*Answer*
git annex references files only once. If a single file exists as multiple, identical copies in several places within the same repository, dropping the file content of one of these files will lead to dropped file content for all of these files.


#### A file upload has failed
A `gin upload` of files has failed with an unspecified message, e.g.

```bash
gin upload data_directory/*
:: Adding file changes
"data_directory/file_one.tif" failed
"data_directory/two.tif" failed
```

*Answer*
Run `gin sync` and check if this resolves the current upload issue. 
This will download changes from the remote repositories and then 
upload any local changes to the remotes.

If it does not help, run `gin --version` and check the current 
GIN client version number. If it is below 1.12, it might 
be helpful to upgrade to the latest version of the client and
run the upload again. You can also try to update the git binary on 
the local machine.

Further check the client logfile; it can be found at the 
following locations depending on the operating system:
- Windows: `C:\Users\<User>\AppData\Local\g-node\gin\gin.log`
- macOS: `/Users/<User>/Library/Caches/g-node/gin/gin.log`
- Linux: `/home/<User>/.cache/g-node/gin/gin.log`

Before checking the log, try to run the upload command again 
to make sure that the failure and any pertinent information 
is included as the last entry in the logfile.


#### Broken pipe upload issue
On uploading to GIN, we encounter the following error, what is the issue and how can it be resolved.

```bash
:: Uploading
Compressing OK
Connection to gin.g-node.org closed by remote host.
fatal: the remote end hung up unexpectedly
fatal: sha1 file '<stdout>' write error: Broken pipe
fatal: the remote end hung up unexpectedly
Pushing to origin failed.
git-annex: sync: 1 failed

[error] 1 operation failed
```

*Answer*
This error can occur when too many small files (each size < 10 MB) with a total sum size of > 4GiB have been committed with a single commit. Try splitting such a commit into multiple smaller ones so that the total sum size of committed files is below 4 GiB.  

The reason behind this issue is, that only files with size > 10MB are checked into git annex that handles large files well. Files with a smaller size are still checked into git, which does not handle many or large files nearly as well as git annex does. In the described case, git cannot handle the sum size of files any longer and will fail on upload.


#### Unspecified client error message [error] 1 operation failed
When trying to upload data to the GIN server, the GIN client prompts "[error] 1 operation failed". What went wrong and how do we fix it.

*Answer*
This error is displayed when a very unusual circumstance has happened. Usually there is no clear answer to this issue and needs further investigation.

- the error has been linked to trying to upload many small files (individual size < 10MB) with a total size of >4GiB that have been added in one single commit, which is something git does not handle well. If this is the case, please try splitting the commit into a couple of commits with fewer files in each commit and try uploading again.

- if this is not the case, please check the client logfile; the logfile contains more detailed information. Depending on the operating system the logfile can be found at:
  - Windows: `c:\users\{user}\appdata\local\g-node\gin\gin.log`
  - Linux: `/home/{user}/.cache/g-node/gin`
  - MacOS: `/Users/<User>/Library/Caches/g-node/gin/gin.log`

- if the log shows an error after `git annex metadata --json --key=MD5-<hash>` you can try to manually upload again using the command `gin annex copy --to=origin <filename>` with the file that caused the issue.


#### Disconnect reading sideband packet upload issue
I cannot clone a repository or upload from my machine to the GIN repository. I constantly get lots of error lines ending in:

```bash
# Example repository clone
gin get myusername/tmp
Downloading repository Repository download failed. Internal git command returned: Cloning into 'tmp'...
remote: Enumerating objects: 516, done.                                                         
remote: Counting objects: 100% (516/516), done.                                                 
remote: Compressing objects: 100% (224/224), done.                                              
client_loop: send disconnect: Broken pipeiB | 1006.00 KiB/s
fetch-pack: unexpected disconnect while reading sideband packet
fatal: early EOF
fatal: index-pack failed
 
[error] 1 operation failed
```

```bash
# Example repository upload
[stderr]
fatal: There is no merge to abort (MERGE_HEAD missing).
2022/04/21 20:16:13 The following error occured:
Connection to gin.g-node.org closed by remote host.
send-pack: unexpected disconnect while reading sideband packet
fatal: sha1 file '<stdout>' write error: Broken pipe
fatal: the remote end hung up unexpectedly
Connection to gin.g-node.org closed by remote host.send-pack: unexpected disconnect while reading sideband packetfatal: sha1 file '<stdout>' write error: Broken pipefatal: the remote end hung up unexpectedly  Pushing to origin failed.
git-annex: sync: 1 failed
2022/04/21 20:16:13 Exiting with ERROR message: 1 operation failed
```

*Answer*
This error can occur when the connection cannot handle a large upload. There is no easy option to deal with this issue from the machine the error occurs on.
- use a wired connection (LAN) if you suspect a WIFI connection can limit upload
- if this is an option, work from a machine where the upload is not an issue
- if the suggestions above are not an option, try to limit the amount of data you upload in one go. This also includes adding and uploading data in chunks:
  - create a clean repository or clone an existing repository from the gin server; at this point it is important to locally start with a repository that does not have a large amount of data waiting to be uploaded.
  - add only one smaller file to this repository, commit and upload; if the upload succeeds, you can be sure that the issue is the chunk size of the upload. Increase the size of uploaded chunks until you hit the amount of data where an upload ends with the error described above and stay below this limit when uploading data from you machine.

At the core of this issue lies a problem that `git` cannot prepare and provide data that is supposed to be uploaded in a reasonable timeframe; the server ready to receive the content has to wait too long and closes the connection.

Check the following threads from users experiencing this or a similar issue on a multitude of git services and potential solutions
- https://stackoverflow.com/questions/66366582/github-unexpected-disconnect-while-reading-sideband-packet
- https://stackoverflow.com/questions/21277806/fatal-early-eof-fatal-index-pack-failed/22317479#22317479
- https://github.com/git-lfs/git-lfs/issues/2428
- https://serverfault.com/questions/1056419/git-wsl2-ssh-unexpected-disconnect-while-reading-sideband-packet
- https://stackoverflow.com/questions/32137388/how-to-check-post-buffer-size-before-clone-git-repository
- https://forum.gitlab.com/t/issues-with-cloning-a-repo-from-windows-using-latest-git/59089
- https://stackoverflow.com/questions/6842687/the-remote-end-hung-up-unexpectedly-while-git-cloning


## Troubleshooting

#### I found a bug, something is not working, or "I don't know what to do"

You can ask questions, report problems or ask for general help by opening an issue [here](https://gin.g-node.org/G-Node/Info/issues).

#### Why do I see files with some strange text like "annex" or "WORM" instead of file content?

GIN is using git-annex to manage large files. Read more [here](wiki/GIN+Advantages+Structure). The fact that the content of these files is not shown, but instead a link to the location where it is supposed to be is shown, might mean either that
* the real content of these files has not been uploaded by the original authors or that
* the repo is a fork and the "real" file can be found in the "mother-repository" accessible below the repository name.
