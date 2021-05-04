# Bernstein conference poster gallery

## Notes


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
