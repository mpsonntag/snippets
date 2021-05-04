# Bernstein conference poster gallery

## Roadmap

- decide on domain
  - should be something generic for both poster gallery and uploader
  - currently bc20.g-node.org and bc20-posters.g-node.org
  - register these domains and switch this in the domains
- decide if previous conference posters should still be available
- on the current system we already have registered users
  - would need to prune these users or setup the server anew
  - only users that have registered should be able to sign up
- the page is running again
  - any design changes?
  - any changes in data structure?
    - invited talks, contributed talks, posters, workshops?
    - topics, posters, talks?
    - additional information?
    - same format with vimeo, hopin, etc?
    - poster categories?
    - new banners?

workflow on site

- bc-admins: send emails to posters - code for upload
- bc-posters: people upload poster+description - can be updated whenever

- bc-posters: conf-admins update email hash list
- conf-gogs: registration checks email hash from bc-posters
- bc-admins: google sheet with poster information, hopin, vimeo link
- bc-admins: google sheet with workshop info
- gnode: save google sheets to tsvs -> run BC20 makefile to create and upload to bc-gogs

- people register: 


- different logins:
  - gca-web
  - juelich scibo (video upload)
  - bc-posters (upload-code)
  - bc-online (checked via email hash from bc-posters)
  - hopin
  - forgot sthg?

## Notes
https://github.com/G-Node/BC20

3 submodules
- uploader
- gin instance templates


on gin
https://gin.g-node.org/G-Node/gin-bc20/src/master

this repo contains the configs and docker files as well as the BC branding

on github.com/gin ... bc20 branch -> this contains noe commit to support the whitelist email changes

  - could use gogs master branch since it now contains default whitelisting
  - but fetches hashes so we probably continue using the gogs/bc20 branch

on gin: the G-Node/bc20data
  ... contains the raw data that is used to create the markdown files that are used to displayed during the conference

https://github.com/G-Node/BC20

contains a makefile that does all the work


WORKFLOW:

spreadsheet from BCOS

makefile
- fetches data from online spreadsheet and writes data to tsv
- then tsv to json
- with the GCA client -> DL abstract to json

on machine bc20.g-node.org

directory /data
directory /gin-bc20 ... contains docker volumes and docker config files ... this is a copy of the files on gin.g-node.org/G-node/gin-bc20

msonntag ... admin
bc20

repos on bc20.g-node.org
- Invited Talks ... https://bc20.g-node.org/BernsteinConference2020/InvitedTalks/wiki ... rendered


locally clone these repositories, add the https://bc20.g-node.org/BernsteinConference2020/InvitedTalks.wiki as remote and push changes to both repos so that the wiki is always properly rendered


locally
- clone github: BC20
- fetch all subrepositories
- create `galleries` folder in the root of the repo
- git fetch all repositories from b20 e.g. 

scripts

tojson.py
mergeabstracts.py ... takes tsv json and abstracts json ... figures still hosted from GCA, just links to the figures are added 
  - adds vimeo, hopin links, 
mkgalleries.py ... for everything except workshops
  - index text came from BCOS
  - 1 markdown file for each poster - uses the previously created json files
  - also created the various index pages
  - WITHDRAWN ... 193 ... id of the withdrawn abstract
mkworkshopgallery ... bit different 


templates?


examples

git clone git@bc20.g-node.org:/BernsteinConference2020/Posters galleries/Posters
cd galleries/Posters
git remote add wiki git@bc20.g-node.org:/BernsteinConference2020/Posters.wiki
git fetch --all



templates

org/home.tmpl ... javascript redirect ... to avoid users seeing the repositories directly but getting redirected to the wiki pages instead


gin.g-node.org/g-node/bc20data ... startpage.md & landing-page.md are just infos from BCOS, not actively used anywhere

