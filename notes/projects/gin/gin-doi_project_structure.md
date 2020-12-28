# GIN-DOI project structure

- Transmission of DOI request forms from GIN to DOI is encryted, using the DOI key entry.
- The validation process requires the contents of https://gin.g-node.org/G-Node/Info/src/master/licenses to compare license texts

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
  - renderRequestPage()
    -> dataset.go:RegistrationRequest
    -> decryptRequestData()
    -> template.reqfail.go
    -> template.reqpage.go
    -> template.info.go
    -> dataset.go:readAndValidate()
  - decryptRequestData()
    -> G-Node/libgin.crypt.go:DecryptURLString
    -> G-Node/libgin.doi.go:DOIRequestData
  - startDOIRegistration()
    -> G-Node/libgin.RepositoryMetadata
    -> G-Node/libgin.DataCite
    -> decryptRequestData()
    -> mail.go:notifyAdmin()

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

-- dataset.go (main)
  - type RegistrationRequest
    -> G-Node/libgin.doi.go:DOIRequestData
    -> G-Node/libgin.doi.go:RepositoryMetadata
  - readFileAtURL()
  - readFileAtPath()
  - createLandingPage()
    -> util.go:prepareTemplates()
    -> templates.info.go
  - readAndValidate()
    -> readFileAtURL()
    -> readRepoYAML()
    -> messages.go:msgNoLicenseFile
    -> validation.go:checkLicenseMatch()
    -> messages.go:msgLicenseMismatch
    -> validation.go:validateDataCiteValues()
    -> messages.go:msgInvalidDOI
  - readRepoYAML()
    -> G-Node/libgin.doi.go:RepositoryYAML
    -> validation.go:checkMissingValues()

-- mail.go (main)
  - notifyAdmin()
    -> createIssue()
    -> util.go:GetGINURL()
    -> sendMail()
  - createIssue()
    -> getIssueID()
    -> gogs/go-gogs-client:CreateIssueOption
    -> G-Node/gin-cli:web.go:Post()
  - getIssueID()
    -> G-Node/gin-cli:web.go:Get()
    -> gogs/go-gogs-client:Issue
  - sendMail()

-- util.go (main)
  - tmplfuncs           ... name to function mapping for html templates
  - templateMap         ... name to template mapping for html templates
  - KeywordPath()
  - prepareTemplates()
    -> templates.common.go:Nav
    -> templates.common.go:Footer
  - GetGINURL()
    

-- validation.go (main)
  - checkMissingValues()
    -> messages.go:msgNoTitle
    -> messages.go:msgNoAuthors
    -> messages.go:msgInvalidAuthors
    -> messages.go:msgNoDescription
    -> messages.go:msgNoLicense
    -> messages.go:msgInvalidReference
  - validateDataCiteValues()
    -> allowedValues

-- workerdispatcher.go (main)
  - struct RegistrationJob
  - newDispatcher()

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
  - regfail.go (gdtmpl)
  - reqpage.go (gdtmpl)

- messages.go (main)

## main.go

Base entry point to the project. Current commandline options for the built project:

`gindoid start`                     ... runs `web.go:web`; starts the DOI server
`gindoid register [arg]`            ... runs `register.go:register`; not implemented
`gindoid make-html [arg]`           ... runs `genhtml.go:mkhtml`; creates html landing pages from xml file content
`gindoid make-keyword-pages [arg]`  ... runs `keywords.go:mkkeywords`; creates keyword pages from xml file content


## web.go

Entry point to the actual DOI server.

### web

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

### renderRequestPage

- parses received http request form content
  - Field regrequest
  - decrypt request content; required fields are username, repo, user email
  - display gdtmpl.RequestFailurePage (regfail.go)
  - TODO: the regfail page parses the Nav header part of the page, but does not display it in the template
          -> check if the page works
- checks the datacite.yaml content
  - dataset.go:readAndValidate()
  - display gdtmpl.RequestFailurePage (regfail.go) on failure
  - display gdtmpl.DOIInfo (info.go) and gdtmpl.RequestPage (reqpage.go) on success
  - TODO: the reqpage parses the Nav header part of the page, but does not display it in the template
          -> check if the page works
  - page is displayed with data from datacite.yaml rendered like the doi landing page
  - submit will transmit the original encrypted information to the "/submit" route of the DOI server


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


## dataset.go

### readAndValidate()
- read in datacite.yml from GIN repository
- extract information from datacite.yml
- checks contents of the datacite.yaml for missing entries and returns an error if required
- checks whether repo contains a LICENSE file; returns an error otherwise
- checks whether 
  a) the datacite.yml licence file name can be found in https://gin.g-node.org/G-Node/Info/src/master/licenses
  b) if yes, checks whether the content of LICENSE and the found license on GIN matches; returns an error otherwise
  c) if no, will continue without raising an issue
- checks if the following datacite keys contain only the allowed values and returns an error otherwise
    "reftype":      {"IsSupplementTo", "IsDescribedBy", "IsReferencedBy", "IsVariantFormOf"},
    "resourcetype": {"Dataset", "Software", "DataPaper", "Image", "Text"},


## mail.go
Handles mails and open issues

### notifyAdmin
- sends an email containing all DOI request information
  - all errors and warnings are collected in the actual job and sent with the email
- opens an issue on gin with the same information -> createIssue()

### createIssue
 -> getIssueID
 - if an issue exists, add a comment to it.
 - create an issue if no issue exists.
   -> gogs/go-gogs-client:CreateIssueOption
   -> G-Node/gin-cli:web.go:Post() ... Post to gin

### getIssueID
getIssueID returns the ID for an issue on a given repo that matches the given title. 
It returns 0 if no issue matching the title is found.
Uses the gin client to access the gin gogs api for the defined doi xml repository
and accesses the repositories issues list. Compares the titles to the title of the current
DOI request
- returns the issue ID if found, -1 or 0 otherwise.


## registration chain

GIN DOI -> request DOI
-> gin-doi/register -> renderRequestPage -> gin-doi/submit -> startDOIRegistration


