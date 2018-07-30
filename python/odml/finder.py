"""odmlFindConvert

odmlFindConvert searches for odml files within a provided SEARCHDIR
and converts them a) to the newest odML format version and
exports all found and resulting newest odML version files to RDF.

Usage: odmlconv [-r] SEARCHDIR

Arguments:
    SEARCHDIR       Directory to search for odML files.

Options:
    -r              search recursively.
    -h --help       show this screen.
    --version       show version.
"""

import os
import pathlib
import sys
import tempfile

from docopt import docopt


def main(args=None):
    parser = docopt(__doc__, argv=args, version="0.1.0")

    root = parser['SEARCHDIR']
    if not os.path.isdir(root):
        print(docopt(__doc__, "-h"))
        exit(1)

    # Handle various odML file endings
    if parser['-r']:
        xfiles = list(pathlib.Path(root).rglob('*.odml'))
        xfiles.extend(list(pathlib.Path(root).rglob('*.xml')))
        jfiles = list(pathlib.Path(root).rglob('*.json'))
        yfiles = list(pathlib.Path(root).rglob('*.yaml'))
    else:
        xfiles = list(pathlib.Path(root).glob('*.odml'))
        xfiles.extend(list(pathlib.Path(root).glob('*.xml')))
        jfiles = list(pathlib.Path(root).glob('*.json'))
        yfiles = list(pathlib.Path(root).glob('*.yaml'))

    # Convert odml to latest version
    tdir = tempfile.mkdtemp(prefix="odmlconv", dir="/home/msonntag/Chaos/DL/odmlconvdir")
    rdir = tempfile.mkdtemp(prefix="odmlrdf", dir=tdir)

    print("Files will be saved to '%s'" % tdir)


if __name__ == "__main__":
    main(sys.argv[1:])

