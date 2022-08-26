# Bernstein Conference Poster Gallery set up notes and data archive

KEEP PRIVATE
- keep the repository private, but make sure no live passwords are used in the config files
- keep the files with passwords in the appropriate repository

This repository contains
- all the information to set up, populate and run the Berstein Conference Poster Gallery
- all the files and statistics from previous conferences

For handling the Bernstein Conference poster gallery, check the [gallery handling notes](./gallery-handling.md).

### Resources and repository structure

#### Additional resources

BC20-uploader   ... github.com:G-Node/BC20-uploader
GCA-Python      ... github.com:G-Node/GCA-Python
gogs            ... github.com:G-Node/gogs
BC-Gallery      ... gin.g-node.org:G-Node/BC-Gallery

#### Repository structure

root
|- README.md
|- gallery-handling.md
|- .gitignore
|- scripts\
|- BC-latest\
|  |- server-resources\
|  |  |- README.md
|  |  |- .env
|  |  |- uploadersalt
|  |  |- docker-compose.yml
|  |  |- config\
|  |  |  |- gogs\
|  |  |  |  |- conf\
|  |  |  |  |  - app.ini
|  |  |  |  |- public\
|  |  |  |  |  |- *.jpg/.png
|  |  |  |  |- templates\
|  |  |  |  |  |- latest-template-tree\*
|  |  |  |- postgres\
|  |  |  |  |- postgressecrets.env
|  |  |  |- uploader\
|  |  |  |  |- config
|  |- galleries\
|  |  |- Info.wiki\
|  |  |  |- Datenschutz.md
|  |  |  |- Home.md
|  |  |  |- 'Terms of Use.md'
|  |  |  |- about.md
|  |  |  |- contact.md
|  |  |  |- imprint.md
|  |  |- main\
|  |  |  |- main.md
|  |  |  |- img\
|  |  |  |  |- *.jpg
|  |  |  |- posters\
|  |  |  |  |- assets\
|  |  |  |  |  |- *.jpg|.png
|  |  |  |  |- banners\
|  |  |  |  |  |- *.jpg|.png
|- BC20\
|  |- docker-logs\
|  |- galleries\
|  |- notes\
|  |- rawdata\
|  |- server-resources\
|- BC21\
|  ... as above 
|- BC22\
|  ... as above 

## Addendum

### Previous resources

BC20            ... github.com:G-Node/BC20
                    ... integrate into new BC-Gallery repository on GIN and archive
BC20data        ... gin.g-node.org:G-Node/BC20data
                    ... integrate into new BC-Gallery repository on GIN and archive
gin             ... gin.g-node.org:G-Node/gin-bc20
                    ... integrate into new BC-Gallery repository on GIN and archive
BC20-uploader   ... github.com:G-Node/BC20-uploader
                    ... keep as is
GCA-Python      ... github.com:G-Node/GCA-Python
                    ... keep as is
gogs            ... github.com:G-Node/gogs ... webgallery
                    ... keep as is
