import datacite

# fetch the XML DataCite file for a specific published data-set

doi = "10.6080/K0G15XS1"

dclient = datacite.DataCiteMDSClient()
curr_xml = dclient.metadata_get(doi)

# because I noticed it: you are using the v1 datacite REST API; they updated the API at some point; the current version does not use the '/works' endpoint any longer.

# you can either use the datacite python package (pip install datacite) to download the XML files for a published data set from the DOI
# or use the REST API to get the JSON files as you already did and then again use the datacite package to convert it to XML.


