## FAQ
- [How can I get a DOI for my data?](#how-can-i-get-a-doi-for-my-data)
- [How can I access the data?](#how-can-i-access-the-data)
- [Is there a list of all GIN client commands?](#is-there-a-list-of-all-gin-client-commands)
- [Can I invite other collaborators who are not registered with GIN?](#can-i-invite-other-collaborators-who-are-not-registered-with-gin)
- [Can I share a repository with a collaborator or journal using a private link or access token?](#can-i-share-a-repository-with-a-collaborator-or-journal-using-a-private-link-or-access-token)
- [Do I have to use git-annex?](#do-i-have-to-use-git-annex)
- [Can I use GIN as a data provider for my research consortium/institute/department/working group with many collaborators and potentially a lot of terabytes of data?](#can-i-use-gin-as-a-data-provider-for-my-research-consortiuminstitutedepartmentworking-group-with-many-collaborators-and-potentially-a-lot-of-terabytes-of-data)

## Troubleshooting
- [I found a bug, something is not working, or "I don't know what to do"](#i-found-a-bug-something-is-not-working-or-i-dont-know-what-to-do)
- [Why do I see files with some strange text like "annex" or "WORM" instead of file content?](#why-do-i-see-files-with-some-strange-text-like-annex-or-worm-instead-of-file-content)

---

#### How can I get a DOI for my data?
See details [here](wiki/DOIfile).
##### Short overview:
* [Create a repository] (https://gin.g-node.org/G-Node/Info/wiki/Web+Interface#creating-a-repository)
* Upload data (using the [Website](https://gin.g-node.org/G-Node/Info/wiki/Web+Interface#uploading-files), our client, or git{annex})
* Create a [DOI request](wiki/DOIfile#structuring-the-doi-request-file) file (`datacite.yml`)
* Set repository to [public] (https://gin.g-node.org/G-Node/Info/wiki/Web+Interface#repository-settings)
* Hit doi button

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

#### GIN CLI says "nothing to do" but there are files missing on the server

Sometimes due to a misconfiguration or a network issue, git-annex might fail to contact the GIN server, while git commands still work. This can make the application incorrectly assume that the GIN server does not support git-annex and disable annex support for it. If this is the case, then the configuration file for the repository, which can be found at `.git/config` inside the local repository directory, will have a line that reads `annex-ignore=true`.

Git annex support can be re-enabled for the remote by removing the line. Alternatively, the following command, when run from inside the repository, will also toggle the setting to its correct value:
```
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

#### Using the GIN CLI behind a proxy

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

#### I found a bug, something is not working, or "I don't know what to do"

You can ask questions, report problems or ask for general help by opening an issue [here](https://gin.g-node.org/G-Node/Info/issues).

#### Why do I see files with some strange text like "annex" or "WORM" instead of file content?

GIN is using git-annex to manage large files. Read more [here](wiki/GIN+Advantages+Structure). The fact that the content of these files is not shown, but instead a link to the location where it is supposed to be is shown, might mean either that
* the real content of these files has not been uploaded by the original authors or that
* the repo is a fork and the "real" file can be found in the "mother-repository" accessible below the repository name.
