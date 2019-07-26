# Research DataManagement Course SS201907

[N] ... toNote
[T] ... toDo
[C] ... toCheck


## Course preparations
### Pre-course installation

Installation:
- Git https://git-scm.com/downloads

Do not install both Anaconda (Beginner) and the Python 3.7 (Advanced).
Only one of the two.

Beginner Python install:
- Anaconda https://www.anaconda.com/distribution/
Launch Anaconda prompt from Start Menu: pip install nixio

Advanced Python install:
- Python 3.7 https://www.python.org/downloads/
After installing Python, open command prompt (cmd) or terminal and run:
python -m pip install --upgrade pip
python -m pip install jupyterlab matplotlib nixio

- GIN client: https://gin.g-node.org/G-Node/Info/wiki/GinCliSetup

1. Python tutorial: https://docs.python.org/3/tutorial/
Chapters 1 through 4 (5 optional)
2. GitHub git help/guides: https://help.github.com/en/articles/set-up-git
3. NIXPy tutorial: https://nixpy.readthedocs.io/en/latest/tutorial.html
4. GIN client tutorial: https://gin.g-node.org/G-Node/Info/wiki/GinUsageTutorial

- Matlab: make sure they can use it from off-site

### Course preparation notes
- Students will bring their own data and will briefly present them on the first day
- git introduction
- python introduction
- nix introduction - probably with Spyder in Python or in Matlab with the nix bindings.
- testing introduction
  - give a brief introduction for python and matlab
  - show what happens when the script changes
  - provide templates for tests that just need to be changed and new tests added
  - short introduction to tests via github/CI to expose them to the options that 
    are available.


## Course notes


### 22.07


[T] gin ... put some replicability etc terms in the general gin description

[T] RDM course ... put RDM slides somewhere we can find it?

[T] RDM course ...
    - define first the report, describe your data
    - collect metadata as automatic as possible
    - create a) automatically out of b)

[T] RDM course/conferences ...
    Grants will require a data management plan. Think about RDM in time, so there are no
    time issues.

[T] odml ... give usage examples how to get tabular data out of odML via odMLTables both 
      GUI and via scripting

[T] RDM ... trivial but treat data management as a todo like meetings. pick a day of the 
      weak, reserve and spend 2h on RDM continuously

[T] RDM ... discussion ... ad hoc data changes vs refinement vs stick to the plan
    we often have exploratory science, what are our recommendations when
    e.g. a new parameter comes along or if a data structure needs to change 

[T] RDM ... what is our policy on data migration ... can we give help there?
     ideally we have an automization script from the start ... continuously use it to 
     create publishable data files while keeping the plain ones.

[T] RDM ... think ahead ... do you need more cameras, LEDs, diff stimuli in the future
    - when writing software make it backwards compatible.

[T] odml ... as with mp3s, don't care about folder structures. an odml editor should
      provide all reqired files, so that the researcher does not have to care too
      much about it. The editor should in term warn, if files have moved.
      Look into git and metadata strcutures ... check if we can come up with
      templates [?]

[T] RDM/tip ... When there are parameter files add comments directly there

[T] RDM/tip ... a problem with automation might be: there are too many plots at every run
        ... add a plot suppression feature to the code so that only the bare necessities
            are created on a pipe run. if you need all info, run without the flag.

[T] odml ... how to deal with warnings and errors

[N] personal ... provide courses on usage of various software tools for free
      at universities .. 2 weeks Tu-Th every two months?

[N] when we have guidelines for bulid pipelines approach the papers and offer the knowledge 

[C] openscience ... reviews on github

[C] Software and data carpentry


### 23.07

[T] RDM course ... after the git course ... history to file and
     upload to GIN course repo

[T] odML ... check whether paragraphs are properly exported to yml

    """
    paragraph:>
      text

      text
    """


### 24.07

[T] nixpy ... when handing a numpy.str_ to a nix entity name it crashes.

[T] odml ... add metadata description to odML tutorial, info pages and link 
      presentaions from there.

[T] odML ... actuaklly spell it out which program was used to create a specific file.

[T] odML ... design generic high level metadata structure to choose from.
     e.g. project - experiment - subject - etc
          stubject - experiment - etc
     take BIDS structure as one example

[T] odML ... terminology RRID

[T] RDM course ... update code snippet to jupyter style in thomas screenshot
     presentation ... contains old odML code

[T] conference notes ... why odml ... everything is stored in one place and machine 
      readable and can write a report tool to create a report for every new experiment
    still not different from matlab custom cells and reporting ...

[T] RDM course ... actually read lyubas paper and distill guidelines for metadata 
      extraction and organisation

[N] RDM course .... we would have liked to achieve two things
    - you are more aware that metadata annotation is really important for science
      and your own rememberance in a year
    - that your data is a bit more organized and annotated by the end of the course

[T] RDM course ... guidelines on what to document
    - what is the data structure
    - what are file types used and how can they be opened
    - what do files contain
    - how do files relate to each other - in a pipeline context - which one is the 
      raw data which is the analysed data etc.

[T] RDM course / gnode ... to discuss ... what are our own guidelines for data management

[N] publish your software via gin and DOI

[T] nixpy ... add tutorial examples to tests to make sure that these examples
      will also work with any current version of nixpy.

