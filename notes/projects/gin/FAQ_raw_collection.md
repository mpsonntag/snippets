## GIN RAW FAQ collection

### "Download failed error" on gin client get-content

(Q) When trying to download a file using the gin commandline client with the gin command "gin get-content [filename]" from a GIN dataset, I always get the error message: "Downloading failed: authorisation failed or remote storage unavailable". I can unlock the file without problems. Could you help me to resolve and get the data?

(A) This message usually pops up, when a download is attempted without being logged into
the gin client or if the logged in user has local access to a repository, but their GIN
user does not have the appropriate permissions to access the content of the repository on 
the GIN server.
Use "gin login [username]" to log into the GIN client locally and check the permissions
of the user on the GIN server.
