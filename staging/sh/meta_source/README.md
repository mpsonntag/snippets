# Notes on the 'crcns_scrape_datacite' script

Run the `crcns_scrape_datacite` script from any working directory. It will go through all 
available datasets from the crcns.org page and try to scrape the "10.6080/*" publication 
ids; it will further download the corresponding datacite XML files using the identified
ids via the datacite API.
Unfortunately in the past there was no way to identify and get all datacite files
for the publisher "CRCNS.org" or via the publisher prefix "10.6080" which made this
scraper script necessary.
The structure of the datasets referenced on "crcns.org" is mostly coherent, but there
are edge cases, non published datasets and syntax / copy paste errors which the script
takes into account to a certain degree.

Running the script does not require any parameters and will put all resulting files and 
directories in the working directory
```bash
bash [path]/crcns_scrape_datacite
```

## Number of available datasets (18.06-2021) and notes for re-run
When comparing the current state (18.06.2021) of files curl'ed to the datacite folder 
(`ls datacite | wc` ... 130) with the number of crcns datasets (`cat crcns_categories | wc` ... 140-1) 
and the number of datasets not published via CRCNS.org = 9 it can be concluded, that all 
available CRCNS.org datacite files have been acquired.
When running the `crcns_scrape_datacite` script again and it results in a different number 
of datasets in `crcns_categories`, then the `crcns_doi_id` and `crcns_doi_id_log` files 
should be checked whether there were any issues with downloading new files 
e.g. syntax issues in the crcns links along the line.


## Notes on problematic dataset links
#### typos or copy/paste issues in links
- https://crcns.org/data-sets/vc/pvc-6/about_pvc-6            http://dx.doi.org/10.6080/K0H12ZXD
- https://crcns.org/data-sets/vc/v1v2-1/about_v1v2-1          http://dx.doi.org/10.6080/K0B27SHN
- https://crcns.org/data-sets/pfc/pfc-3/about-pfc-2           http://dx.doi.org/10.6080/K0ZW1HVD
- https://crcns.org/data-sets/pfc/pfc-4/about-pfc-2           http://dx.doi.org/10.6080/K0V40S4D
- https://crcns.org/data-sets/ofc/ofc-3/about-ofc-2           http://dx.doi.org/10.6080/K0VM49GF
- https://crcns.org/data-sets/hc/hc-6/about-hc-5              http://dx.doi.org/10.6080/K0NK3BZJ
- https://crcns.org/data-sets/hc/hc-12/about-hc-11            http://dx.doi.org/10.6080/K0R49NQV
- https://crcns.org/data-sets/methods/cai-3/about-ret-2       http://dx.doi.org/10.6080/K05D8PS8
- https://crcns.org/data-sets/bst/vta-2/vta-2                 https://doi.org/10.6080/K0VQ30V9
- https://crcns.org/data-sets/bst/rrf-1/about-rrf-1           https://doi.org/doi:10.6080/K04B2ZJ5

### Datasets not published as CRCNS.org / via datacite
- https://crcns.org/data-sets/vc/v4-1/about-v4-1      https://doi.org/10.6084/m9.figshare.12269513.v1
- https://crcns.org/data-sets/ac/ac-6/about-ac-6      https://doi.gin.g-node.org/10.12751/g-node.df3de6/
- https://crcns.org/data-sets/motor-cortex/alm-5/about-alm-5  https://doi.org/10.25378/janelia.7489253
- https://crcns.org/data-sets/ssc/ssc-12              https://doi.org/10.5061/dryad.nk98sf7q7
- https://crcns.org/data-sets/hc/hc-23/about-hc-23    https://doi.org/10.6084/m9.figshare.c.4496375
- https://crcns.org/data-sets/movements/dream
- https://crcns.org/data-sets/movements/zipser-1
- https://crcns.org/data-sets/tools/mesmerize
- https://crcns.org/data-sets/tunicates/ci-1/about-ci-1   https://doi.org/10.6084/m9.figshare.10289162
