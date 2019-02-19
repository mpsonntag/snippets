import odml.tools as oto

main = "/home/msonntag/Chaos/DL/conv/"
folder_v1_0 = main
folder_v1_1 = main + "out/"
folder_rdf = main + "rdf/"

# Conversion of v1.0 to v1.1 files
# Will overwrite existing files
fc = oto.format_converter.FormatConverter()
fc.convert_dir(folder_v1_0, folder_v1_1, False, "v1_1")

fname_short = folder_v1_1 + "spikeLFP_metadata080707_short_v1.0.xml"
frdf_short = folder_rdf +"spikeLFP_metadata080707_short.ttl"

fname = folder_v1_1 + "spikeLFP_metadata080707_v1.0.xml"
frdf = folder_rdf +"spikeLFP_metadata080707.ttl"

# write v1.1 to RDF
# Works only for v1.1 files; convert from v1.0 to v1.1 first if required.
doc = oto.odmlparser.ODMLReader(parser='XML').fromFile(open(fname))
f = oto.rdf_converter.RDFWriter(doc)
f.write_file(frdf, "turtle")

doc = oto.odmlparser.ODMLReader(parser='XML').fromFile(open(fname_short))
f = oto.rdf_converter.RDFWriter(doc)
f.write_file(frdf_short, "turtle")

# -------------------------

# Reading and writing documents

fname = "spikeLFP_metadata080707_v1.0.xml"
fout = "spikeLFP_metadata080707_v1.1.xml"

# read in odML document
doc = oto.odmlparser.ODMLReader(parser='XML').fromFile(open(fname))

# parse to format
w = oto.odmlparser.ODMLWriter(parser='XML')
w.write_file(doc, fout)

# -------------------------

import odml.tools as oto

main = "/home/msonntag/Chaos/DL/conv/"
folder_v1_0 = main
folder_v1_1 = main + "out/"
folder_rdf = main + "rdf/"

fname_short = folder_v1_1 + "spikeLFP_metadata080707_short_v1.0.xml"
frdf_short = folder_rdf +"spikeLFP_metadata080707_short.ttl"

doc = oto.odmlparser.ODMLReader(parser='XML').fromFile(open(fname_short))
f = oto.rdf_converter.RDFWriter(doc)
f.write_file(frdf_short, "turtle")

# -------------------------
    
import odml.tools as oto

main = "/home/msonntag/Chaos/DL/conv/"
fin = main +"tmp.xml"
fout = main+"tmpout.xml"

vc = oto.version_converter.VersionConverter(fin)

# either write to file
vc.write_to_file(fout)

# or pass it to the python xml parser
doc = oto.odmlparser.ODMLReader(parser='XML').from_string(str(vc))




