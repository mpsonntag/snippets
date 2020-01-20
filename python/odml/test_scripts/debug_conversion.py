import os

import odml
from odml.tools.version_converter import VersionConverter as VC

root = os.path.join(os.environ['HOME'], 'Chaos', 'DL', 'x_odml', 'convert')

"""
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
"""

tiny = os.path.join(root, '1.3_tiny.xml')
out_tiny = os.path.join(root, '1.4_tiny.xml')

conv = VC(tiny)
conv.write_to_file(out_tiny)

tdoc = odml.load(out_tiny)

print("\n---- converted values -----")
props = tdoc.sections[0].properties
for p in props:
    print("%s \n\t--- '%s'" % (p.value, p.value[0]))

odml.save(tdoc, out_tiny)
tdoc = odml.load(out_tiny)

print("\n---- saved and loaded values -----")
props = tdoc.sections[0].properties
for p in props:
    print("%s \n\t--- '%s'" % (p.value, p.value[0]))

odml.Property(name="testAddSingleStringValue", value="d, e, f", parent=tdoc.sections[0])
odml.Property(name="testAddStringListWS", value=[" some ", " more ", " strings "], parent=tdoc.sections[0])
odml.Property(name="testAddIntList", value=[1, 2, 3], parent=tdoc.sections[0])

odml.save(tdoc, out_tiny)

odml.save(tdoc, ("%s.json" % out_tiny), "JSON")
odml.save(tdoc, ("%s.yaml" % out_tiny), "YAML")

xdoc = odml.load(out_tiny)
jdoc = odml.load(("%s.json" % out_tiny), "JSON")
ydoc = odml.load(("%s.yaml" % out_tiny), "YAML")

print("\n---- saved and loaded values, 2nd save -----")
print("\nJSON equal: %s" % (tdoc == jdoc))
props = jdoc.sections[0].properties
for p in props:
    print("%s \n\t--- '%s'" % (p.value, p.value[0]))

print("\nXML equal: %s" % (tdoc == xdoc))
props = xdoc.sections[0].properties
for p in props:
    print("%s \n\t--- '%s'" % (p.value, p.value[0]))

print("\nYAML equal: %s" % (tdoc == ydoc))
props = ydoc.sections[0].properties
for p in props:
    print("%s \n\t--- '%s'" % (p.value, p.value[0]))


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
