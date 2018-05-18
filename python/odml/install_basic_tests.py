import os
import odml

from odml.tools.version_converter import VersionConverter

workdir = "/home/msonntag/Chaos/work/x_odml"
slf = "save_load"
new_fn_base = "1.4_testfile.%s"

convdir = "convert"
conv_fn_base = "1.3_convert.%s"

compdir = "complex"
comp_fn_base = "1.4_example.%s"

print("Version '%s'\nInstalled at '%s'\n" % (odml.__version__, odml.__file__))

print("Working in directory '%s'\n" % workdir)

print("\nCreate document\n")
doc = odml.Document(author="HPL")
sec = odml.Section(name="sec", parent=doc)
prop = odml.Property(name="prop", parent=sec)
subsec1 = odml.Section(name="subsec", parent=sec)
subsec2 = odml.Section(parent=sec)

print("\nSaving document\n%s\n" % doc)
odml.save(doc, os.path.join(workdir, slf, (new_fn_base % 'x')))
odml.save(doc, os.path.join(workdir, slf, (new_fn_base % 'j')), 'JSON')
odml.save(doc, os.path.join(workdir, slf, (new_fn_base % 'r')), 'RDF')
odml.save(doc, os.path.join(workdir, slf, (new_fn_base % 'y')), 'YAML')

print("\nLoading document\n")
xdoc = odml.load(os.path.join(workdir, slf, (new_fn_base % 'x')))
jdoc = odml.load(os.path.join(workdir, slf, (new_fn_base % 'j')), 'JSON')
ydoc = odml.load(os.path.join(workdir, slf, (new_fn_base % 'y')), 'YAML')
rdoc = odml.tools.odmlparser.ODMLReader('RDF').from_file(os.path.join(workdir, slf, (new_fn_base % 'r')), 'turtle')[0]

print("\nTesting equality\n")
assert(doc == xdoc)
assert(doc == jdoc)
#assert(doc == rdoc)
assert(doc == ydoc)

assert(sec == xdoc[0])
assert(sec == jdoc[0])
#assert(sec == rdoc[0])
assert(sec == ydoc[0])

assert(subsec1 == xdoc[0][0])
assert(subsec1 == jdoc[0][0])
assert(subsec1 == rdoc[0]["subsec"])
assert(subsec1 == ydoc[0][0])

assert(prop == xdoc[0].properties[0])
assert(prop == jdoc[0].properties[0])
assert(prop == rdoc[0].properties[0])
assert(prop == ydoc[0].properties[0])

print("\nTest complex file load from XML\n")
print(odml.load(os.path.join(workdir, compdir, (comp_fn_base % 'xml'))))

print("\nTest complex file load from JSON\n")
print(odml.load(os.path.join(workdir, compdir, (comp_fn_base % 'json')), 'JSON'))

print("\nTest complex file load from YAML\n")
print(odml.load(os.path.join(workdir, compdir, (comp_fn_base % 'yaml')), 'YAML'))

print("\nTest format conversion from XML\n")
conv_file = conv_fn_base % "xml"
_ = VersionConverter(
    os.path.join(workdir, convdir, conv_file)).write_to_file(
    os.path.join(workdir, convdir, "1.4_%s" % conv_file))

print("\nTest format conversion from JSON\n")
conv_file = conv_fn_base % "json"
_ = VersionConverter(
    os.path.join(workdir, convdir, conv_file)).write_to_file(
    os.path.join(workdir, convdir, "1.4_%s" % conv_file), 'JSON')

print("\nTest format conversion from YAML\n")
conv_file = conv_fn_base % "yaml"
_ = VersionConverter(
    os.path.join(workdir, convdir, conv_file)).write_to_file(
    os.path.join(workdir, convdir, "1.4_%s" % conv_file), 'YAML')

print("\nDone...\n")
