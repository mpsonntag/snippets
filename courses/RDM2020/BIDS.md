# Brain Imaging Data Structure (BIDS)

BIDS is an initiative to establish a data structure aimed to consistently organize and document neuroimaging and connected behavioral data.

Gorgolewski, K.J., Auer, T., Calhoun, V.D., Craddock, R.C., Das, S., Duff, E.P., Flandin, G., Ghosh, S.S., Glatard, T., Halchenko, Y.O., Handwerker, D.A., Hanke, M., Keator, D., Li, X., Michael, Z., Maumet, C., Nichols, B.N., Nichols, T.E., Pellman, J., Poline, J.-B., Rokem, A., Schaefer, G., Sochat, V., Triplett, W., Turner, J.A., Varoquaux, G., Poldrack, R.A., 2016. The brain imaging data structure, a format for organizing and describing outputs of neuroimaging experiments. Sci Data 3, 160044.

Research Resource Identifier RRID:SCR_016124

https://bids.neuroimaging.io


It is not a standard per se but a best practice model to enable data sharing and open source tool development based on a common data structure.

To this end the BIDS standard specifies
- which file formats are to be used for a use case (i.e. Nifti, json, tsv)
- the naming convention for files and directories
- core metadata and how they are to be stored e.g. about participants, stimuli and key recording settings

Besides the imaging aspect it includes
- behavior
- physiology

So far full BIDS specifications exist for
- MRI (2016)
- fMRI (2016)
- MEG (2018)
- EEG (2019)
- iEEG (2019)

Specification extensions e.g. for PET or CT are currently being developed by the community. 

# The BIDS structure

The Brain Imaging Data Structure (BIDS) specifies folder structures and file names as well as supported file types for different types of neuroimaging data.

## The BIDS folder structure and supported file formats

https://github.com/bids-standard/bids-starter-kit/wiki

### BIDS file type support
- `.json` files to document metadata
- `.tsv` files containing tab separated tabular metadata - no CSV, no excel, only true tabs, no spacing
- raw data files specific to the modality that the project contains e.g. nii.gz files for an anatomical MRI project; only NIFTI files are supported, .

### BIDS general folder structure

project                 exampleProjectName
└── subject             └── sub-subject_id_01
    └── session             └── ses-session_number_01
        └── datatype            └── anat
        └── datatype            └── func

`project`   ... can have any name; should be descriptive
`subject`   ... `sub-<participant label>`
                Label has to be specific for each subject
                Only one folder per subject per dataset
`session`   ... `sub-<session label>`
                Each folder represents a recording session
                If required use multiple sessions per subject
                The session label has to be unique per subject
`datatype`  ... defines the types of data used in this dataset
                Has to be one of the following using this wording:
                `func`, `dwi`, `fmap`, `anat`, `meg`, `eeg`, `ieeg`, `beh`

`func`      ... Functional MRI data
`dwi`       ... Diffusion Imaging Data
`fmap`      ... Fieldmap MRI data
`anat`      ... Anatomical MRI data
`meg`       ... MEG data
`eeg`       ... EEG Data
`ieeg`      ... intracranial EEG data
`beh`       ... behavior

All of the datatypes allow only specific files that are specifically named

### File names and folder structure
Metadata and data file names depend on the project type and the folder names!

Example

 anat: Anatomical MRI data (`myProject/sub-01/ses-01/anat/`)

    Data:
        sub-<>_ses-<>_T1w.nii.gz
    Metadata:
        sub-<>_ses-<>_T1w.json

The root of the project folder should contain the following files:
- `README`
- `dataset_description.json`
- `participants.tsv`

These files have to be named exactly like written above and they must not be empty.
Be aware that putting any additional files in a BIDS structure will invalidate the BIDS project by default. There are two (and a half) ways to deal with this limitation
- Keep all files that are not part of the BIDS specification in directories outside of the BIDS structure. This is also necessary if you want to have the BIDS structure in git.
- add all non-BIDS files to a special file, `.bidsignore`. This works similar to the `.gitignore` functionality, any files mentioned in this file will be ignored by the BIDS validation and by the tools that work with BIDS. Here you will need what you have learned in the first session: navigating the file system, providing correct paths and file extensions.


        *_not_bids.txt
        extra_data/

## Examples

Example project structure

