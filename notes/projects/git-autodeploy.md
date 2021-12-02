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
# make the experience more joyful
sudo usermod --shell /bin/bash gitdeploy
# create a home directory that will contain the required code
mkdir /data/app
# change ownership to the gitdeploy user
chown -R gitdeploy:gitdeploy /data/app
# set this directory as home to the gitdeploy user
sudo usermod -d /data/app gitdeploy
```

## Preparing hosting directories

  - on the hosting server create the directory that will contain the hosted repositories

        mkdir -vp /data/web/autodeploy

  - make sure all hosted git repositories are public
  - clone all required repositories using https clone to `/data/web/autodeploy`. 

        git clone https://github.com/G-Node/odml-templates
        git clone https://github.com/G-Node/odml-terminologies
        git clone https://github.com/G-Node/python-odml

  - change ownership of all hosted repositories to the `gitdeploy` user
    
        chown -R gitdeploy:gitdeploy /data/web/autodeploy

## Setting up the auto-deployment on a new server

- The following section can be out of date; check [the flask wsgi](https://flask.palletsprojects.com/en/2.0.x/deploying/mod_wsgi/) documentation for details.

- make sure Apache is set up to work with WSGI (Web server gateway interface applications) and check if `wsgi` is available and enabled.
- otherwise install it via `apt-get install libapache2-mod-wsgi-py3`, enable it and restart Apache.

- install flask using the `gitdeploy` user

      sudo su - gitdeploy
      pip install --user flask

- clone the github-hook-handler from github into `/data/app`

      git clone https://github.com/G-Node/github-hook-handler

- create a uuid as "payload-secret" for the deployment
- in `/data/app` create a file `cloner.wsgi` and paste the following code:

      import sys
      sys.path.insert(0, '/data/app/github-hook-handler/')

      from handlers import cloner

      hosted_repos = ["odml-templates", "odml-terminologies", "python-odml"]
      listener = cloner.create_app('/data/web/autodeploy/', 'payload-secret', hosted_repos)
      application = listener.app

- if required, `chown` the github-hook-handler repository and the `cloner.wsgi` file to the "gitdeploy" user / "gitdeploy" group.

- add an apache site configuration `git-handler.conf` with the following content and enable it

        Listen 5000
        <VirtualHost dev.g-node.org:5000>
            ServerName dev.g-node.org
            ServerAdmin dev@g-node.org

            DocumentRoot /data/app

            WSGIDaemonProcess dev.g-node.org user=gitdeploy group=gitdeploy threads=5 home=/data/app
            WSGIProcessGroup dev.g-node.org

            WSGIScriptAlias /cloner /data/app/cloner.wsgi
            <Directory /data/app>
                Require all granted
            </Directory>
        </VirtualHost>

- do the following github setup for both templates and terminologies:
  - create a new webhook in "settings/webhooks"
  - use the following URL as Payload URL: `http://dev.g-node.org:5000/cloner/`
  - select content type `application/json`
  - add the "payload-secret" created above
  - trigger just a push event
  - set as `active`

- on the webserver add the apache site configurations for templates and terminologies, enable them and restart apache

- everything should be set up to automatically update both templates and terminologies upon changes on the github repositories.

- check the apache log when a push is happening to ensure that the hook is working properly.
