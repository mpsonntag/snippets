# Research DataManagement Course SS201907


## 25.07
[T] RDM course notes:
Hands on suggestions for reorganising Data and structures and general conventions
- Add a bash guide for file manipulation, markdown guide for readmes, json/yaml guide for parameter files
- Add a readme to explain the project folder structure and how it can be made use of ... for your future self and maybe your PI
  A readme should contain:
  - Brief description of the folder structure
  - Brief description of which filetypes can be found where and which programs can be used to open them, if they are not
      special common.
  - Description of data analysis pipeline
- parameter files
  - use yaml or json if your software supports it
  - add comments to each parameter explaining what it is, what it does in the software and if applicable which units they are in
- Organise folder strucutre - give a couple of examples how other people organized their data as a help how to structure your own
  - Project ... stick to introducting projects for a scientific question.
      don't be afraid to duplicate data if it keeps the repository structure clean
    - Experiments ... should at least contain a reference to the raw data ... but tricky ... rename, move, delete
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
- Define a naming scheme for Projects and Experiments early on and use these as reference in your LABBOOK
- Define 2h a week to curate Data and update documentation - you will benefit in the longrun
- Define 2h a week to add automation to your analysis




Open Questions for us:
- how to deal with folder reorganisation
  - if it is a major reorganisation of files and folders, keep the old structure with a date in the repository, 
    so that old scripts will still run

   e.g.

   - Project
     - 2019-07-25_before_reorganisation ... can also be zipped, but should be complete, if you don't version your repo
       - Experiments
       - Stimulus
       ...
     - Experiments
     ...

- how to deal with changes in naming schemes
- how to deal with additional parameters
  - how to best add them
  - how to keep software able to include old data

- use jupyter notebooks to already document your workflow if you can - what is our stance on subnotebooks if 
  the workflow is too large.
- we should give recommendations on how to organize code in a workflow as well
- restructure scripts:
  - move parameters to the top of a script and document them
  - move code to functions

[T] gin - sift through all repositories and check different project structures to identify common patterns that
          we can give as examples how to structure a project folder.



