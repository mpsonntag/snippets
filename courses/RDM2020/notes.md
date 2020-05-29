- read through data management materials, find new ones
- give basic examples
  - include thomas' suggestions
  - include suggestions from the venice course
  - add new suggestions
  - think about how to include them in the general odml introductions
  - if adding links in the tutorial, add access tests to ensure that these links are always available.
- give an example of how to use local style

- try to document all settings for every experiment/setup; save it with every experiment, keep it close to the raw data, make the connections clear
- try to automate settings documentation
  - template and manual checklist
  - if available, save settings to file and connect to raw data

- check the bids standard as example for a structured workflow/metadata collection

- leave comments every where! it does not hurt and helps later on

- when taking notes, use open standards, ideally ones that are machine readable and writeable and that are common:
  - json
  - yaml
  - markdown for notes

- bids as example

- real live example: odml of a calcium imaging experiment


# Course outline

## Metadata part
- Thomas already explained the concept of metadata and why they are important

- Examples how other people deal with metadata

- Which metadata are usually collected -> examples -> labbook, strains, stimulus protocols

- How to approach metadata collection?
  - Obey good practices from the start
  - Good practice examples
    - Thomas examples
    - Examples from other projects, websites, tutorials

- Different concepts?
  - Project based
  - Experiment based
  - Protocol based
  - Strain/animal based
  - Date based
  - Experimenter based

  -> We cannot tell what the correct concept is for your organisation, there are too many variables, some of which we might not even know

- Different methods
  - Labbook
  - CSV files
  - Text documents

- Different use cases?

- Identify required metadata in a project and choose a documenting concept

- odML: a tool to automate metadata collection
  - Template concept

  - odML jupyter notebook
    - Links
    - Basic concepts (save, load, create docs, add template to document)

  - Why automation:
    - Less error prone
    - Reduce documentation work
    - Quickly get an overview with the xml local style - view in browser
    - Glue a yaml printout in your labbook  
    - Reformat and hand over partial metadata with more ease e.g. when in a project based style of documentation extract infos about experiments with a specific strain and compile all information with more ease.
      - Example: compile a list of experiments where a specific person did the experiments -> collect docs and view in browser with localview

## Open Data storage <-> Metadata connection part: NIX (Neuroscience Information Exchange) format

- Update NIX jupyter notebook
  - get RDM2019 to the point of the nixio tutorial