```
ds001
├── dataset_description.json
├── participants.tsv
├── sub-01
│   ├── anat
│   │   ├── sub-01_inplaneT2.nii.gz
│   │   └── sub-01_T1w.nii.gz
│   └── func
│       ├── sub-01_task-balloonanalogrisktask_run-01_bold.nii.gz
│       ├── sub-01_task-balloonanalogrisktask_run-01_events.tsv
│       ├── sub-01_task-balloonanalogrisktask_run-02_bold.nii.gz
│       ├── sub-01_task-balloonanalogrisktask_run-02_events.tsv
├── sub-02
│   ├── anat
│   │   ├── sub-02_inplaneT2.nii.gz
│   │   └── sub-02_T1w.nii.gz
│   └── func
│       ├── sub-02_task-balloonanalogrisktask_run-01_bold.nii.gz
│       ├── sub-02_task-balloonanalogrisktask_run-01_events.tsv
│       ├── sub-02_task-balloonanalogrisktask_run-02_bold.nii.gz
│       ├── sub-02_task-balloonanalogrisktask_run-02_events.tsv
...
└── task-balloonanalogrisktask_bold.json
```

Find more examples at
https://github.com/bids-standard/bids-examples

# The BIDS validator

A validation can be run on a local BIDS directory using a web service provided at 

https://bids-standard.github.io/bids-validator/

[example]

If you are not allowed to provide an off site page access to your data, you can also install and run validation tools locally to ensure, that your BIDS structure remains clean and compatible with any additional tools.

https://github.com/bids-standard/bids-validator

Local installation:
- nodejs (full functionality, commandline tool)
- Python (reduced functionality)
- docker

# The BIDS Specification

https://bids-specification.readthedocs.io/en/stable/

Detailed example, how to read and use to get a properly valid BIDS structure for a modality
https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/03-electroencephalography.html

Definitions - there are a set of terms that are important for the BIDS structure. To avoid misinterpretation, they have been defined here 
- if you want to use BIDS, it might be worth your time to familiarize yourself with these terms beforehand to be sure you know what you are doing.
https://bids-specification.readthedocs.io/en/stable/02-common-principles.html#definitions


# BIDS specifications in the making - get involved

https://bids.neuroimaging.io/get_involved.html

Example: BIDS for PET is close to finishing


- feedback, contribute, provide another usecase example from your project, propose your format to be included
- if you found errors or things that were ambiguous to you or information you felt was missing - you yourself can add this on the starter-kit page - you just need to be signed into github and you can immediately change it
- extend the core specification
https://bids-specification.readthedocs.io/en/stable/06-extensions.html
- ask for or add a new BIDS extension for your formats

YOU CAN ACTUALLY CONTRIBUTE TO MAKE LIVES EASIER FOR THE COMMUNITY AND IN A ROUNDABOUT WAY ALSO FOR YOU


# BIDS converters, tools and apps

List of tools
https://bids.neuroimaging.io/benefits.html

Raw data to BIDS converter
https://github.com/Donders-Institute/bidscoin

BIDS apps - applications that work with BIDS datasets
https://bids-apps.neuroimaging.io/about/
https://doi.org/10.1371/journal.pcbi.1005209

Example app
https://github.com/poldracklab/fmriprep

Outlook - BIDS is at version v1.4.0; any non-backwards compatible changes will be introduced with version v2.0.

# Specific tutorials
https://github.com/bids-standard/bids-starter-kit/wiki/Tutorials


# Linklist
https://bids.neuroimaging.io
https://bids-specification.readthedocs.io/en/stable/
https://github.com/bids-standard/bids-starter-kit

Papers

BIDS
https://doi.org/10.1038/sdata.2016.44
EEG-BIDS
https://doi.org/10.1038/s41597-019-0104-8
iEEG BIDS
https://doi.org/10.1038/s41597-019-0105-7
MEG BIDS
https://doi.org/10.1038/sdata.2018.110
BIDS apps
https://doi.org/10.1371/journal.pcbi.1005209 

# assignment
- read through https://github.com/bids-standard/bids-starter-kit and maybe the specification (not that extensive)
- try to map your data to the BIDS structure; if you have problems check the examples page: https://github.com/bids-standard/bids-examples
- create an example dataset based on your own data (does not have to contain actual data, but the structure should fit)
- make sure your example is valid using the online validator
- then read through the specification for your dataset and try to find some metadata, validate again

-> for week after
- locally clone the gin repo
- create a new branch with your full name
- add your example dataset to your branch and push to gin. Check the GIN FAQ / gin-cli notes for details.

