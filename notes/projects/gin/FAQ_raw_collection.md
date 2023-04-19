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


### I cannot create a new account on GIN due to Captcha issues

(Q)
I am having trouble registering a new user account on https://gin.g-node.org.

Every time I click "Create New Account" on the sign up page an error appears
"Captcha didn't match".

(A)
The currently used Captcha has been known to cause issues with some browser 
versions. You can either try to use a different browser; the Chrome 
and Chromium Browsers have caused no issues at all in this respect. If you
do not want to switch browser, try updating to the latest version.


### Error pushing file content to GIN using DataLad

(Q) When trying to push files to GIN using the DataLad command line client,
the file content does not show up on the GIN server. What is going wrong?

(A)
Currently there is an incompatibility with the underlying git-annex version (>8)
that a default installation of Datalad is using with the current git annex version
on GIN.
We advise mainly using the GIN command line client for the time being. If you
currently need to use DataLad and still want to use it with the GIN server,
you have to make sure, that DataLad is using a git annex version of 8.

This issue will get resolved in the future, but for now please keep using 
the GIN command line client or git annex version 8.



### Upload error / corrupted repository issue when using datalad upload to gin

> A

We started using GIN to host big git annex repos with neuroimaging data using datalad, 
and for one of the repos, when pushing to GIN with datalad push, we keep on receiving 
the below error message. The repos are private and are submodules of other gin
repositories.

CommandError: 'git -c diff.ignoreSubmodules=none push --progress --porcelain gin master:master git-annex:git-annex'
failed with exitcode 128 under /data/proj_data/proj_data_4a/mriqc
Delta compression using up to 64 threads
CommandError: 'ssh -o ControlPath=/home/username/.cache/datalad/sockets/53dce49f ... 'git-receive-pack '"'"'/ginuser/proj_data_4a-mriqc.git'"'"''' failed with exitcode 255
send-pack: unexpected disconnect while reading sideband packet
fatal: the remote end hung up unexpectedly

> B

