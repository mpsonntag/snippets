"""
Ripped code to load specific data from an online doi.xml file. Might be useful
at some point in the future.
"""

import requests

from lxml import etree

CONF = {"reg_id": "__ID__"}


def parse_doi_xml(xml_string):
    doi_conf = {}
    dsns = "{http://datacite.org/schema/kernel-4}"

    root = etree.fromstring(xml_string)
    # Handle title
    title = root.find("%stitles" % dsns).find("%stitle" % dsns).text
    if title:
        doi_conf["title"] = title

    # Handle date
    date = root.find("%sdates" % dsns).find("%sdate" % dsns).text
    if date:
        doi_conf["reg_date"] = date

    # Handle citation
    citation = ""
    creators = root.find("%screators" % dsns).findall("%screator" % dsns)
    for creator in creators:
        curr = creator.find("%screatorName" % dsns).text
        curr = curr.replace(",", "").split(" ")
        citation = "%s, %s %s" % (citation, curr[0], curr[-1][0])
    if citation:
        doi_conf["citation"] = citation

    return doi_conf


def run():
    print("-- Loading doi xml for 'g-node.%s'" % CONF["reg_id"])
    doi_url = "https://doi.gin.g-node.org/10.12751/g-node.%s/doi.xml" % CONF["reg_id"]
    res = requests.get(doi_url)
    if res.status_code != 200:
        print("-- ERROR: Status code (%s); could not access requested DOI; "
              "          Make sure access is available." % res.status_code)
        exit(-1)

    _ = parse_doi_xml(res.text.encode())


if __name__ == "__main__":
    run()
