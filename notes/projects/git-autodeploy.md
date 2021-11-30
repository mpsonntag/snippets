# git autodeployment via hooks

## Preparing a dedicated deployment user

The service requires a dedicated user that starts and runs a Python Flask server handling updates of all hosted git repositories. Since this results in a running continuous background process, it is best to set up a dedicated user for this task.

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

## Preparing hosting directories

  - on the hosting server create the directory that should contain the hosted repositories

        mkdir -vp /data/web/autodeploy

  - make sure all hosted git repositories are public
  - clone all required repositories using https clone to `/data/web/autodeploy`. 

        git clone https://github.com/G-Node/odml-templates
        git clone https://github.com/G-Node/odml-terminologies
        git clone https://github.com/G-Node/python-odml

  - change ownership of all hosted repositories to the `gitdeploy` user
    
        chown -R gitdeploy:gitdeploy /data/web/autodeploy
