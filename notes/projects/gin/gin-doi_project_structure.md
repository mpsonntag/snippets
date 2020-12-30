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
    -> G-Node/libgin.doi.go:RepositoryMetadata
    -> G-Node/libgin.datacite.go:DataCite
    -> G-Node/libgin.doi.go:GINUser
    -> decryptRequestData()
    -> mail.go:notifyAdmin()
    -> G-Node/libgin.doi.go:IsRegisteredDOI()
    -> util.go:randAlnum()
    -> G-Node/gin-cli.gin.go:RequestAccount()
    -> G-Node/libgin.datacite.go:NewDataCiteFromYAML()
    -> mail.go:notifyUser()

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
  - createRegisteredDataset()
    -> prepDir()
    -> cloneAndZip()
    -> G-Node/libgin.datacite.go:AddURLs()
      -> G-Node/libgin.util.go:GetArchiveSize()
    -> getPreviousDOI()
    -> createLandingPage()
    -> mail.go:notifyAdmin()
    -> validation.go:collectWarnings()
  - prepDir()
  - cloneAndZip()
    -> cloneRepo()
    -> derepoCloneDir()
    -> zip()
  - cloneRepo()
    -> G-Node/gin-cli.ginclient.repos.go:CloneRepo()
    -> G-Node/gin-cli.ginclient.repos.go:GetContent()
  - derepoCloneDir()
  - zip()
    -> G-Node/libgin.archive.go:MakeZip
  - getRepoForks()
    -> getLatestDOITag()
  - getLatestDOITag()
    -> G-Node/gin-cli:web.go:Get()

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
  - AwardNumber()
    -> templates.info.go
  - AuthorBlock()
    -> templates.info.go
  - FormatCitation()
    -> templates.page.go (DOI Landingpage)
  - FormatReferences()
    -> templates.info.go
  - FormatIssuedDate()
    -> templates.keyword.go
    -> templates.info.go
  - KeywordPath()
    -> templates.keyword.go
    -> templates.info.go
  - FormatAuthorList()
    -> templates.keyword.go
  - NewVersionLink()
    -> templates.info.go
  - OldVersionLink()
    -> templates.info.go

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
  - collectWarnings()
    -> dataset.go:getRepoForks()

-- workerdispatcher.go (main)
  - struct RegistrationJob
  - newDispatcher()
  - Worker.start()
    - dataset.go:createRegisteredDataset()
  - worker.stop()

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

### startDOIRegistration
- parses and decrypts form data again
  - returns request failed on decrypt error
  - send email containing all information and create an issue on gin.g-node.org/G-Node/DOImetadata in any case & render result regardless if any further error occurs -> nail.go:notifyAdmin();
  - mail and issue will only be sent when this function exits though; if it hangs, no email, no issue.
  - create a new random doi and check via https://doi.org whether the created doi is registered or not.
    - requires libgin.IsRegisteredDOI()
  - check whether the account requesting the DOI actually exists
    - requires gin-cli.RequestAccount()
  - runs dataset.go:readAndValidate() again
  - create DataCite struct
    - requires libgin.datacite.go:NewDataCiteFromYAML()
  - job is added to server `jobQueue`
  - send email to user; mail.go:notifyUser()


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

### createRegisteredDataset
- prepare the landing directory in the DOI serve directory
  -> prepDir()
- clone the repository, unannex and create a zipfile with the contents
  -> cloneAndZip()
- handle 3 reference repo URLs (DOI origin, DOI fork, DOI zip)
  -> G-Node/libgin.datacite.go:AddURLs()
    -> G-Node/libgin.util.go:GetArchiveSize()
- check if there is a previous version
  -> getPreviousDOI()
- create the landing page in the target directory
  -> createLandingPage()
- create the doi.xml file in the target directory
  - on error call `notifyAdmin`, create issue and send email
- write DataCite content to doi.xml file
  -> validation.go:collectWarnings()
  - if there are any errors or warnings, `notifyAdmin` to create issue and send email

### prepDir
- create the target directory
- create the `.htaccess` file in it

### cloneAndZip
- create folder TargetDirectory/jobname
- clone the repository; cloned directory name will be lower case
  -> cloneRepo()
- uninit repository
  -> derepoCloneDir()
- create zip file
  -> zip()

### cloneRepo
- switch to target directory
- clone the repository and get annex content
  -> G-Node/gin-cli.ginclient.repos.go:CloneRepo()
  -> G-Node/gin-cli.ginclient.repos.go:GetContent()

### derepoCloneDir
- switches to target dir
- runs git annex uninit
- sets file and dir permissions in .git dir able for deletion
- removes .git dir

### zip
- check paths for zip file
- create empty zip file
- switch to cloning dir
- zip content of cloning dir
  -> G-Node/libgin.archive.go:MakeZip

### getPreviousDOI
NOT FUNCTIONAL UNTIL AUTOMATIC FORKING TO THE DOI USER IS IMPLEMENTED (I think)
- fetches all forks of the current repo
  -> getRepoForks()

### getRepoForks
- fetch forks of the current repo from gin as gogs.Repository list
  -> G-Node/gi-cli.web.go:Get()
- check if a user DOI has forked the repo and a tag exists
  -> getLatestDOITag()

### getLatestDOITag
NOT FUNCTIONAL UNTIL AUTOMATIC FORKING TO THE DOI USER IS IMPLEMENTED
- fetch releases of the forked repository
- walk through existing releases and return the latest


## validation

### collectWarnings
- Funder has no ID
- Reference uses "Name" instead of "Citation" (legacy issue)
- Abstract is shorter than 80 char
- check for existing forks of the current repository by the DOI user
  -> dataset.go:getRepoForks()


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


## TODO list

- config.go:Configuration
  - add `CloneDirectory` to the `Storage` struct

- dataset.go:cloneAndZip
  - create Job directory in `TargetDirectory` AND in `CloneDirectory`
  - hand over `CloneDirectory/Job` to cloneRepo()
  - change `repodir` to use `CloneDirectory`
    -> zip should look in the correct dir and create in the correct dir

- dataset.go:derepoCloneDir
  - remove usage of this function
  -> save code to somewhere or keep function with a comment

- dataset.go:zip
  - ignore still existing `.git` dir when creating zip file;
  - actually the other way around: hand over all file paths except for the `.git` to be added to the zip file.

- either workdispatcher.go:Worker.start() ignores the createRegisteredDataset error and should not
  or
  createRegisteredDataset should not return an error
