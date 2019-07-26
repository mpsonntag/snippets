# Research DataManagement Course SS201907


## 25.07

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

 
