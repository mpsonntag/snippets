import os
import odml.tools as oto

wdir = "/home/msonntag/Chaos/work/x_odml/file_dump/conv"
folder_v1_1 = os.path.join(wdir, "out")

# Conversion of v1.0 to v1.1 files
# Will overwrite existing files
fc = oto.format_converter.FormatConverter()
fc.convert_dir(wdir, folder_v1_1, False, "v1_1")

