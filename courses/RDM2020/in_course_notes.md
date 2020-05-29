## 29.05.2020 - Student data introduction

### Xiuna Zhu - Bayesian Modeling of learning
- data: eeg, fmri
- wide range of data formats csv, mat, Rdata
- using matlab, R, macos, github, gitlab, sourcetree

- issues: problems with git workflow

### Anna Dewentner, DueringLab, Vascular Cognitive Impairment

- white matter degradation due to blood vessel disease
- using single-shell and multi-shell pipelines
- 60 participants study, 480 MIs, pre-collected data

- data formats: 
- tools: matlab, R

- no major problems, has to use lots of scripts

### Antonia Bose, TUM, Neuroradiology, Neuroenergetics of the human brain

- measure energy consumption in the brain looking at oxygenation and glucose levels
- tools: Hybrid PET-MR, qBOLD (quantitative) & fPET

- 2 sessions per subject: high and low glucose levels

- PET, MR data, physiological parameters from blood samples, trauma questionaire data
- Python, Linux
- FSL/SPM ???
- github

### Elena Bonke, cBrain LMU, Neuroimaging in sport related brain injury (RepImpact)

- looking at specific level of brain injury: subconcussions e.g. headbutt a football
- imaging soccer players during a season

- MRI, fMRI, EEG, balance testing, blood and saliva testing, cognitive testing

- paper based questionaires, redcap software to digitize -> excel files
- digital tests e.g. cognitive functioning and balance performance -> excel files
- imaging data; software pipelines -> excel files
- lab tests -> ??? collaborators do the work -> spss and sas for statistics

- problems: data curation
  - inconsistencies in acquired data

- using lrz sync and share for sharing datafiles with collaborators
- have not heard of the BIDS format

### Ilgin Kolabas, Image acquisition in lightsheet mice microscopy

- 1.3 TB per light sheet scan (3x9 tiles ~2400 slices)
- Fiji ImageJ: data stitching of LZW compression (500 GB)
- Arivis/Imaris Software converter (300 GB)
- all in lab storage and data handling

- annex/datalad? as a solution for distributed drives where the data will be available?

- main problem: how to deal with these amounts of data (~50TB per mouse)

### Eleni Petridou, TUM, Zebrafish retina cell-pair neuro-glia

- life eyes in agaraose
- movie data - gfp, rfp labelled cells that are dividing
- manually identify glial cell pairs
- file containing cell positions and lineage

- analysis of notch sensor levels in sibling cells (ImageJ)
- excel sheet from ImageJ with mean pixel values
- Graphpad prism statistics

- birthdating of retinal neurons

-> imageJ
- workflow: how are the manual steps documented?
  - workfile textfile describing the steps applied
  - ROI files as secondary analysis files
  - in excel files adding comments and appropriate naming

### Rong Fang, Stroke and dementia project

- 600 stroke patients; neuropsycholoical tests, neuroimaging data (brain structural connectome)
- Excel as data, R as language (and Matlab)

issues
- many variables ... management of the variety of input data to analysis results
  - e.g. clinical data (excel sheet) - sex, age, education level etc ~300 variables for each person

- gets raw neuroimaging data and transforms this data
