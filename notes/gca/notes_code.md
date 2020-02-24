# Notes on dev and testing

## Image handling
Manual conversion probably best to use imagemagick to convert to jpg, 50% and then manually check all files. if a png did not properly get exported, open with gimp and manually save as jpg.

## Database

### Database updates

When updating the postgres database make sure that the service is restarted after the 
update it done, otherwise the play service might have a stale view on the database service.

### Database scripts in a docker container

When updating postgres in a docker container via a script use the following templates. When inserting rows where uuids are required, it might be necessary to activate the uuid creation function.

    sudo cp [dir]/[script].sql /web/gca[dir]/scripts/
    CONTAINERNAME=[addme]
    # to use and create uuids postgres needs the extension enabled
    sudo docker exec -it ${CONTAINERNAME} psql -Upostgres -dplay -c 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'
    sudo docker exec -it ${CONTAINERNAME} psql -Uplay -dplay -a -f /docker-entrypoint-initdb.d/[script].sql


## Scala debugging

Scala commandline debug: 
`Import play.api.Logger`
`Logger.debug("Message")`

How to debug log string in scala

    Logger.debug(s"Liking abstract with uuid: [$id]")


## Testing mobile images
When trying to test mobile images e.g. figures or banners:
- mobile figures are only fetched when published abstracts are viewed via the abstract list
- for local testing make sure we (a) know the uuid of a specific figure; (b) the corresponding figures in `./figures` and `./figures_mobile` have the same id but completely different content.
- use chromium; open dev panel, toggle the device toolbar (top left)


## Testing the offline app
Testing the offline app has to be done at least from a server
due to all the not allowed cross reference linking.

## Unit tests

### Running single tests

    # e.g.
    sbt "test-only service.BannerServiceTest"

## Templates

how templates are constructed on their way to the user

server
1) nest templates.
2) execute everything with an @.
3) deliver user.
4) executes <scritps> -> usually at their point of encounter which is usually 
   BEFORE any html tags & knockout bindings are encountered.
5) render HTML tags one after the other, run additional scripts if encountered.

Note: any javascript changes will be hot reloaded when using `sbt run`.

