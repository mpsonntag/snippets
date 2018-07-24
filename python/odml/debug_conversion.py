import os

import odml
from odml.tools.version_converter import VersionConverter as VC

root = os.path.join(os.environ['HOME'], 'Chaos', 'DL', 'x_odml', 'convert')

conv_no_enc = os.path.join(root, '1.3_convert.xml')
out_noenc = os.path.join(root, '1.4_converted_noenc.xml')

conv_utf8 = os.path.join(root, '1.3_convert_utf8.xml')
out_utf8 = os.path.join(root, '1.4_converted_utf8.xml')

# Convert no encoding
conv = VC(conv_no_enc)
conv.write_to_file(out_noenc)

vdoc = odml.load(out_noenc)


# Convert utf8 encoding in xml header
conv = VC(conv_utf8)
conv.write_to_file(out_utf8)

vudoc = odml.load(out_utf8)
