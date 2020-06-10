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
