
GCA-Web development notes

Not necessarily up to date.

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

docker build -t mpsonntag/gca-web:[tagname] .

## Local test builds:

GCAHOME=/home/msonntag/Chaos/dmp/gca-web
GCAIMAGE=favabs

GCAIMAGE=latest

### just the config
docker run -dit --rm --name gca_bee -v $GCAHOME/conf_dev/:/srv/gca/conf/ -p 9000:9000 mpsonntag/gca-web:$GCAIMAGE

### config and figures
docker run -dit --rm --name gca_bee -v $GCAHOME/conf_dev/:/srv/gca/conf/ -v $GCAHOME/figures/:/srv/gca/figures/ -v $GCAHOME/figures_mobile/:/srv/gca/figures_mobile/ -p 9000:9000 mpsonntag/gca-web:$GCAIMAGE

# config, figures and "latest" h2 database
docker run -dit --rm --name gca_bee -v $GCAHOME/conf_dev/:/srv/gca/conf/ -v $GCAHOME/figures/:/srv/gca/figures/ -v $GCAHOME/figures_mobile/:/srv/gca/figures_mobile/ -v $GCAHOME/db_h2_latest/:/srv/gca/db/ -p 9000:9000 mpsonntag/gca-web:$GCAIMAGE

# config, figures and "favabs" h2 database
docker run -dit --rm --name gca_bee -v $GCAHOME/conf_dev/:/srv/gca/conf/ -v $GCAHOME/figures/:/srv/gca/figures/ -v $GCAHOME/figures_mobile/:/srv/gca/figures_mobile/ -v $GCAHOME/db_h2_favabs/:/srv/gca/db/ -p 9000:9000 mpsonntag/gca-web:$GCAIMAGE



sudo docker run -d --name gcaweb -rm -v /data/gca/conf/:/srv/gca/conf/ -p 9000:9000 gnode/gca

sudo docker run -it -v /data/gca/conf/:/srv/gca/conf/ -p 9000:9000 gnode/gca

sudo docker run -d --name gca_bee -v /data/gca/conf/:/srv/gca/conf/ -p 9000:9000 gnode/gca

14:58 -> 15:14

sudo docker run -dit --rm --name gca_bee -v /data/gca/conf/:/srv/gca/conf/ -p 9000:9000 gnode/gca:working

sudo docker run -dit --rm --name gca_bee -p 9000:9000 mpsonntag/gca-web

sudo docker run -dit --rm --name gca_bee -v /data/gca/conf/:/srv/gca/conf/ -v /data/gca/figures/:/srv/gca/figures -v /data/gca/figures_mobile/:/srv/gca/figures_mobile/ -p 9000:9000 mpsonntag/gca-web

https://hub.docker.com/r/gnode/gca/
gnode/gca

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

# GCA-pgres db
GCAHOME=/home/msonntag/Chaos/dmp/gca-web
docker run -dit --rm --name pgres_gca_bee -v $GCAHOME/db_pgres_test/:/var/lib/postgresql/data -p 5432:5432 postgres:latest

## Restoring db dump and loading it into a running postgres docker container
-- create empty database directory on host system e.g.
    mkdir db_pgres_play

-- start postgres docker container pointing to the empty directory
    GCAHOME=/home/msonntag/Chaos/dmp/gca-web
    docker run -dit --rm --name pgres_gca_bee -v $GCAHOME/db_pgres_play/:/var/lib/postgresql/data -p 5432:5432 postgres:latest

NEXT STEP: figure out from "abstracts" journalcontrol how the backups are done and how the database is backed up, what the name of the database is and which user. 

Linklist
https://docs.docker.com/engine/examples/postgresql_service/#use-container-linking
https://rominirani.com/docker-tutorial-series-part-8-linking-containers-69a4e5bf50fb
https://stackoverflow.com/questions/24252598/how-to-setup-linkage-between-docker-containers-so-that-restarting-wont-break-it

https://hub.docker.com/_/postgres/
https://markheath.net/post/exploring-postgresql-with-docker
https://stackoverflow.com/questions/35679995/how-to-use-a-postgresql-container-with-existing-data
https://stackoverflow.com/questions/37834435/docker-compose-postgresql-import-dump
https://stackoverflow.com/questions/26598738/how-to-create-user-database-in-script-for-docker-postgres
https://github.com/docker-library/postgres/issues/193

https://www.playframework.com/documentation/2.6.x/ProductionConfiguration

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

GCA-Web - dev machine:

on dev, the required config files can be found in:

    /web/gca/conf

it should contain the file `application.dev.conf` with an appropriate base url e.g. `https://dev.g-node.org`

