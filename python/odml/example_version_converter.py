import os
import odml.tools as oto

from odml.tools.version_converter import VersionConverter

wdir = "/home/msonntag/Chaos/work/x_odml/file_dump"
fin = os.path.join(wdir, ()) "" main +"tmp.xml"
fout = main+"tmpout.xml"

# Conversion of odML v1 to v1.1
vc = VersionConverter(fin)

# either write to file
print("Converting '%s' ..." % vc.filename)
vc.write_to_file(fout)

# or pass it to the python xml parser
doc = oto.odmlparser.ODMLReader(parser='XML').from_string(str(vc))