If this happens for one repo but not others, there may be a problem with the repo. 
Have you checked that the repo is ok? Can you push to other remotes?
Have you tried using the GIN client (https://gin.g-node.org/G-Node/Info/wiki/GIN+CLI+Setup) 
for upload instead of datalad?

> A

We set the default remote using gin use-remote, which
worked fine, but then when trying gin upload -- to gin
we got the following error about my git annex version

:: Uploading
git-annex: Repository /data/proj_data/proj_data_4a/mriqc is at unsupported version 10. Upgrade git-annex.
[error] 1 operation failed

We then did git annex upgrade in my local repo, but the problem persisted

> B

The repo is at the new git-annex version 10, which is not yet supported by GIN.

If you want to use GIN, you need to use git-annex
version 8, and the repository should have been created with that version.
Unfortunately, there is no workaround as far as we know.

Apologies for the inconvenience, and thanks for bringing this up.
It is useful to know how the version incompatibility presents with datalad.

> A

Interestingly, we have several other repos with the same git-annex version which we 
do manage to push to GIN with datalad commands without problems.

> B

Ok, then we need to look further into this. Still, the error you get might be related 
to the git-annex version. It might be useful to figure out what is different for this 
repo than for your other repos.

Eventually GIN will be upgraded to the new version, but it will take a while. It is not 
just the GIN client but also the GIN server that uses git-annex.

> A

It looks like the GIN server does not have problems with my git-annex version for most 
repos, whereas GIN CLI consistently does?!

This repo does not look different from the other ones I do manage to push using datalad 
push, so still puzzling?

> B

We will send you two repos (pushed datalad subdatasets) which are very similar in terms 
of content, but differ in terms of being able to push to them, for each of the errors we 
receive. This will probably be the best way of figuring out the problem, because we 
do not see any differences between them. We'll will send the respective error messages along too.

However, these repos are currently private, so we would prefer to add you as a 
collaborator for testing purposes rather than making them public at this point if that is ok?

> A

I wanted to point you to my revived Neurostars thread with Yarik at datalad re the issues 
below, and wonder about your thoughts?

https://neurostars.org/t/datalad-push-to-gin-errors/24051/18

> B

Having large binary files versioned in git instead of git-annex can lead to long 
processing times, which could cause timeouts and might be a reason for some repos 
having issues. I think it is good advice to put all large files in git-annex.

Have you tried removing and re-creating the repos that cause errors? Some of them are 
completely empty anyway.

Finally, I would not exclude that some of the problems might be caused by using git-annex 
version 10 on the client side while the GIN server is using git-annex version 8.

> A

Some of the repos are empty because pushing fails, they are not empty on my server, so 
recreating is not that simple, but I may try to do some cleanup to reduce the size of .git/objects.

Is there any plan to make GIN compatible with newer git annex versions? In that case, 
we could test the influence of this issue.

> B

You don't have to change your local repos, just remove and re-create the repos on GIN.
Eventually the GIN server will be updated to git-annex version 10, but this will take a while.

> A

I just wanted to inform whether there is any update on this, since I keep on experiencing 
this annoying problem, also with new repos, so I would like to sort it out!

> B

we ran some checks that reported the following repos to be corrupted:

proj_data_4a-derivatives.git
proj_data_4a-firstlevel.git proj_data_4a-mriqc.git
proj_data_4b-derivatives.git
proj_more_data-derivatives.git
proj_more_data-mriqc.git

Are these the repos that have the problem?
Have you tried removing and re-creating the repos?

> A

These are indeed exactly the repos in which I experience problems!

I just removed and recreated the proj_more_data-derivatives.git (which is a "subrepo" 
(i.e. datalad subdataset) of proj_more_data.git) - it should be empty now.

The proj_more_data repo are completely new and failing upon the first push attempt.

> B

the repo proj_more_data-derivatives.git seems ok now.

It is unclear what might be the cause. Somehow the state of the branches seems to get corrupted.
We ran the checks on a number of other datalad repos but haven't seen this error anywhere else.

> A

Datalad push --to gin requires me to enter my passphrase a couple of times, with a 
"connection closed" message in between (see below).

Pushing has now started, but such messages early on have been a reliable predictor of 
trouble in the past, so not very high hopes it will work with the newly created repo - 
does the error give you any clue?

Enter passphrase for key '/home/username/.ssh/id_key':  | 1.00/4.00 [00:00<00:00, 8.39k Steps/s]
Connection closed by gin.g-node.org port 22
Enter passphrase for key '/home/username/.ssh/id_key': █████████████████████████████████████| 2.00/4.00 [00:00<00:00, 4.41k Steps/s]
Enter passphrase for key '/home/username/.ssh/id_key':

> B

The checks report the repo to be corrupted again, but now it uses 12GB of storage. 
Is this the amount of data that should have been pushed?

> A

It is pushing as we speak, but gets interrupted, and prompts for passphrase in between.

Hence, it looks like things get corrupted very early on during the pushing process?

> B

How about pushing a single file first and see whether that gets you to a valid state of the repo?

> A

Even trying to push one simple small .json file triggers the problem now, illustrating 
that it happens at the end of compression, not when copying - see below.

The compression resumes but becomes extremely slow or even stalls completely after this error.

I bet the recreated repo is corrupted again?

user@machine:/data/proj_more_data/derivatives$ datalad push --to gin fmriprep/dataset_description.json
Enter passphrase for key '/home/username/.ssh/id_key':  | 1.00/4.00 [00:00<00:00, 8.39k Steps/s]
Update availability for 'gin':  75%|██████████████▊| 3.00/4.00 [00:00<00:00, 6.60k Steps/sConnection to gin.g-node.org 
closed by remote host.██████████████▊▎| 16.0k/16.1k [00:57<01:34, 1.43s/ Objects]

> B

At least we know it's not related to the amount or number of files.

- Was this an annexed file?
- Have you ever experienced such behavior with a repo that wasn't a submodule?

> A

Not an annexed file, no, can also try with an annexed one

Never experienced with a non-submodule repo, as virtually all of
them are subdatasets/submodules of a superdataset in our file
organisation

Please note that these are private repos atm too

> B

So it seems unrelated to git-annex.

Maybe something goes wrong when pushing a submodule from the root repo. Could even be a datalad issue.

> A

It does not seem to be that simple, I now recreated the repo afresh and tried to push 
a single annexed file first thing, and the same error occurs (see error message below).

> B

> It has nothing to do with annex, more likely with submodules or the network connection.

Also, I did not push the submodule from the root repo, but the subdataset/submodule 
itself (hence not datalad push -r from root, but without -r from subrepo).

> The datalad folks say it is not a datalad issue...

Based on which evidence?

> Any other suggestions?

Can you try this from a computer outside your university network?

> A

Not sure based on what the datalad folks say this, can double-check, and I am in touch 
with our IT folks too.

I need to be on my university network to connect to the server, either on campus or 
via VPN, hence difficult to try from outside?

> B

It is interesting to see that some repos, even though all are submodules, seem to be 
more susceptible to the problem (-derivatives, -mriqc) - could it have to do with number 
or type of files stored in git (rather than git annex)? .html files for example?

It certainly could have to do with the number of files. The "connection closed" error 
could be resulting from a timeout because git takes too long.
Do these repos have many more files that those that are not affected?

> A

Seems like I have found the solution to the problem, which must be
related to some issues with the git repo, as the following simple
solution has worked for several repos now

    cd /data/proj_data_4a/mriqc
    git gc   #garbage collection and cleanup
    datalad siblings -s gin remove
    datalad create-sibling-gin ginuser/proj_data_4a-mriqc -s gin —private   #create fresh remote repo
    datalad push --to gin

> B

The repos seem ok now. Great that you found the solution!
We'll add this to the GIN FAQs.
