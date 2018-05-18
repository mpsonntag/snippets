import odml.tools as oto

main = "/home/msonntag/Chaos/DL/conv/"
folder_v1_0 = main
folder_v1_1 = main + "out/"
folder_rdf = main + "rdf/"

fname_short = folder_v1_1 + "spikeLFP_metadata080707_short_v1.0.xml"
frdf_short = folder_rdf +"spikeLFP_metadata080707_short.ttl"

# requires odML v1.1 files
doc = oto.odmlparser.ODMLReader(parser='XML').fromFile(open(fname_short))
f = oto.rdf_converter.RDFWriter(doc)
f.write_file(frdf_short, "turtle")

