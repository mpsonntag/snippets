# GIN-DOI project structure

## Project hierarchy

main.go (main)
- web.go (main)
- register.go (main)
- genhtml.go (main)
  - const defginurl     ... "https://gin.g-node.org"
  - const defdoibase    ... "10.12751/g-node."
  - const defstoreurl   ... "https://doid.gin.g-node.org"
  - isURL()
  - readFileAtPath()
  - mkhtml()            ... entry point
  - fetchAndParse()
- keywords.go (main)
  -> G-Node/libgin.RepositoryMetadata
  -> G-Node/libgin.DataCite
  - mkkeywords()        ... entry point
    -> dataset.go:readFileAtURL()
    -> dataset.go:readFileAtPath()
    -> util.go:KeywordPath()
    -> util.go:prepareTemplates()
-- dataset.go (main)
  - readFileAtURL()
  - readFileAtPath()
-- util.go (main)
  - tmplfuncs           ... name to function mapping for html templates
  - templateMap         ... name to template mapping for html templates
  - KeywordPath()
  - prepareTemplates()
    -> templates.common.go:Nav
    -> templates.common.go:Footer

- templates
  - common.go (gdtmpl)
    - Nav               ... navigation bar
    - Footer            ... footer


## main.go

Base entry point to the project. Current commandline options for the built project:

`gindoid start`                     ... runs `web.go:web`; starts the DOI server
`gindoid register [arg]`            ... runs `register.go:register`; not implemented
`gindoid make-html [arg]`           ... runs `genhtml.go:mkhtml`; creates html landing pages from xml file content
`gindoid make-keyword-pages [arg]`  ... runs `keywords.go:mkkeywords`; creates keyword pages from xml file content


## keywords.go

Creates index.html pages for keywords found in provided doi.xml files.

### mkkeywords

Sole function
- cycles through all provided arguments
  - checks if they are doi.xml files or urls to fetch doi.xml files from and unmarshals them to a `libgin.DataCite` struct
  - walks through all keywords for this file; updates the global keyword-dataset mapping with the current keywords and adds the current dataset to all occurring keywords.
- cycle through keyword map and create landing pages for each keyword
  - creates a directory and and `index.html` file for every keyword
- creates a keywords `index.html` file listing all keywords sorted by a) # of linked datasets and b) lexical order
