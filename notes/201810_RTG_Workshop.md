

Introduction

- general intro to data and metadata handling
  why care about this:
  - make your life easier
  - make the life of your colleages / PIs / collaborators / community easier
  - address major problems in science:
    - reproducibility
    - open data

- project structuring best practices
  - be nice to your future self!
  - for each project add a readme briefly describing your project file organization
    - document abbreviations in filenames, excel sheets and data structures in the readme as well. in a year you will forget the details of at least some of them!
    - when adding new files, folders think about how information in the files can be found and understood

  - collect information about your experiments (metadata) and your workflow from the beginning
    - which information is metadata and interesting
    - ideally document your workflow through scripts and add comments to every important step
    - use reusable templates for collecting metadata
    - connect metadata in an easy to consume way to the appropriate data
  - keep things together that belong together - data, metadata and analysis scripts

  - manual curation takes effort; if you have to manually annotate something more than twice, script!
  - avoid data dumps!

Tools we developed and can provide that can help

- top level data organization: short tutorial of gin / usage
  - why gin is there
  - basics of gin
  - web features, web resources
  - gin-cli features; point to tutorials and recipies
  - how does this help in context of data organization
    - searchability (text file crawling index)
    - versioning
    - reusablility: easy publication and data availability

- project/experiment level organisation: nix usage tutorial with available jupyter notebook
  - nix intro - idea, main contributors, why advantageous in light of what we heard before
  - how to get data into nix
  - dimensions, automatic si unit conversion
  - (multi)tags and features and why they are awesome
  - how to plot using multitags / features
  - how to add metadata
    - quick intro to odML
    - how to add to a nix file
    - how to connect to data
    - how to search for data from metadata
  - neo integration for ephys related data

  - how does nix help
    - with data organization: nix is hdf5 which is basically a file system. you can move everything into one file. add all data about a project to a single file.
    - with annotation: requires a bit more effort and information to store data forcing to be more explicit, providing the minimal required information (dimensions, labels, units) - a bit inconvenient at first, but pays of in the long run esp. if scripted.
    - with findability: connect every piece of data to descriptive metadata - the metadata within a nix file is searchable and links back to its data.
    - with reproducibility: raw data, processed data and analysed data in the same file and already connected via tags, multitags and features, easily consumable to reproduce basic figures.


A collection of further tools that can make your life easier
- python and jupyter notebooks
- conda to keep project software dependencies separate and workflows reproducible (document whole environments with specific software package versions, be sure whoever reproduces the environment will get the same software packages)
- snakemake - automatize whole analysis pipelines


Hands on session

- teams of 2 - owner of data and naive person
- explain to naive person how the data is structured - if the other person does not understand a step - change this part.
- make a dataset easier to understand by changing a feature
- adding metadata somewhere
- importing the data and metadata to nix
- adding a subsequent analysis step to the nix file
