
## required repositories

- would be a good idea to have
  - an organization
        deploy
  - teams
        core
        private
        public
  - at least 3 users (admin, write, read)
        deployadmin
        deploywrite
        deployread

- published doi repo (does not need to be within the deploy org)
- ready to publish doi repo (within the deploy org)
- annex data repo (within the deploy org)
- datalad repo (within the deploy org)

- public repo (within the deploy org)
- private repo (within the deploy org)
- unlisted repo (within the deploy org)

- repo with gin config file (within the deploy org)
  - different annex size

- supported file types
  - xml
  - json
  - yaml
  - odml
  - mp4 (in and outside of annex)
  - mp3 (in and outside of annex)
  - pdf (in and outside of annex)   
  - jpeg (in and outside of annex)
  - png (in and outside of annex)
  - tiff (in and outside of annex)
  - markdown

## what to check before an update

- user number
- repo number

## what to check after an update

### web functionality
- search

- registration (captcha) (firefox and chromium)
- user settings
- create organization
- create team
- add existing read, write and admin user to team
- create repo as org
- open issue
- fork repo to user
- update readme
- create Pull Request
- close PR
- close issue
- delete fork
- delete repo
- delete team
- delete organization
- delete account

### repo functionality
- login existing admin user

### client functionality

#### previous repos

- existing private repo
- existing public repo
- existing unlisted repo

- existing datalad repo

- DOI repo display
- DOI request

- filetypes display

- download of private repo + annex content
- download of public repo + annex content
- download of datalad repo + annex content

#### new repos

- create repo using org
- add read, write
- download repo as admin
- add git and annex data, upload
- download repo as write
- add git and annex data, upload
- download repo as read

## cleanup
- delete created repos
- delete created accounts
