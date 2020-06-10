# Brain Imaging Data Structure (BIDS)

[xxx] BIDS citation
Gorgolewski, K.J., Auer, T., Calhoun, V.D., Craddock, R.C., Das, S., Duff, E.P., Flandin, G., Ghosh, S.S., Glatard, T., Halchenko, Y.O., Handwerker, D.A., Hanke, M., Keator, D., Li, X., Michael, Z., Maumet, C., Nichols, B.N., Nichols, T.E., Pellman, J., Poline, J.-B., Rokem, A., Schaefer, G., Sochat, V., Triplett, W., Turner, J.A., Varoquaux, G., Poldrack, R.A., 2016. The brain imaging data structure, a format for organizing and describing outputs of neuroimaging experiments. Sci Data 3, 160044.

Research Resource Identifier RRID:SCR_016124

BIDS is an initiative to establish a data structure aimed to consistently organize neuroimaging and behavioral data.

Uses simple file formats and folder structures.

--- https://osf.io/fhm5d/
Not a file format, but a way of structuring your data and providing metadata
–
It specifies which 
file formats 
are to be used (i.e. Nifti, json, tsv)
–
It specifies the 
naming convention 
for files and directories
–
It addresses the problem of 
metadata 
getting lost while doing your research
–
Details from DICOM headers lost in converting DICOM to Nifti
–
Details about the participants
–
Details about the cognitive task an/or experimental manipulations

Rather than as a “standard”, 
you should consider it a widely supported “best practice”

BIDS was initiated at Stanford to address the challenges of OpenFMRI.org (now OpenNeuro.org)

Main focus is on “brain” imaging, i.e. neuroimaging, which is often done in relation to cognitive 
neuroscience

Not only focusses on the imaging aspect
–
Also on the cognitive part of the research (i.e. behavior)
–
Also on other measures of brain activity (i.e. physiology)

In 2016 BIDS was specified for MRI and fMRI, in 2018 also MEG, in 2019 also for EEG and iEEG, 
and more extensions are in the works
---

can also be adopted for other use cases.

Current BIDS usage:
https://miro.medium.com/max/1400/0*hWRIrcNvy7yFxdwQ.png



Trying to be a community project. All users should be aware that they can help making the project better
https://bids.neuroimaging.io/get_involved.html

Many tools have been grown and become available around the BIDS specification.

This relies on the fact that the BIDS specification leads to a strict, stereotypical data structure. To ensure this remains valid and ensure that the tools built around the data structure remain functional, BIDS provides a validator tool. This validator tool can be run on the root of a BIDS repository and will return all errors and warnings it encounters with respect to the BIDS specification. It does not check the contents of the files.

Be aware that putting any additional files in a BIDS structure will invalidate the BIDS project by default. There are two (and a half) ways to deal with this limitation
- Keep all files that are not part of the BIDS specification in directories outside of the BIDS structure. This is also necessary if you want to have the BIDS structure in git.
- add all non-BIDS files to a special file, `.bidsignore`. This works similar to the `.gitignore` functionality, any files mentioned in this file will be ignored by the BIDS validation and by the tools that work with BIDS. Here you will need what you have learned in the first session: navigating the file system, providing correct paths and file extensions.


        *_not_bids.txt
        extra_data/

# The BIDS structure

Definitions - there are a set of terms that are important for the BIDS structure. To avoid misinterpretation, they have been defined here - if you want to use BIDS, it might be worth your time to familiarize yourself with these terms beforehand to be sure you know what you are doing.
https://bids-specification.readthedocs.io/en/stable/02-common-principles.html#definitions


## examples

https://github.com/bids-standard/bids-examples

# The BIDS validator

A validation can be run on a local BIDS directory using a web service provided at 

https://bids-standard.github.io/bids-validator/

[example]

If you are not allowed to provide an off site page access to your data, you can also install and run validation tools locally to ensure, that your BIDS structure remains clean and compatible with any additional tools.

https://github.com/bids-standard/bids-validator


There is no comparable implementation of the web service BIDS validator for local checks, but you can use the python implementation to locally check, whether all files in a BIDS directory are valid BIDS files.

`pip install -U bids_validator`

Example code

    from bids_validator import BIDSValidator
    
    validator = BIDSValidator()
    filepaths = ["/sub-01/anat/sub-01_rec-CSD_T1w.nii.gz", "/sub-01/anat/sub-01_acq-23_rec-CSD_T1w.exe"]
    for filepath in filepaths:
        print(validator.is_bids(filepath))  # will print True, and then False

For the more versed people there is also the option to locally start the full BIDS web service using docker, but we will not cover this here and now. The details are documented on https://github.com/bids-standard/bids-validator

# BIDS converters, tools and apps

https://bids-apps.neuroimaging.io/about/
https://doi.org/10.1371/journal.pcbi.1005209

Outlook - BIDS is at version v1.3.0; any non-backwards compatible changes will be introduced with version v2.0.



# Get involved

- feedback, contribute, provide another usecase example from your project, propose your format to be included
- if you found errors or things that were ambiguous to you or information you felt was missing - you yourself can add this on the starter-kit page - you just need to be signed into github and you can immediately change it
- extend the core specification
https://bids-specification.readthedocs.io/en/stable/06-extensions.html
- ask for or add a new BIDS extension for your formats

YOU CAN ACTUALLY CONTRIBUTE TO MAKE LIVES EASIER FOR THE COMMUNITY AND IN A ROUNDABOUT WAY ALSO FOR YOU




# Linklist

https://github.com/bids-standard/bids-starter-kit

https://bids-specification.readthedocs.io/en/stable/

# assignment

- read through https://github.com/bids-standard/bids-starter-kit and maybe the specification (not that extensive)
- try to map your data to the BIDS structure; if you have problems check the examples page: https://github.com/bids-standard/bids-examples
- create an example dataset based on your own data (does not have to contain actual data, but the structure should fit)
- make sure your example is valid using the online validator

-> for week after
- locally clone the gin repo
- create a new branch with your full name
- add your example dataset to your branch and push to gin. Check the GIN FAQ / gin-cli notes for details.

