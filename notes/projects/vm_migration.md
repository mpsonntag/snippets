dev (12)
-[x] VM setup and IP assignment
-[x] basic setup
    -[x] apache
    -[x] docker
    -[x] docker-compose
    -[x] users and groups
    -[x] letsencrypt
-[x] gin.dev setup
    -[x] directory structure, required files
    -[x] letsencrypt setup
    -[x] service setup
    -[x] service user setup
    -[x] required service repo setup
    -[ ] upload / download test
    -[ ] haproxy setup and test
    -[ ] gindex setup and test
-[x] doi.dev setup
    -[x] directory structure, required files
    -[x] letsencrypt setup
    -[x] doi static host setup
    -[x] doireg service setup
    -[x] gin cli host setup
    -[ ] doi procedure test
-[x] meta.dev setup
    -[x] directory structure, required files
    -[x] letsencrypt setup
    -[x] service setup
    -[x] content upload
-[x] gca.dev setup
    -[x] directory structure, required files
    -[x] letsencrypt setup
    -[x] service setup
    -[x] database import
-[ ] gintest.dev setup
    -[ ] directory structure, required files
    -[x] letsencrypt setup
    -[ ] service setup
    -[ ] service user setup
    -[ ] required service repo setup
    -[ ] upload / download test
-[ ] doitest.dev setup
    -[ ] directory structure, required files
    -[x] letsencrypt doiregtest setup
    -[ ] doi static host setup -> re-use dev doi?
    -[ ] doiregtest service setup
    -[ ] gin cli host setup
    -[ ] doi procedure test
-[ ] valid.dev setup
    -[ ] directory structure, required files
    -[x] letsencrypt valid setup
    -[ ] valid service setup

minor (13)
-[x] VM setup and IP assignment
-[x] basic setup
    -[x] apache
    -[x] docker
    -[x] docker-compose
    -[x] users and groups
    -[x] letsencrypt
    -[x] letsencrypt/apache setup for maintenance.srv-13
-[ ] bc, posters.bc, static page setup
    -[x] static page directory structure
    -[x] static page resources move
    -[x] static page apache conf setup
    -[x] directory structure, required files
    -[x] data move to bc setup
    -[x] letsencrypt/apache setup all files (maintenance, bc, bc.posters)
    -[x] service setup using maintenance
    -[x] bc full setup and preparation for 2022
    -[ ] letsencrypt/apache switch to services
    -[x] update bc app.ini, restart service
    -[ ] test access
    -[x] letsencrypt switch to static page
    -[ ] add user to vault
-[ ] meta setup
    -[x] directory structure, required files
    -[x] prep all files apache conf files (meta, owl)
    -[x] service setup using search.gin letsencrypt for setup
    -[x] import RDF database
    -[x] owl.meta directory + static file setup
    -[ ] git directory python-odml setup
    -[ ] github hook setup
    -[ ] letsencrypt/apache switch setup meta / owl.meta
    -[ ] setup backup database
    -[ ] owl.meta uptime robot ping setup
-[x] abstracts setup
    -[x] directory structure, required files
    -[x] import banners and images
    -[x] letsencrypt/apache setup all files (maintenance, abstracts)
    -[x] service setup using maintenance
    -[x] import database
    -[ ] setup backup database, images
    -[ ] letsencrypt/apache switch setup
    -[ ] uptime robot ping setup and server switch
-[ ] odml setup
    -[x] letsencrypt/apache setup all files (maintenance, odml, templates, terminologies)
    -[x] git directory templates
    -[x] git directory terminologies
    -[ ] github hook setup templates
    -[ ] github hook setup terminologies
    -[ ] letsencrypt/apache switch setup
-[ ] VM cleanup
    -[ ] cleanup backup folder on gate for meta
    -[ ] cleanup backup folder on gate for abstracts
    -[x] bc, posters.bc A rec to 13 by ITG, bc IP assign to 14 via A rec
    -[x] meta, owl.meta, upload.meta A rec to 13 by ITG
    -[x] abstracts A rec to 13 by ITG
    -[x] odml, templates, terminologies A rec to 13 by ITG
    -[x] maintenance A rec for service setup
    -[x] meta VM shutdown
    -[ ] bc VM shutdown
    -[ ] abstracts VM shutdown
    -[ ] odml VM shutdown
    -[ ] letsencrypt bc, bc.posters; apache reload, check
    -[ ] letsencrypt meta, owl.meta, upload.meta; apache reload, check
    -[ ] letsencrypt abstracts; apache reload, check
    -[ ] letsencrypt odml, templates, terminologies; apache reload check
    -[x] test https forward of odml

major (14)
-[ ] VM setup, IP assignment by ITG (from old bc), A rec entries srv14, maintenance.srv14
-[x] basic setup
    -[x] apache
    -[x] docker
    -[x] docker-compose
    -[x] users and groups
    -[x] letsencrypt
    -[x] letsencrypt setup maintenance.srv-14
-[x] valid.gin setup
    -[x] directory structure, required files
    -[x] letsencrypt/apache setup all files (maintenance, valid.gin)
    -[x] service setup using maintenance
    -[x] letsencrypt/apache switch
-[x] proc.gin setup
    -[x] directory structure, required files
    -[ ] letsencrypt/apache setup all files (maintenance, proc.gin, proc-config.gin)
-[ ] VM cleanup
    -[x] valid service; valid.gin, proc.gin, proc-config.gin A rec to 14 by ITG
    -[x] letsencrypt valid.gin
    -[ ] proc.gin, proc-config.gin; apache reload, check valid

doi (11)
-[ ] VM setup, IP assignment by ITG (from old meta), A rec entries srv11, maintenance.srv11
-[ ] basic setup
    -[ ] apache
    -[ ] docker
    -[ ] docker-compose
    -[ ] users and groups
    -[ ] letsencrypt
    -[ ] letsencrypt setup maintenance.srv11
TODO add services list; add test, data link in and IP switch plan

gin (10)
-[ ] VM setup, IP assignment by ITG (from old odml), A rec entries srv10, maintenance.srv10
-[ ] basic setup
    -[ ] apache
    -[ ] docker
    -[ ] docker-compose
    -[ ] users and groups
    -[ ] letsencrypt
    -[ ] letsencrypt setup maintenance.srv10

TODO add services list; add test, data link in and IP switch plan

  maybe use different names for the test partitions to be sure e.g.
  /data/migrate/gin-repositories
  /data/migrate/gin-postgres
  /data/gindata/gin-repositories
  /data/gindata/gin-postgres

# Current DNS TTL

Check using `dig [DNS name]` or `dig any [DNS name]` to display the TTL for a DNS entry.
The times are noted in seconds and are counting down until the next cache refresh. When there is a difference between the normal dig and dig any, there might be an issue when switching the IP for a DNS entry and requesting an SSL certificate until the longer TTL period has expired.

                                                + any
abstracts.g-node.org      67xx      ~2h         84000     ~24h
owl.meta.g-node.org       67xx      ~2h         84000     ~24h
meta.g-node.org           67xx      ~2h         84000     ~24h
bc.g-node.org             67xx      ~2h         84000     ~24h
odml.g-node.org           3600      1h          same
templates.g-node.org      3600      1h          same
terminologies.g-node.org  3600      1h          same
valid.gin.g-node.org      36xx      ~1h         same
doi.gin.g-node.org        26xx      ~45min      same
gin.g-node.org            3600      1h          same

One could also flush the google DNS cache [here](https://developers.google.com/speed/public-dns/cache).
