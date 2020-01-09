# Notes for datacite->odml conversion

To manually get the datacite file for a CRCNS.org publication
- get the title from the CRCNS data-set details page
- paste with quotes in search.datacite.org
- open result page and DL XML or JSON datacite file from link on the side 

Another way to get these files:
- look up the CRCNS.org DOI e.g. https://doi.org/10.6080/k0wd3xh6 
- replace link to https://search.datacite.org/works/10.6080/k0wd3xh6
- open page and DL XML or JSON datacite file from link on the side

To automate the stripping of datacite files from DataCite.org, use the api:
    https://support.datacite.org/docs/api

- Do as above, but replace the link with the following links:
    https://api.datacite.org/dois/application/vnd.datacite.datacite+xml/10.6080/k0wd3xh6
    https://api.datacite.org/dois/application/vnd.datacite.datacite+json/10.6080/k0wd3xh6


