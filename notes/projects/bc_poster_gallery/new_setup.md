## New repositories and pipelines to handle and update the Bernstein Conference Poster Gallery

### Current resources

BC20            ... github.com:G-Node/BC20
                    ... retire and integrate into new BC-Gallery repository on GIN
BC20-uploader   ... github.com:G-Node/BC20-uploader
                    ... keep as is
BC20data        ... gin.g-node.org:G-Node/BC20data
                    ... retire and integrate into new BC-Gallery repository on GIN
gin             ... gin.g-node.org:G-Node/gin-bc20
                    ... retire and integrate into new BC-Gallery repository on GIN
gogs            ... github.com:G-Node/gogs ... webgallery
                    ... keep as is
GCA-Python      ... github.com:G-Node/GCA-Python
                    ... keep as is

### New resources

gogs            ... github.com:G-Node/gogs
BC20-uploader   ... github.com:G-Node/BC20-uploader
GCA-Python      ... github.com:G-Node/GCA-Python
BC-Gallery      ... gin.g-node.org:G-Node/BC-Gallery

BC-Gallery structure
|- README.md
|- setup-notes.md
|- .gitignore
|- scripts\
|- BC-latest\
|  |- server-resources
|  |  |- uploadersalt
|  |  |- docker-compose.yml
|  |  |- config\
|  |  |  |- gogs\
|  |  |  |  |- config\
|  |  |  |  |  - app.ini
|  |  |  |  |- public\
|  |  |  |  |  |- *.jpg/.png
|  |  |  |  |- templates\
|  |  |  |  |  |- latest-template-tree\*
|  |  |  |- uploader\
|  |  |  |  |- configuration
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
