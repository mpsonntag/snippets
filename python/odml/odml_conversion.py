import odml.tools as oto

main = "/home/msonntag/Chaos/DL/conv/"
fin = main +"tmp.xml"
fout = main+"tmpout.xml"

# Conversion of odML v1 to v1.1
vc = oto.version_converter.VersionConverter(fin)

# either write to file
vc.write_to_file(fout)

# or pass it to the python xml parser
doc = oto.odmlparser.ODMLReader(parser='XML').from_string(str(vc))
