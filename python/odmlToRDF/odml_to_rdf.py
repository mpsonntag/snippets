"""
This file provides examples how to convert odml files between versions and formats.
"""
import argparse
import sys

from os.path import join

from odml.tools import ODMLReader, ODMLWriter, RDFWriter
from odml.tools.converters import FormatConverter, VersionConverter

ROOT = "/home/msonntag/Chaos/DL/conv/"
FOLDER_OUT = join(ROOT, "out")
FOLDER_RDF = join(ROOT, "rdf")
BASE_EXAMPLE = "spikeLFP_metadata080707"
BASE_EXAMPLE_SHORT = "spikeLFP_metadata080707_short"


def update_write_rdf():
    """
    Conversion of odml v1.0 to v1.1 files and export to RDF.
    Will overwrite existing files.
    """
    o_ver_conv = FormatConverter()
    o_ver_conv.convert_dir(ROOT, FOLDER_OUT, False, "v1_1")

    f_in_short = join(FOLDER_OUT, f"{BASE_EXAMPLE_SHORT}_v1.0.xml")
    f_out_rdf_short = join(FOLDER_RDF, f"{BASE_EXAMPLE_SHORT}.ttl")

    f_in = join(FOLDER_OUT, f"{BASE_EXAMPLE}_v1.0.xml")
    f_out_rdf = join(FOLDER_RDF, f"{BASE_EXAMPLE}.ttl")

    # write v1.1 to RDF
    # Works only for v1.1 files; convert from v1.0 to v1.1 first if required.
    doc = ODMLReader(parser='XML').from_file(f_in)
    rdf_writer = RDFWriter(doc)
    rdf_writer.write_file(f_out_rdf, "turtle")

    doc = ODMLReader(parser='XML').from_file(f_in_short)
    rdf_reader = RDFWriter(doc)
    rdf_reader.write_file(f_out_rdf_short, "turtle")


def read_write():
    """
    Basic reading and writing of odml documents
    """
    f_in = join(ROOT, f"{BASE_EXAMPLE}_v1.0.xml")
    f_out = join(FOLDER_OUT, f"{BASE_EXAMPLE}_v1.1.xml")

    # read in odML document
    doc = ODMLReader(parser='XML').from_file(f_in)

    # parse to format
    o_writer = ODMLWriter(parser='XML')
    o_writer.write_file(doc, f_out)


def write_rdf():
    """
    Read an XML odml file and convert it to an RDF file
    """
    f_in = join(ROOT, f"{BASE_EXAMPLE_SHORT}_v1.0.xml")
    f_out_rdf = join(FOLDER_RDF, f"{BASE_EXAMPLE_SHORT}.ttl")

    doc = ODMLReader(parser='XML').from_file(f_in)
    rdf_writer = RDFWriter(doc)
    rdf_writer.write_file(f_out_rdf, "turtle")


def convert_odml():
    """
    Convert a v1.0 odml file to a v1.1 file or pass it to an in memory odml document
    """
    f_in = join(ROOT, "tmp.xml")
    f_out = join(ROOT, "tmpout.xml")

    o_ver_conv = VersionConverter(f_in)

    # either write to file
    o_ver_conv.write_to_file(f_out)

    # or pass it to the python xml parser
    doc = ODMLReader(parser='XML').from_string(str(o_ver_conv))
    doc.pprint()


def main():
    """
    Parse command line arguments and call the corresponding odml to RDF function.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upgrade", dest="upgrade", action="store_true",
                        help="Upgrade an odml file to the latest version and save as XML")
    parser.add_argument("--upgrade-print", dest="upgrade_print", action="store_true",
                        help="Upgrade an odml file to the latest version and "
                             "print the content")
    parser.add_argument("--upgrade-rdf", dest="upgrade_rdf", action="store_true",
                        help="Upgrade an odml file to the latest version and save as RDF")
    args = parser.parse_args()
    upgrade = args.upgrade
    upgrade_print = args.upgrade_print
    upgrade_rdf = args.upgrade_rdf

    if upgrade:
        read_write()
        sys.exit(0)

    if upgrade_print:
        convert_odml()
        sys.exit(0)

    if upgrade_rdf:
        update_write_rdf()
        sys.exit(0)

    write_rdf()


if __name__ == "__main__":
    main()
