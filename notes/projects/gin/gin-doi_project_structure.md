# GIN-DOI project structure

## Project hierarchy

main.go (main)
- web.go (main)
  - struct reqResultData
  - web()
    -> config.go:loadconfig()
    -> G-Node/gin-cli.gin.go:Login()
    -> workerdispatcher.go:newDispatcher()
    -> workerdispatcher.go:newWorker()
    -> workerdispatcher.go:Dispatcher.run()
    -> web.go:renderRequestPage()
    -> web.go:startDOIRegistration()
    -> assetserver.go:newAssetsFS()

- register.go (main)

- genhtml.go (main)
  - const defginurl                     ... "https://gin.g-node.org"
  - const defdoibase                    ... "10.12751/g-node."
  - const defstoreurl                   ... "https://doid.gin.g-node.org"
  - isURL()
  - readFileAtPath()
  - mkhtml()                            ... entry point
    ->dataset.go:createLandingPage()
  - fetchAndParse()                     ... not used within the gindoi project

- keywords.go (main)
  -> G-Node/libgin.RepositoryMetadata
  -> G-Node/libgin.DataCite
  - mkkeywords()        ... entry point
    -> dataset.go:readFileAtURL()
    -> dataset.go:readFileAtPath()
    -> util.go:KeywordPath()
    -> util.go:prepareTemplates()

-- config.go (main)
  -> G-Node/libgin.util.go:ReadConf()
  -> G-Node/libgin.util.go:ReadConfDefault()
  - loadconfig()
    -> G-Node/gin-cli.config.config.go:ParseWebString()
    -> G-Node/gin-cli.config.config.go:ParseGitString()
    -> G-Node/gin-cli.git.keygen.go:GetHostKey()
    -> G-Node/gin-cli.config.config.go:AddServerConf()
    -> G-Node/gin-cli.git.keygen.go:WriteKnownHosts()
    -> G-Node/gin-cli.gin.go:New()

-- workerdipatcher.go (main)
  - struct RegistrationJob
  - newDispatcher()

-- dataset.go (main)
  - readFileAtURL()
  - readFileAtPath()
  - createLandingPage()
    -> util.go:prepareTemplates()
    -> templates.info.go

-- util.go (main)
  - tmplfuncs           ... name to function mapping for html templates
  - templateMap         ... name to template mapping for html templates
  - KeywordPath()
  - prepareTemplates()
    -> templates.common.go:Nav
    -> templates.common.go:Footer

-- assetsserver.go (main)
  - struct AssetFS
  - newAssetFS()
  - AssetFS.Open()

- templates
  - common.go (gdtmpl)
    - Nav               ... navigation bar
    - Footer            ... footer
  - info.go (gdtmpl)
    - DOIInfo           ... DOI landing page wrapper used in various locations

## main.go

Base entry point to the project. Current commandline options for the built project:

`gindoid start`                     ... runs `web.go:web`; starts the DOI server
`gindoid register [arg]`            ... runs `register.go:register`; not implemented
`gindoid make-html [arg]`           ... runs `genhtml.go:mkhtml`; creates html landing pages from xml file content
`gindoid make-keyword-pages [arg]`  ... runs `keywords.go:mkkeywords`; creates keyword pages from xml file content


## web.go

Entry point to the actual DOI server.

## web

- loads server config
  - requires libgin and all values set as environmental variables
  - sets maximum request queue
  - set maximum number of concurrent workers

  - sets up gin doi to gain access to gin via gin-cli
    - handshakes with gin server and fetches gin hostkey
    - creates an gin-cli client and logs in to the gin server with the doi user
  - creates a job dispatcher with max number of workers and max number of jobs
    - start the job dispatcher
    - create workers to the maximum number of jobs
    - worker idle until jobs come in
  - create available server routes
    "/"             ... serve storage at `config.Storage.StoreURL` (DOI root)
    "/register"     ... web.go:renderRequestPage()
    "/submit"       ... web.go:startDOIRegistration()
    "/assets/"      ... serves assets files from the local file system
  - keep server alive for incoming traffic


## genhtml.go

Creates index.html pages for registered DOIs from provided doi.xml files.

### mkhtml
- cycles through all provided arguments (doi.xml files or urls pointing to doi.xml files).
  - prepares Source and ForkRepository URLs
  - creates a directory for each DOI and creates an `index.html` landing page in it

### fetchAndParse
- this function is not used within the gindoi project
- no usage in libgin nor in gogs
- could be removed or moved to libgin if used from another project

- fetches a DataCite yaml file from a gin repository and returns the read information.


## keywords.go

Creates index.html pages for keywords found in provided doi.xml files.

### mkkeywords
- cycles through all provided arguments (doi.xml files or urls pointing to doi.xml files).
  - checks if they are doi.xml files or urls to fetch doi.xml files from and unmarshals them to a `libgin.DataCite` struct
  - walks through all keywords for this file; updates the global keyword-dataset mapping with the current keywords and adds the current dataset to all occurring keywords.
- cycle through keyword map and create landing pages for each keyword
  - creates a directory and and `index.html` file for every keyword
- creates a keywords `index.html` file listing all keywords sorted by a) # of linked datasets and b) lexical order