the required figures and figures_mobile directories can be found in:

    /web/gca/figures
    /web/gca/figures_mobile

`a` and `b` are dummy images that can replace the empty figures that are currently still being set up by the tests
and potentially break shit when testing. Use `a` for `figures` and `b` for `figures_mobile` to test the difference.

fetch the latest container

    sudo docker pull gnode/gca

MAKE SURE CONF IS UPDATED AND CONTAINS ALL REQUIRED ROUTES! YES ROUTES IS IN THE CONF FOLDER!

stop the running machine

    sudo docker stop gca_bee

startup with the latest container:

    sudo docker run -dit --rm --name gca_bee -v /web/gca/conf/:/srv/gca/conf/ -v /web/gca/figures/:/srv/gca/figures -v /web/gca/figures_mobile/:/srv/gca/figures_mobile/ -p 9000:9000 gnode/gca

cleanup any old containers:

    sudo docker images
    sudo docker ps -aq --no-trunc -f status=exited | xargs docker rm
    sudo docker images -f "dangling=true" -q | xargs docker rmi

check the current status of the instance:

    sudo docker logs -f gca_bee

once the instance is done and running, fix the abstract figures:

    sudo cp /web/gca/a /data/gca/figures/[insert figureID]
    sudo cp /web/gca/a /data/gca/mobile_figures/[insert figureID]

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

[{"ExtendedData":"","name":"Central Lecture Hall (ZHG)","description":"Main Conference and Workshops","point":{"lat":51.542262,"long":9.935886},"type":0,"zoomto":true,"floorplans":["https://www.uni-muenchen.de/studium/beratung/beratung_service/beratung_lmu/beratungsstelle-barrierefrei/bilderbaukasten/Barrierefreiheit/geschwister-scholl-platz-1-eg.jpg"]},{"ExtendedData":"","name":"Alte Mensa","description":"Public Lecture and Conference Dinner","point":{"lat":51.533442,"long":9.937631},"type":0,"zoomto":true},{"ExtendedData":"","name":"Alte Mensa","description":"Conference Dinner","point":{"lat":51.533442,"long":9.937631},"type":5,"zoomto":true},{"ExtendedData":"","name":"Göttingen Hbf","description":"main station","point":{"lat":51.536548,"long":9.926891},"type":4,"zoomto":true}]

[{"title":"Satellite Workshops","subtitle":"Goal of the Satellite Workshops is to provide a stage to discuss topical research questions, novel scientific approaches and challenges in Computational Neuroscience and related fields.","tracks":[{"title":"Sensory neurons: 'predictive coding' or 'coding for predictions'?","subtitle":null,"chair":["Matthew Chalk"],"events":[{"title":"Opening Remarks","subtitle":null,"start":"14:00","end":"14:20","location":"Marchstrasse 23","date":"2018-09-25","authors":[],"type":"workshop","abstract":null},{"title":"Learning to read out predictions of external stimuli from the retina","subtitle":null,"start":"14:20","end":"15:10","location":"Marchstrasse 23","date":"2018-09-25","authors":["Audrey Sederberg, Georgia Institute of Technology, Atlanta, USA"],"type":"workshop","abstract":"http://..."}]}]},{"title":"Postdoc meeting","subtitle":"","tracks":[{"title":"Postdoc meeting","subtitle":"","events":[{"title":"Postdoc Meeting","subtitle":null,"start":"19:00","end":"21:00","location":null,"date":"2018-09-25","authors":[],"type":null,"abstract":null}]}]}]

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

safari dirty fix
https://gist.github.com/kylebarrow/1042026

/assets/images/BC18Banner.jpg
/assets/images/BC18Thumb.jpg

https://portal.g-node.org/abstracts/bc18/BC18_header.jpg
https://portal.g-node.org/abstracts/bc14/BC14_icon.png

https://c1.staticflickr.com/1/421/32089433213_6ec7af402b_b.jpg

http://www.nncn.de/header/header-conference.jpg
http://www.nncn.de/bilder/bc14_kurzlogo

NOTE: for the apps: the cache is extremely persistent. to get a proper reload for e.g. 
on chrome to get schedule updates, one has to clear the complete browsing data and make
sure, that also the data saving is disabled since this seems to be an extra cache.

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

Issues GCA-Web:
- when submitting (?) an abstract, the last line of the successful submission message in the info box reads: 
'To register please go to: null'; where null is a link to some myabstracts page 
e.g.: http://localhost:9000/myabstracts/8a7573cf-5fbb-4871-ac90-0a9079e4e27b/null
This happens if a conference provides no link to the conference page / registration site.
