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

VERSION = "0.1.0"


def main(args=None):
    parser = docopt(__doc__, argv=args, version=VERSION)

    cite_file = parser['FILENAME']
    if not os.path.isfile(cite_file):
        print("[Error] Could not access file '%s'\n" % cite_file)
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
