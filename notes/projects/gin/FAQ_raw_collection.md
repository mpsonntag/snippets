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
