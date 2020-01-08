# Notes on dev and testing

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

## Testing mobile images

When trying to test mobile images e.g. figures or banners:
- mobile figures are only fetched when published abstracts are viewed via the abstract list
- for local testing make sure we (a) know the uuid of a specific figure; (b) the corresponding figures in `./figures` and `./figures_mobile` have the same id but completely different content.
- use chromium; open dev panel, toggle the device toolbar (top left)
