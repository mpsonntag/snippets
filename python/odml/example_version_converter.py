import os
import odml.tools as oto

from odml.tools.version_converter import VersionConverter

wdir = "/home/msonntag/Chaos/work/x_odml/file_dump"
fn = "1.3.3_convert%s.xml"
fin = fn % ""
fout = fn % "_converted"

# Conversion of odML v1 to v1.1
vc = VersionConverter(os.path.join(wdir, fin))

# either write to file
print("Converting '%s' ..." % vc.filename)
vc.write_to_file(os.path.join(wdir, fout))

# or pass it to the python xml parser
doc = oto.odmlparser.ODMLReader(parser='XML').from_string(str(vc))
