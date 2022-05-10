# in-house-gin

This repository documents how to set up a custom instance of the [GIN](https://gin.g-node.org) G-Node infrastructure 
service.

## Setup prerequisites and preparations

The setup has been tried and tested on Linux based Operating systems.

`docker` and `docker-compose` are required.

To smoothly work with a docker deployment, the following groups and users should be set up.

### System preparations
- prepare dedicated deployment group e.g. "ginservice" group if it does not exist
- create a dedicated deployment user e.g. "ginuser"
- note deployment group and user IDs for the `docker-compose.yml` file.
- for any further setup, all required directories and files should be created with this user/group as owners.
- make sure to add all users that are running docker-compose or need access to project files to the docker and deploy groups.

# gin core repository handling

Properly handle the G-Node/Info.wiki

- add a git ssh key on the GIN server
- on gin.g-node.org fork the G-Node/Wiki repository which is itself a fork of the G-Node/Info.wiki
- handle everything via git and not via the gin client to avoid images or larger files to be added to the annex.

```
# clone the user fork of the G-Node/Wiki repo
git clone git@gin.g-node.org:/[user]/Wiki.git
cd Wiki
# add upstream repo for pull requests
git remote add upstream git@gin.g-node.org:/G-Node/Wiki.git
# add the actual GIN wiki remote
git remote add livewiki git@gin.g-node.org:/G-Node/Info.wiki.git
git fetch --all
# make sure any changes from upstream (G-Node/Wiki) are in the origin ([user]/Wiki) repository
git checkout master
git rebase upstream/master
git push origin/master
```

- check via `git log` that `upstream/master`, `origin/master` and `livewiki/master` are all at the same, latest commit
- if this is not the case, origin/master has to be brought to a state where changes can be pushed to `livewiki/master` without causing issues.
- edit and commit files, push to the origin repo ([user]/Wiki)
- create a Pull request from [user]/Wiki to G-Node/Wiki to review and document the changes
- merge the pull request; rebase all remotes locally and push the changes to `origin` and the actual, live GIN Info wiki `livewiki`.

```
git fetch --all
git checkout master
git rebase upstream/master
# push the upstream merge to the [user]/Wiki
git push origin/master
# push the latest changes to the GIN Info wiki pages
git push livewiki/master
```

## GIN plain docker setup

... add this information to the GIN Info wiki: in-house

- add an ssh public key on the running GIN server
- clone repositories when testing on localhost using

  ```
  ssh://git@localhost:2222/[ginuser]/[ginrepository].git
  ```
