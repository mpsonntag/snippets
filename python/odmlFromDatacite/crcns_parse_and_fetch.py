"""
Query the public Datacite API for CRCNS specific publications and
download all available data entries as XML files.
"""
import json
import requests

# Adjust as required
DATACITE_API_ENDPOINT = "https://api.datacite.org/dois"
# Page size might be required to be increased at some point
DATACITE_QUERY = "?query=publisher:CRCNS.org&page[size]=500"
DATACITE_API_XML_ENDPOINT = "/application/vnd.datacite.datacite+xml"


def fetch_datacite():
    """
    Query Datacite for CRCNS specific publications and
    download all available data entries as XML files.
    """
    datacite_uri = f"{DATACITE_API_ENDPOINT}{DATACITE_QUERY}"

    print("... running DataCite query")
    req = requests.get(datacite_uri)
    req_json = json.loads(req.text.encode("utf-8"))

    datacite_items = req_json["data"]
    print("... query returned %s data-sets" % len(datacite_items))

    for datacite_item in datacite_items:
        curr_doi = datacite_item['attributes']['doi']
        curr_file_path = "%s.xml" % curr_doi.split("/")[1]

        print(f"... fetching DataCite file '{curr_file_path}'")
        curr_uri = f"{DATACITE_API_ENDPOINT}{DATACITE_API_XML_ENDPOINT}/{curr_doi}"
        req = requests.get(curr_uri)
        with open(curr_file_path, "w+", encoding="utf-8") as curr_file:
            curr_file.write(req.text)


if __name__ == "__main__":
    fetch_datacite()
