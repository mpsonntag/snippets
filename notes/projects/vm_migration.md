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

-[ ] maintenance encrypt setup
    -[ ] bc setup with maintenance test
    -[x] letsencrypt for maintenance
    -[ ] bc.dev service setup at maintenance
    -[ ] bc.dev letsencrypt
    -[ ] switch bc service to bc.dev domain
-[ ] bc, posters.bc setup
    -[ ] directory structure, required files
    -[ ] letsencrypt setup
    -[ ] bc service setup
    -[ ] posters.bc service setup

minor (13)
-[x] VM setup and IP assignment
-[x] basic setup
    -[x] apache
    -[x] docker
    -[x] docker-compose
    -[x] users and groups
    -[x] letsencrypt
    -[ ] letsencrypt/apache setup for search.gin
    -[ ] letsencrypt/apache setup for maintenance.srv13
-[ ] bc, posters.bc, static page setup
    -[x] static page directory structure
    -[x] static page resources move
    -[x] static page apache conf setup
    -[ ] directory structure, required files
    -[ ] data move to bc setup
    -[ ] letsencrypt/apache setup all files (maintenance, bc, bc.posters)
    -[ ] service setup using maintenance
    -[ ] bc full setup and preparation for 2022
    -[ ] letsencrypt/apache switch to services
    -[ ] letsencrypt switch to static page
-[ ] meta setup
    -[x] directory structure, required files
    -[x] prep all files apache conf files (meta, owl)
    -[x] service setup using search.gin letsencrypt for setup
    -[x] import RDF database
    -[x] owl.meta directory + static file setup
    -[ ] git directory python-odml setup
    -[ ] github hook setup
    -[ ] shut off meta VM and continue once done
    -[ ] letsencrypt/apache switch setup meta / owl.meta
    -[ ] setup backup database
-[x] abstracts setup
    -[x] directory structure, required files
    -[x] import banners and images
    -[x] letsencrypt/apache setup all files (maintenance, abstracts)
    -[x] service setup using maintenance
    -[x] import database
    -[ ] setup backup database, images
    -[ ] letsencrypt/apache switch setup
-[ ] odml setup
    -[ ] letsencrypt/apache setup all files (maintenance, odml, templates, terminologies)
    -[ ] git directory templates
    -[ ] git directory terminologies
    -[ ] github hook setup templates
    -[ ] github hook setup terminologies
    -[ ] letsencrypt/apache switch setup
-[ ] VM cleanup
    -[ ] cleanup backup folder on gate for meta and gca
    -[ ] bc VM shutdown; bc, posters.bc A rec to 13 by ITG, bc IP assign to 14 via A rec
    -[ ] letsencrypt bc, bc.posters; apache reload, check
    -[ ] meta VM shutdown; meta, owl.meta, upload.meta A rec to 13 by ITG
    -[ ] letsencrypt meta, own.meta, upload.meta; apache reload, check
    -[ ] abstracts VM shutdown, abstracts A rec to 13 by ITG
    -[ ] letsencrypt abstracts; apache reload, check
    -[ ] odml shutdown, odml, templates, terminologies A rec to 13 by ITG
    -[ ] letsencrypt odml, templates, terminologies; apache reload check
    -[ ] test https forward of odml
    -[ ] maintenance A rec for service setup (could use search.gin instead)
    -[ ] remove search.gin A rec

major (14)
-[ ] VM setup, IP assignment by ITG (from old bc), A rec entries srv14, maintenance.srv14
-[ ] basic setup
    -[ ] apache
    -[ ] docker
    -[ ] docker-compose
    -[ ] users and groups
    -[ ] letsencrypt
    -[ ] letsencrypt setup maintenance.srv14
-[ ] valid.gin setup
    -[ ] directory structure, required files
    -[ ] letsencrypt/apache setup all files (maintenance, valid.gin)
    -[ ] service setup using maintenance
    -[ ] letsencrypt/apache switch
-[ ] proc.gin setup
    -[ ] directory structure, required files
    -[ ] letsencrypt/apache setup all files (maintenance, proc.gin, proc-config.gin)
    -[ ] service setup using maintenance
    -[ ] letsencrypt/apache switch
-[ ] VM cleanup
    -[ ] valid service; valid.gin, proc.gin, proc-config.gin A rec to 14 by ITG
    -[ ] letsencrypt valid.gin, proc.gin, proc-config.gin; apache reload, check valid

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