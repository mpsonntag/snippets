# git autodeployment via hooks

## Prepare a dedicated deployment user

The service requires a dedicated user that starts and runs the python flask server handling updates of all hosted git repositories. Since this results in a running continuous background process, it is best to set up a dedicated user for this task:

```bash
# check whether the user exists
getent passwd gitdeploy
# if not create user without setting up a home directory
useradd -M gitdeploy
# disable user login
usermod -L gitdeploy
# create a home directory that will contain the required code
mkdir /data/app
# change ownership to the gitdeploy user
chown -R gitdeploy:gitdeploy /data/app
# set this directory as home to the gitdeploy user
sudo usermod -d /data/app gitdeploy
```