[T] gnode project ... Data organisation: can we come up with a simple shell script, 
    that traverses the file structure of a repo and
    - extracts all file types used
    - gives a tree of the current file structure
    - provides short initial texts and a project description template that just
      needs to be filled out
    - spits it out as markdown, that can easily be updated and extended to
      make documenting the contents of a repo easier.
    - also create a file with improvement notes e.g. when there are whitespaces or
      special characters in file or foldernames and reports on duplicate filenames
      could also have duplicate file checks
    - could be a go project since it nicely ports to all systems


### 25.07

[P] RDM course presentation by ???
    electrophysiology ... LFP and spike sorting data
    monkey task recordings
    original data Matlab ... data munged to python numpy data
    pipeline in jupyter notebooks that get quite large
    uses pickl to store results ... could be moved to a different format

[T] poster ... put DOI options: publication, data publication, software publication
    on poster

[C] gin ... how are large files in gin actually handled ... are old file versions 
    of large files kept locally if new versions are pushed to the server?
    if you remove large file content from the local host will it allow it, if
    there are large file versions, that are not yet on the server and would be
    lost I assume? 

[T] gin ... create usage comic/schematics for gin use cases - what happens where
    with which files.

[T] RDF ... create query to look for specific recording software / equipment / files
    to search for datasets that one can actually access and use.

[T] RDF ... on the RDF conversion service keep a copy of all uploaded and converted
    files with IP and date even after the upload is done and back that stuff up.

[T] gin ... should we add searchable categories or search suggestions based on keywords
    in .datacite.yml files and display these in the dashboard? then redirect to search
    with the respective term.

[R] conference notes ... there are journals that specifically publish datasets w/o a 
    new scientific finding.

[T] license notes ... get license knowledge its own notes file
    - creativecommons.org
    - facts are not licensible ... research data are facts ... all data cannot be licensed
      but the intention of an author/publisher can be made clear e.g. that they would
      like a contribution note if someone else uses their data.

[T] Put software from university studies on github

[T] gin-cli ... the description of `remote-add` is not fully helpful ... maybe add a 
      specific example?

[T] gin resources .... if ok, move all slides and presentations to the gin public resources.

[T] RDM course notes:

Hands on suggestions for reorganising Data and structures and general conventions
- Add a bash guide for file manipulation, markdown guide for readmes, json/yaml guide for 
  parameter files
- Add a readme to explain the project folder structure and how it can be made use of 
  ... for your future self and maybe your PI
  A readme should contain:
  - Brief description of the folder structure
  - Brief description of which filetypes can be found where and which programs can be used 
    to open them, if they are not special common.
  - Description of data analysis pipeline
- parameter files
  - use yaml or json if your software supports it
  - add comments to each parameter explaining what it is, what it does in the software and 
    if applicable which units they are in
- Organise folder strucutre - give a couple of examples how other people organized their 
  data as a help how to structure your own
  - Project ... stick to introducting projects for a scientific question.
      don't be afraid to duplicate data if it keeps the repository structure clean
    - Experiments ... should at least contain a reference to the raw data 
                  ... but tricky ... rename, move, delete
      - ??? By date
      - ??? By subexperiment e.g. behavior + analysis
    - Stimulus/paradigm
    - Subjects
    - Results
    - Figures
    - Discussion
    - Software
    - Notes
    Readme ... have a readme in every folder, also good place to describe the naming scheme
- Define a naming scheme for Projects and Experiments early on and use these as reference 
  in your LABBOOK
- Define 2h a week to curate Data and update documentation - you will benefit in the longrun
- Define 2h a week to add automation to your analysis
- as guidelines stick to one style of folder structure (see examples above); if you require an
  additional way to display your data use links if possible or work on readonly copies but
  don't have the same editable file in multiple locations without version control.

Open Questions for us:
- how to deal with folder reorganisation
  - if it is a major reorganisation of files and folders, keep the old structure with a 
    date in the repository, so that old scripts will still run

   e.g.

   - Project
     - 2019-07-25_before_reorganisation ... can also be zipped, but should be complete, 
                                            if you don't version your repo
       - Experiments
       - Stimulus
       ...
     - Experiments
     ...

- how to deal with changes in naming schemes
- how to deal with additional parameters
  - how to best add them
  - how to keep software able to include old data

- use jupyter notebooks to already document your workflow if you can - what is our stance on 
  subnotebooks if the workflow is too large.
- we should give recommendations on how to organize code in a workflow as well
- restructure scripts:
  - move parameters to the top of a script and document them
  - move code to functions

[T] gin ... sift through all repositories and check different project structures to identify 
    common patterns that we can give as examples how to structure a project folder.

[T] odml feature ... function to create a section tree from a data/folder_structure
    - with files as properties
    - + a check function if everything in the odml is there
    - need category or type for directories and files to include
    - might want a dict for reserved odml types and it asks if you want to use them

[C] is there a pep8 check for jupyter notebooks

[T] gnode ... should we do an FAQ how to do proper DataManagement lists and examples ... 
    hands on tips to go through to easily improve DataManagement

[C/T] RDM course - add git, bash, json, markdown, yaml, links to tutorials we like
      e.g. GregsBashuide ... mywiki.wooledge.org/bashguide

[T] gin ... good to knows: gin does not support branches due to annex where this is not
    supported yet. does not push large file content. in this case currently use git and 
    annex directly if you want to use branches with annex. -> but does a branch
    merge on the server then properly move the annexed data?

[T] RDM ... for the next one include python environments and docker in the 
      presentation at least or a short introduction.
 
