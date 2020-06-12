# Basic BIDS validation examples

Upload the following folders to https://bids-standard.github.io/bids-validator/ and try to fix the warnings.

## 01_empty_example/

    01_empty_example
    ├── datafile.txt
    ├── dataset_description.json
    └── .bidsignore

- This directory is basically no BIDS directory. It only shows the error message if a directory is not identified as related to BIDS.

## 02_invalid_structure/

    02_invalid_structure
    ├── invalid_folder
    │   └── invalid_file.txt
    └── sub-01
        ├── invalid_folder_name
        │   └── unsupported_file.txt
        └── ses-01
            └── anat
                └── sub-01_ses-01_T1w.nii.gz

- This directory structure contains unsupported folders. Remove all folders until there are no more "NOT_INCLUDED" error warnings.
- Notice that empty files are not allowed in a valid BIDS directory.
- Notice that a dataset description at the root of the BIDS directory is required to provide minimal documentation.

## 03_invalid_file_annotation

    03_invalid_file_annotation
    ├── dataset_description.json
    ├── sub-01
    │   └── ses-01
    │       └── anat
    │           └── sub-01_ses-01_T1w_invalid_annotation.nii.gz
    └── sub-custom
        └── ses-custom
            └── anat
                └── sub-02_ses-02_T1w.nii.gz

- This directory contains issues in its file names.
- Note that custom subject and session annotations are valid, if they are properly passed along to the file names.
- Also not that special characters like space, "-" and "_" should be avoided in any naming scheme.

## 04_invalid_additional_file

    04_invalid_additional_file
    ├── dataset_description.json
    ├── additional_file.txt
    ├── README.md
    ├── sub-01
    │   ├── additional_file.txt
    │   └── ses-01
    │       └── anat
    │           └── sub-01_ses-01_T1w_invalid_annotation.nii.gz
    └── sub-02
        └── ses-02
            └── anat
                ├── sub-01_ses-01_T1w_invalid_annotation.nii.gz
                └── sub-02_ses-02_unsupported_file.tsv

- Note that only specific file types are allowed at specific levels of the BIDS directory hierarchy.
- Note that a README file is allowed at the root, but only if its name fits exactly.
- Note that additional files can be excluded from the BIDS validation using a ".bidsignore" file in the root of the directory. Add a bidsignore file, that ignores all files with the text extension ".txt".

