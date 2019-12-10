"""
This file provides examples how to convert odml files between versions and formats.
"""

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

    f_in_short = join(FOLDER_OUT, "%s_v1.0.xml" % BASE_EXAMPLE_SHORT)
    f_out_rdf_short = join(FOLDER_RDF, "%s.ttl" % BASE_EXAMPLE_SHORT)

    f_in = join(FOLDER_OUT, "%s_v1.0.xml" % BASE_EXAMPLE)
    f_out_rdf = join(FOLDER_RDF, "%s.ttl" % BASE_EXAMPLE)

    # write v1.1 to RDF
    # Works only for v1.1 files; convert from v1.0 to v1.1 first if required.
    doc = ODMLReader(parser='XML').from_file(open(f_in))
    rdf_writer = RDFWriter(doc)
    rdf_writer.write_file(f_out_rdf, "turtle")

    doc = ODMLReader(parser='XML').from_file(open(f_in_short))
    rdf_reader = RDFWriter(doc)
    rdf_reader.write_file(f_out_rdf_short, "turtle")


def read_write():
    """
    Basic reading and writing of odml documents
    """
    f_in = join(ROOT, "%s_v1.0.xml" % BASE_EXAMPLE)
    f_out = join(FOLDER_OUT, "%s_v1.1.xml" % BASE_EXAMPLE)

    # read in odML document
    doc = ODMLReader(parser='XML').from_file(open(f_in))

    # parse to format
    o_writer = ODMLWriter(parser='XML')
    o_writer.write_file(doc, f_out)


def write_rdf():
    """
    Read an XML odml file and convert it to an RDF file
    """
    f_in = join(ROOT, "%s_v1.0.xml" % BASE_EXAMPLE_SHORT)
    f_out_rdf = join(FOLDER_RDF, "%s.ttl" % BASE_EXAMPLE_SHORT)

    doc = ODMLReader(parser='XML').from_file(open(f_in))
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
