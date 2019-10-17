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
from lxml import etree

VERSION = "0.1.0"


class ParserException(Exception):
    """
    Exception wrapper used by various odML parsers.
    """
    pass


def parse_datacite(xml_file):
    parser = etree.XMLParser(remove_comments=True)
    root = etree.parse(xml_file, parser).getroot()
    if not etree.QName(root).localname == 'resource':
        raise ParserException("Could not find datacite root element")


def main(args=None):
    parser = docopt(__doc__, argv=args, version=VERSION)

    cite_file = parser['FILENAME']
    if not os.path.isfile(cite_file):
        print("[Error] Could not access input file '%s'\n" % cite_file)
        exit(1)

    try:
        parse_datacite(cite_file)
    except etree.XMLSyntaxError as exc:
        print("[Error] Could not parse input file '%s'" % cite_file)
        print("\t%s" % exc.msg)
        exit(1)
    except ParserException:
        print("[Error] Could not find the datacite root element in file '%s'" % cite_file)
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
