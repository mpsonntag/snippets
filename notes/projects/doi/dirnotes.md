Set up the server for easy serving directory switch without having to touch the various configs
- to move serving dirs from one server to the other
- switch the serving directory when storage increases

Handling symlinked serving directories
- create choose a root dir e.g. `mkdir /serve-data`
- create the directory that will be the original serving dir that might be switched later on e.g. `mkdir /serve-data/data`
- create a symlink named `data-live` to the original serving dir `cd /serve-data && ln -s /serve-data/data data-live`
- update `/etc/apache2/apache2.conf` to enable access to `/serve-data/data-live`
- update all apache config files using this hosting directory at `/etc/apache2/sites-available`
- enable all sites and restart the apache `systemctl restart apache2.service`
- when using a docker based server deployment, update the hosting directories to the symlink as well.
- when switching the hosting directory, simply switch the symlink and all services should work without interruption.
