import os
import odml

workdir = "/home/msonntag/Chaos/work/x_testodml"
fn = "1.4_testfile.%s"

print("Version '%s'\nInstalled at '%s'\n" % (odml.__version__, odml.__file__))

print("Create document\n")
doc = odml.Document(author="HPL")
sec = odml.Section(name="sec", parent=doc)
prop = odml.Property(name="prop", parent=sec)
subsec1 = odml.Section(name="subsec", parent=sec)
subsec2 = odml.Section(parent=sec)

print("Saving document\n%s\n" % doc)
odml.save(doc, os.path.join(workdir, (fn % 'x')))
odml.save(doc, os.path.join(workdir, (fn % 'j')), 'JSON')
odml.save(doc, os.path.join(workdir, (fn % 'r')), 'RDF')
odml.save(doc, os.path.join(workdir, (fn % 'y')), 'YAML')

print("Loading document\n")
xdoc = odml.load(os.path.join(workdir, (fn % 'x')))
jdoc = odml.load(os.path.join(workdir, (fn % 'j')), 'JSON')
ydoc = odml.load(os.path.join(workdir, (fn % 'y')), 'YAML')
rdoc = odml.tools.odmlparser.ODMLReader('RDF').from_file(os.path.join(workdir, (fn % 'r')), 'turtle')[0]

print("Testing equality\n")
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

print("Test loading complex files")
xdoc = odml.load(os.path.join(workdir, ''))


