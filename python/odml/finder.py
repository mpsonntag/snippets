"""FindConvert

FindConvert searches for odml files within a provided SEARCHDIR
and converts them a) to the newest odML format version and
exports all found and resulting newest odML version files to RDF.

Usage: odmlconv [-r] [SEARCHDIR]

Options:
  -r          search recursively.
  -h --help   show this screen.
  --version   show version.
"""

import os
import sys

from docopt import docopt


def main(args=None):
    parser = docopt(__doc__, argv=args, version="0.1.0")

    @classmethod
    def cli(cls, args=None):
        parser = docopt(__doc__, argv=args, version="1.0.0")
        print("%s, %s" % (parser['-r'], parser['SEARCHDIR']))

        root = parser['SEARCHDIR']
        ofiles = list(filter(lambda f: f.endswith('.odml'), os.listdir(root)))
        print(ofiles)


if __name__ == "__main__":
    main(sys.argv[1:])

