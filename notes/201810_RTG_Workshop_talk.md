

Outline
  - thanks for all the data, we tried to integrate it as much as we could

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
    - document abbreviations in filenames, excel sheets and data structures in the readme 
        as well. in a year you will forget the details of at least some of them!
    - when adding new files, folders think about how information in the files 
        can be found and understood

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
    - versioning - data integrity, making it easy to keep access to old file version w/o the version number in filename scheme
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
    - how to extract metadata from a nix file and make it available as a searchable 
      and indexable textfile
  - neo integration for ephys related data

  - how does nix help
    - data integrity: has a built in validator to make sure data is a) not corrupted and 
          b) has all the information that the data model requires (errors and warnings)
    - data organization: nix is hdf5 which is basically a file system. you can move 
          everything into one file. add all data about a project to a single file.
    - data annotation: requires a bit more effort and information to store data forcing 
          to be more explicit, providing the minimal required information (dimensions, 
          labels, units) - a bit inconvenient at first, but pays of in the long run esp. 
          if scripted.
    - findability: connect every piece of data to descriptive metadata - the metadata 
          within a nix file is searchable and links back to its data.
    - reproducibility: raw data, processed data and analysed data in the same file and 
          already connected via tags, multitags and features, easily consumable to 
          reproduce basic figures.


A collection of further tools that can make your life easier
- python and jupyter notebooks
- python virtualenv or even better anaconda to keep project software dependencies 
  separate and workflows reproducible (document whole environments with specific software 
  package versions, be sure whoever reproduces the environment will get the same software packages)
- snakemake - automatize whole analysis pipelines


Hands on session

- teams of 2 - owner of data and naive person
- explain to naive person how the data is structured - if the other person does not understand a step - change this part.
- make a dataset easier to understand by changing a feature
- adding metadata somewhere
- importing the data and metadata to nix
- adding a subsequent analysis step to the nix file




# Slides - Data management workshop

## Outline

-------------------

Thanks to you!

-------------------

- Introduction to data management
  - consumer level
  - user level

- General advice on structuring data

- Tools introduction
  - gin
  - NIX & odML

- Hands on session


## Introduction

    data management

-------------------

    data management 
         ?
    boring! I want to do science!

-------------------

    visceral understanding that good data management is important

-------------------

    The big picture!

    Replication / reroducibility crisis!
    Glimpse it at https://en.wikipedia.org/wiki/Replication_crisis

    1,500 scientists lift the lid on reproducibility
    Nature News Feature, 25.05.2016, ISSN: 0028-0836
    https://www.nature.com/news/1-500-scientists-lift-the-lid-on-reproducibility-1.19970

    "More than 70% of researchers have tried and failed to reproduce another scientist's 
    experiments, and more than half have failed to reproduce their own experiments. 
    Those are some of the telling figures that emerged from Nature's survey of 1,576 
    researchers who took a brief online questionnaire on reproducibility in research."

    [image about factors that prohibit reproducibility]

-------------------

    Collection of key articles about the topic from 2016 until now.

    The awareness arrived in the scientific community that
    many many studies cannot be reproduced
    - missing raw data (from not public to lost)
    - missing information to interpret the raw/processed data or the analysis steps involved
    - different results when employing the analysis pipelines from raw data to final figures

-------------------

    We know we should do sthg about it, but lets make it less abstract and a bit more concrete!

    Data, data about experiments (metadata), analysis scripts and pipelines
    should be
    - easy to find or easy to search and interpret
    - accessible and available
    - repeatable, replicable, reproducible
    - reusable

    Put like this, this is already a lot of work and knowledge to do properly!

-------------------

    There are a couple of initiatives that have invested more time and effort in 
    thinking about these issues. For their conclusions and proposals read up here, e.g.

        FAIR
        The FAIR Guiding Principles for scientific data management and stewardship
        Nature Scientific Data, 15.03.2016, https://doi.org/10.1038/sdata.2016.18

        ReScience
        Sustainable computational science: the ReScience initiative
        PeerJ Computer Science, 18.12.2017, https://doi.org/10.7717/peerj-cs.142
        https://rescience.github.io

