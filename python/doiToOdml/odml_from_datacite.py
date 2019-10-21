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
from lxml import etree
from xml.parsers.expat import ExpatError

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


def parse_datacite_dict(doc):
    """
    :param doc: python dict containing datacite conform data to
                be parsed.
    """
    if not doc or "resource" not in doc:
        raise ParserException("Could not find root")

#    supported_tags = ["identifier", "creators", "titles", "publisher", "publicationYear",
#                      "subjects", "contributors", "dates", "language", "resourceType",
#                      "alternateIdentifiers", "relatedIdentifiers", "sizes", "formats",
#                      "version", "rightsList", "descriptions", "geoLocations",
#                      "fundingReferences"]
    supported_tags = ["identifier"]


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
