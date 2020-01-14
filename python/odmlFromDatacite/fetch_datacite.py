import json
import os
import requests

import datacite

# Adjust as required
output_dir = os.path.join(os.sep, "tmp", "datacite")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

datacite_api_endpoint = "https://api.datacite.org/dois"
datacite_query = "query=publisher:CRCNS.org&fl=doi,minted,updated,xml&fq=has_metadata:true&fq=is_active:true&rows=1000&start=0&sort=updated+asc&wt=json"

datacite_uri = "%s?%s" % (datacite_api_endpoint, datacite_query)

print("... running DataCite query")
req = requests.get(datacite_uri)
req_json = json.loads(req.text.encode("utf-8"))

datacite_items = req_json["data"]
print("... query returned %s data-sets" % len(datacite_items))

# DataCite interaction client without authorization;
# used to fetch DataCite XML metadata for specific DOIs
dclient = datacite.DataCiteMDSClient()

for idx, datacite_item in enumerate(datacite_items):
    curr_doi = datacite_items[idx]['attributes']['doi']
    curr_filename = "%s.xml" % curr_doi.split("/")[1]
    curr_file_path = os.path.join(output_dir, curr_filename)

    print("... fetching DataCite file '%s'" % curr_filename)
    curr_xml = dclient.metadata_get(curr_doi)
    with open(curr_file_path, "w+") as curr_file:
        curr_file.write(curr_xml)
