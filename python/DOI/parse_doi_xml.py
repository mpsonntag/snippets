"""
Ripped code to load specific data from an online doi.xml file. Might be useful
at some point in the future.
"""

import sys

import requests

from lxml import etree

DATACITE_NAMESPACE = "{http://datacite.org/schema/kernel-4}"
GNODE_DOI_URL = "https://doi.gin.g-node.org/10.12751/"
CONF = {"reg_id": "__ID__"}


def parse_doi_xml(xml_string):
    """
    Parses title, dates, creators and citation from an XML string and
    returns this information as dict.
    :param xml_string: XML string containing G-Node DOI metadata.
    :return: dict containing the parsed XML information.
    """
    doi_conf = {}
    dsns = DATACITE_NAMESPACE

    root = etree.fromstring(xml_string)
    # Handle title
    title = root.find(f"{dsns}titles").find(f"{dsns}title").text
    if title:
        doi_conf["title"] = title

    # Handle date
    date = root.find(f"{dsns}dates").find(f"{dsns}date").text
    if date:
        doi_conf["reg_date"] = date

    # Handle citation
    citation = ""
    creators = root.find(f"{dsns}creators").findall(f"{dsns}creator")
    for creator in creators:
        curr = creator.find(f"{dsns}creatorName").text
        curr = curr.replace(",", "").split(" ")
        citation = f"{citation}, {curr[0]} {curr[-1][0]}"
    if citation:
        doi_conf["citation"] = citation

    return doi_conf


def run():
    """
    Fetches the XML file for a specific G-Node DOI id and parses the XML content.
    """
    print(f"-- Loading doi xml for 'g-node.{CONF['reg_id']}'")
    doi_url = f"{GNODE_DOI_URL}g-node.{CONF['reg_id']}/doi.xml"
    res = requests.get(doi_url)
    if res.status_code != 200:
        print(f"-- ERROR: Status code {res.status_code}; could not access requested DOI")
        sys.exit(-1)

    _ = parse_doi_xml(res.text.encode())


if __name__ == "__main__":
    run()
