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

tiny = os.path.join(root, '1.3_tiny.xml')
out_tiny = os.path.join(root, '1.4_tiny.xml')

conv = VC(tiny)
conv.write_to_file(out_tiny)

tdoc = odml.load(out_tiny)

print("---- converted values -----")
print(tdoc.sections[0].properties[0].value)
print(tdoc.sections[0].properties[0].value[0])
print(tdoc.sections[0].properties[1].value)
print(tdoc.sections[0].properties[1].value[0])

odml.save(tdoc, out_tiny)
tdoc = odml.load(out_tiny)

print("---- saved and loaded values -----")
print(tdoc.sections[0].properties[0].value)
print(tdoc.sections[0].properties[0].value[0])
print(tdoc.sections[0].properties[1].value)
print(tdoc.sections[0].properties[1].value[0])

odml.Property(name="3", value="d, e, f", parent=tdoc.sections[0])
odml.Property(name="4", value=["sfasdf","asdffgh"], parent=tdoc.sections[0])
odml.Property(name="5", value=[1,2,3], parent=tdoc.sections[0])

odml.save(tdoc, out_tiny)

odml.save(tdoc, ("%s.json" % out_tiny), "JSON")
odml.save(tdoc, ("%s.yaml" % out_tiny), "YAML")

xdoc = odml.load(out_tiny)
jdoc = odml.load(("%s.json" % out_tiny), "JSON")
ydoc = odml.load(("%s.yaml" % out_tiny), "YAML")

print("---- saved and loaded values -----")
print("\nJSON equal: %s" % (tdoc == jdoc))
print(jdoc.sections[0].properties[0].value)
print(jdoc.sections[0].properties[1].value)
print(jdoc.sections[0].properties[2].value)
print(jdoc.sections[0].properties[3].value)
print(jdoc.sections[0].properties[4].value)

print("\nXML equal: %s" % (tdoc == xdoc))
print(xdoc.sections[0].properties[0].value)
print(xdoc.sections[0].properties[1].value)
print(xdoc.sections[0].properties[2].value)
print(xdoc.sections[0].properties[3].value)
print(xdoc.sections[0].properties[4].value)

print("\nYAML equal: %s" % (tdoc == ydoc))
print(ydoc.sections[0].properties[0].value)
print(ydoc.sections[0].properties[1].value)
print(ydoc.sections[0].properties[2].value)
print(ydoc.sections[0].properties[3].value)
print(ydoc.sections[0].properties[4].value)


"""
doc = odml.Document()
sec = odml.Section(name='bla')
sec = odml.Section(name='bla', parent=doc)
prop = odml.Property(name="1", value="a", parent=sec)
prop = odml.Property(name="2", value=["b", "c"], parent=sec)
odml.save(doc, out_tiny)
prop = odml.Property(name="3", value="d, e, f", parent=sec)
odml.save(doc, out_tiny)
blargh = odml.load(out_tiny)
"""
