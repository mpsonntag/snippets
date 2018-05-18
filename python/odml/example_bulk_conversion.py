import odml.tools as oto

main = "/home/msonntag/Chaos/DL/conv/"
folder_v1_0 = main
folder_v1_1 = main + "out/"

# Conversion of v1.0 to v1.1 files
# Will overwrite existing files
fc = oto.format_converter.FormatConverter()
fc.convert_dir(folder_v1_0, folder_v1_1, False, "v1_1")

