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
