"""odmlFromDatacite

Convenience script to parse a datacite xml file
and create an odML xml file with the parsed information.

Usage: odmlFromDatacite FILENAME

Arguments:
    FILENAME    Path and filename of the datacite xml file to be parsed.

Options:
    -h --help   Show this screen.
    --version   Show version number.
"""

import os
import sys
import xmltodict

from docopt import docopt
from xml.parsers.expat import ExpatError

import odml


VERSION = "0.1.0"


class ParserException(Exception):
    """
    Exception wrapper used by various odML parsers.
    """
    pass


def dict_from_xml(xml_file):
    """
    Parse the contents of an xml file into a python dictionary.

    :param xml_file: Location of the xml file to be parsed.
    :return: dictionary containing the contents of the xml file.
    """

    try:
        with open(xml_file) as file:
            doc = xmltodict.parse(file.read())
    except ExpatError as exc:
        raise ParserException("Could not parse file")

    return doc


def handle_identifier(node, odml_doc):
    id_type = "@identifierType"
    id_value = "#text"

    if not node or (id_type not in node and id_value not in node):
        return

    sec = odml.Section(name="identifier", type="DataCite/identifier", parent=odml_doc)
    if id_type in node:
        odml.Property(name="identifierType", values=node[id_type], parent=sec)
    if id_value in node:
        odml.Property(name="identifier", values=node[id_value], parent=sec)


def handle_creators_item(node, sec):
    for sub in node:
        if sub == "creatorName":
            odml.Property(name=sub, values=node[sub]["#text"], parent=sec)
            if "@nameType" in node[sub]:
                odml.Property(name="creatorNameType", values=node[sub]["@nameType"], parent=sec)

        elif sub in ["givenName", "familyName"]:
            odml.Property(name=sub, values=node[sub], parent=sec)
        elif sub == "nameIdentifier":
            # toDo handle multiple name identifier
            subsec = odml.Section(name=sub, type="DataCite/creator", parent=sec)
            odml.Property(name=sub, values=node[sub]["#text"], parent=subsec)
            if "@schemeURI" in node[sub]:
                odml.Property(name="schemeURI", dtype=odml.dtypes.DType.url,
                              values=node[sub]["@schemeURI"], parent=subsec)
            if "@nameIdentifierScheme" in node[sub]:
                odml.Property(name="nameIdentifierScheme",
                              values=node[sub]["@nameIdentifierScheme"], parent=subsec)

        elif sub == "affiliation":
            # toDo handle multiple affiliations
            sec_aff = odml.Section(name=sub, type="DataCite/creator", parent=sec)
            odml.Property(name=sub, values=node[sub]["#text"], parent=sec_aff)
            if "@affiliationIdentifier" in node[sub]:
                odml.Property(name="affiliationIdentifier", values=node[sub]["@affiliationIdentifier"], parent=sec_aff)
            if "@affiliationIdentifierScheme" in node[sub]:
                odml.Property(name="affiliationIdentifierScheme", values=node[sub]["@affiliationIdentifierScheme"],
                              parent=sec_aff)
            if "@schemeURI" in node[sub]:
                odml.Property(name="schemeURI", values=node[sub]["@schemeURI"],
                              dtype=odml.dtypes.DType.url, parent=sec_aff)
        else:
            print("[Warning] Found unsupported node '%s', ignoring" % sub)


def handle_creators(node, odml_doc):
    if not node or "creator" not in node:
        return

    sec = odml.Section(name="creators", type="DataCite/creator", parent=odml_doc)

    for (idx, creator) in enumerate(node["creator"]):
        p_name = "%s %d" % ("creator", idx+1)
        subsec = odml.Section(name=p_name, type="DataCite/creator", parent=sec)
        handle_creators_item(creator, subsec)


def parse_datacite_dict(doc):
    """
    :param doc: python dict containing datacite conform data to
                be parsed.
    """
    if not doc or "resource" not in doc:
        raise ParserException("Could not find root")

    dcite_root = doc["resource"]
    if "identifier" not in dcite_root:
        raise ParserException("Could not find identifier (DOI) node")

#    supported_tags = ["identifier", "creators", "titles", "publisher", "publicationYear",
#                      "subjects", "contributors", "dates", "language", "resourceType",
#                      "alternateIdentifiers", "relatedIdentifiers", "sizes", "formats",
#                      "version", "rightsList", "descriptions", "geoLocations",
#                      "fundingReferences"]
    supported_tags = {"identifier": handle_identifier,
                      "creators": handle_creators}

    odml_doc = odml.Document()
    odml_doc.repository = "https://terminologies.g-node.org/v1.1/terminologies.xml"

    for node in dcite_root:
        if node in supported_tags:
            supported_tags[node](dcite_root[node], odml_doc)


def main(args=None):
    parser = docopt(__doc__, argv=args, version=VERSION)

    cite_file = parser['FILENAME']
    if not os.path.isfile(cite_file):
        print("[Error] Could not access input file '%s'\n" % cite_file)
        exit(1)

    doc = None
    try:
        doc = dict_from_xml(cite_file)
    except ParserException as exc:
        print("[Error] '%s' in file '%s'" % (exc, cite_file))
        exit(1)

    try:
        parse_datacite_dict(doc)
    except ParserException as exc:
        print("[Error] Could not parse input file '%s'\n\t%s" % (cite_file, exc))
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
