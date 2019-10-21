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
    supported_tags = {"identifier": handle_identifier}

    for node in dcite_root:
        if node in supported_tags:
            supported_tags[node](dcite_root[node])


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
