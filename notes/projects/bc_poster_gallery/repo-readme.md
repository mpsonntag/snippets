# Bernstein Conference Poster Gallery set up notes and data archive

**KEEP PRIVATE**
- keep the repository private, but make sure no live passwords are used in the config files
- keep the files with passwords in the appropriate repository

This repository contains
- all information to set up the service
- all information to populate and run the Bernstein Conference Poster Gallery
- all files and statistics from previous conferences

For preparing the server to host the Bernstein Conference poster gallery, check the [gallery setup notes](./gallery-setup.md).
For handling the Bernstein Conference poster gallery content before and during a conference, check the [gallery handling notes](./gallery-handling.md).
For a timetable and a task checklist see the [gallery timetable notes](./gallery-timetable.md).


### Resources and repository structure

#### All poster gallery resources

```
BC20-uploader       ... github.com:G-Node/BC20-uploader
GCA-Python          ... github.com:G-Node/GCA-Python
gogs                ... github.com:G-Node/gogs
BCCN-Conference     ... gin.g-node.org:G-Node/BCCN_Conference
```

#### Repository structure

```
root
├── README.md
├── gallery-handling.md
├── .gitignore
├── scripts\
|   └── *.py
├── BC-latest\
|  ├── server-resources\
|  |  ├── README.md
|  |  ├── .env
|  |  ├── uploadersalt
|  |  ├── docker-compose.yml
|  |  ├── static\
|  |  |   ├── resources\
|  |  |   |   └── *.jpg/.png
|  |  |   └── index.html
|  |  └── config\
|  |     ├── gogs\
|  |     |  ├── conf\
|  |     |  |   └── app.ini
|  |     |  ├── public\
|  |     |  |   └── *.jpg/.png
|  |     |  └── templates\
|  |     |      └── latest-template-tree\*
|  |     ├── postgres\
|  |     |   └── postgressecrets.env
|  |     └── uploader\
|  |         └── config
|  └── galleries\
|     ├── Info.wiki\
|     |  ├── Datenschutz.md
|     |  ├── Home.md
|     |  ├── 'Terms of Use.md'
|     |  ├── about.md
|     |  ├── contact.md
|     |  └── imprint.md
|     ├── main\
|     |  ├── main.md
|     |  └── img\
|     |      └── *.jpg
|     └── posters\
|         ├── assets\
|         |   └── *.jpg|.png
|         └── banners\
|             └── *.jpg|.png
├── BC20\
|  ├── docker-logs\
|  ├── galleries\
|  ├── notes\
|  ├── rawdata\
|  └── server-resources\
├── BC21\
|   ... as above 
├── BC22\
|   ... as above 
...
```

## Addendum

### Previous resources

```
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
```
