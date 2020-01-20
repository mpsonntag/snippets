import os
import odml.tools as oto

wdir = "/home/msonntag/Chaos/work/x_odml/file_dump/conv"
folder_v1_1 = os.path.join(wdir, "out")
folder_rdf = os.path.join(wdir, "rdf")

fname_short = os.path.join(folder_v1_1, "spikeLFP_metadata080707_short_v1.0.xml")
frdf_short = os.path.join(folder_rdf, "spikeLFP_metadata080707_short.ttl")

# requires odML v1.1 files
doc = oto.odmlparser.ODMLReader(parser='XML').from_file(fname_short)
f = oto.rdf_converter.RDFWriter(doc)
f.write_file(frdf_short, "turtle")
