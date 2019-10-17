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

from docopt import docopt
from lxml import etree as ET
from lxml.etree import XMLSyntaxError

VERSION = "0.1.0"


def parse_datacite(xml_file):
    parser = ET.XMLParser(remove_comments=True)
    ET.parse(xml_file, parser).getroot()


def main(args=None):
    parser = docopt(__doc__, argv=args, version=VERSION)

    cite_file = parser['FILENAME']
    if not os.path.isfile(cite_file):
        print("[Error] Could not access input file '%s'\n" % cite_file)
        exit(1)

    try:
        parse_datacite(cite_file)
    except XMLSyntaxError as exc:
        print("[Error] Could not parse input file '%s'" % cite_file)
        print("\t%s" % exc.msg)
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
