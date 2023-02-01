## GIN RAW FAQ collection

### "Download failed error" on gin client get-content

(Q) When trying to download a file using the gin commandline client with the gin command "gin get-content [filename]" from a GIN dataset, I always get the error message: "Downloading failed: authorisation failed or remote storage unavailable". I can unlock the file without problems. Could you help me to resolve and get the data?

(A) This message usually pops up, when a download is attempted without being logged into
the gin client or if the logged in user has local access to a repository, but their GIN
user does not have the appropriate permissions to access the content of the repository on 
the GIN server.
Use "gin login [username]" to log into the GIN client locally and check the permissions
of the user on the GIN server.

### Cannot use GIN repository deploy keys; "GIN: Key Error"

(Q)
The GIN repository options provide a "Deploy key" ssh feature
we would like to use. The concerned project contains an exclusively 
generated ssh key as deploy key. The workflow set up on the reading 
side has the key added to the ssh-agent and can apparently connect. 
GIN however returns a "key error" and cuts the connection. How can
the deploy keys be properly used?

(A)
Unfortunately the GIN repository deploy keys are currently 
unavailable; they might be available in a future update of
the GIN services. If this is a high priority feature for
you, you can leave a +1 feature message on the issue tracker
and keep an eye on the progress of the feature:

https://github.com/G-Node/gogs/issues/85

As a current work-around you can create a dedicated GIN
user account with the ssh deploy key you want to use.


### We moved our data and want to remove all our repositories, can you help

We have moved our data to another location and would like to request your assistance in 
removing the current GIN repositories. Unfortunately, we have been unable to find a way 
to batch-remove GIN repositories through the web interface or cli.
Is it possible on your side to help us remove all the repositories in question?

If you don't need the organization, we can remove it with the repos for you.  To do this, 
please add the user "curator" to the Owners of the organization and afterwards remove 
yourselves from the Owners. This will dissociate your accounts from the organization and 
we will be able to remove it safely.