-------------------

    Cool, that was the big picture.
    
    I'll keep it in mind, when I'm a PI in two years.
    Again, why should I care when there is so much science to do?

-------------------

    Be nice to your future self!

    In a year from now:
    - where did I put project Awesome2017?
    - which script did I use to create figure something_12b?
    - oh my, 12 different stimuli, was it the one labeled O215Co245_Ramp_12?

-------------------

    How does the above translate into everyday work?

    There are a couple of easy, low maintainance things
    that you can do to make a lot of things easier for you 
    and others.

1) add a readme for every project. Take a moment to describe
 - the folder structure
   - describe which folder contains which kind of files and 
   if there is any specificity to naming or structure of thf files and folders
   - which folder contains which files
   - what do the names mean
   - is there anything important about how the project is structured
- the workflow
   - which is raw data, which is processed data
   - how do you get from raw to processed in general terms + scripts involved

- waaah, my workflow has changed, I don't want to rewrite the whole readme:
  - like in a labbook just add the changes with a date at the top and you're good!

-------------------

    If you want to be thorough, take a half day and make sure the following
    is true for every project, also add it directly to the project folder.

2) Make sure everything required is in the project or properly referenced
  - scripts used for processing and analysis
  - description of any abbreviations used
  - hardware information
  - software used

-------------------

    This part is best done and decided at the beginning of a project.
    Can be done later as well but will take a lot of effort then.

3) Store your data in an intuitive way
  - use existing data models if available - these usually already have documentation how to read the data
    e.g. neo (Ephys), nifti or bids (fMRI), MNE (eeg & meg) [xxx] check here
  - When using your own data model
    - have units and labels unambiguously attached to your data
    - don't nest too deep
    - keep (field)names expressive
    - when possible add descriptions of names and relations directly to the data structure

-------------------

    This part takes some effort once, but pays off in the long run
    and is a good habit to evolve.

4) Document everyday scripting analysis work, keep marked as journal next to your data
  - copy the history of your commands - already helpful
  - if you have time move the relevant commands to a working script - cool
  - add explanatory comments to the script - awesome

-------------------

    This part takes a lot of effort once and bit of upkeep in evolving
    projects. This will help a lot in years to come.

5) Collect additional information about the experiments and add them to the project
  - organism
  - experimental setup
  - software used
  - experimental settings
  - analysis scripts used
  - analysis settings
  
  - if you have to do any of the above steps more than once, write a template and reuse

-------------------

6) Develop a habit

    in case of fire
    git commit
    git push
    leave

  - add and update readme
  - use abbreviations that make sense
  - use templates where-ever you can
  - put in scripts whatever makes sense
  - backup your stuff

-------------------

    In general terms:
    – Make information explicit and unambiguous (avoid hidden knowledge)
    – Try to save all information (avoid information loss)
    – Store similar things in similar ways, sticking to established procedures and organization (avoid ad hoc solutions)

    How to make things easier?
    - Starting even before the data is recorded: Planning data management in advance
    - Automating (meta)data collection procedures as much as possible, storing information in machine-readable ways
    - Using tools, conventions, formats that facilitate data organization

-------------------

Be nice to others! Help getting the scientific community get back on track

    - use open source tools
    - fill in the blanks on data submission
    - open source your datasets

-------------------

Questions and comments so far?

-------------------

How can we make your life easier:

- gin (data hosting)
  - versioning
  - workflow / scripting integration
  - backup
  - indexed search
  - publication
  - data sharing (public and private)

- nix (expressive data format)

    [disclaimer] using nix takes a bit of effort but pays way off

  - store data, processed data, analysed data and metadata in the same file
  - store all labels and units alongside the data
  - adding dimensionality of the data is required - making data sets easy to interpret without knowledge about the oroject.
  - store raw data and data from any subsequent processing step in the same file
  - logically link analysed to the corresponding raw data e.g. spikes to their original traces 
  - since all labels and units are there and the data is linked, you can easily plot both side by side. automatic si unit conversion makes this even easier.
  - attach any metadata directly to the corresponding raw, processed or analysed data
  - search and retrieve data via the easier searchable metadata part.
  - export metadata only for indexing and searching on a larger scale

- odML (metadata format)
  - same features as in nix but standalone when used with other data formats.

