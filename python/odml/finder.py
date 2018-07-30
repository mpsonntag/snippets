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
import odml
import pathlib
import sys
import tempfile

from docopt import docopt
from odml.tools.version_converter import VersionConverter as VerConf
from odml.tools.odmlparser import ODMLReader, ODMLWriter


def run_rdf_conversion(infile, dir):
    outname = os.path.splitext(os.path.basename(infile))[0]
    outfile = os.path.join(dir, "%s.rdf" % outname)
    doc = ODMLReader().from_file(infile)
    ODMLWriter("RDF").write_file(doc, outfile)


def run_version_conversion(flist, convdir, rdir, source_backend="XML"):
    for f in flist:
        infile = str(f.absolute())
        print("Handling file '%s'" % infile)
        try:
            odml.load(infile, source_backend)
            print("RDF conversion of '%s'" % infile)
            run_rdf_conversion(infile, rdir)
        except Exception:
            outname = os.path.splitext(os.path.basename(infile))[0]
            outfile = os.path.join(convdir, "%s_conv.xml" % outname)
            try:
                _ = VerConf(infile).write_to_file(outfile, source_backend)
                try:
                    print("RDF conversion of '%s'" % outfile)
                    run_rdf_conversion(outfile, rdir)
                except Exception as e:
                    print("[Error] converting '%s' to RDF: '%s'" % (infile, str(e)))
            except Exception as e:
                # Ignore files we cannot parse or convert
                print("[Error] version converting file '%s': '%s'" % (infile, str(e)))


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

    root = None
    if parser["-o"] and os.path.isdir(parser["-o"]):
        root = parser["-o"]
    tdir = tempfile.mkdtemp(prefix="odmlconv_", dir=root)
    rdir = tempfile.mkdtemp(prefix="odmlrdf_", dir=tdir)

    print("Files will be saved to '%s'" % tdir)

    run_version_conversion(xfiles, tdir, rdir)
    run_version_conversion(jfiles, tdir, rdir, "JSON")
    run_version_conversion(yfiles, tdir, rdir, "YAML")


if __name__ == "__main__":
    main(sys.argv[1:])

