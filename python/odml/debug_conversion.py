import os

import odml
from odml.tools.version_converter import VersionConverter as VC

root = os.path.join(os.environ['HOME'], 'Chaos', 'DL', 'x_odml', 'convert')

conv_no_enc = os.path.join(root, '1.3_convert.xml')
conv_utf8 = os.path.join(root, '1.3_convert_utf8.xml')

out_noenc = os.path.join(root, '1.4_converted_noenc.xml')
out_utf8 = os.path.join(root, '1.4_converted_utf8.xml')

print("%s, %s, %s, %s" % (conv_no_enc, conv_utf8, out_noenc, out_utf8))

