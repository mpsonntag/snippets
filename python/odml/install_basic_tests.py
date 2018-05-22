import os
import sys

import odml

from odml.tools.version_converter import VersionConverter

WORKDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources")


def run():
    slf = "save_load"
    new_fn_base = "1.4_testfile.%s"

    convdir = "convert"
    conv_fn_base = "1.3_convert.%s"

    compdir = "complex"
    comp_fn_base = "1.4_example.%s"

    print("Testing odML version\t'%s'" % odml.__version__)
    print("Installed at\t\t'%s'" % odml.__file__)
    print("Working in directory\t'%s'" % WORKDIR)
    print("Python version:\t\t'%s.%s.%s'" % (sys.version_info.major,
                                             sys.version_info.minor,
                                             sys.version_info.micro))

    print("\n\n-- Create document")
    doc = odml.Document(author="HPL")
    sec = odml.Section(name="sec", parent=doc)
    prop = odml.Property(name="prop", parent=sec)
    subsec = odml.Section(name="subsec", parent=sec)
    _ = odml.Section(parent=sec)
    print(doc)

    print("\n\n-- Saving document ...")
    odml.save(doc, os.path.join(WORKDIR, slf, (new_fn_base % 'x')))
    odml.save(doc, os.path.join(WORKDIR, slf, (new_fn_base % 'j')), 'JSON')
    odml.save(doc, os.path.join(WORKDIR, slf, (new_fn_base % 'r')), 'RDF')
    odml.save(doc, os.path.join(WORKDIR, slf, (new_fn_base % 'y')), 'YAML')
    print("-- Done...")

    print("\n-- Loading document ...")
    xdoc = odml.load(os.path.join(WORKDIR, slf, (new_fn_base % 'x')))
    jdoc = odml.load(os.path.join(WORKDIR, slf, (new_fn_base % 'j')), 'JSON')
    ydoc = odml.load(os.path.join(WORKDIR, slf, (new_fn_base % 'y')), 'YAML')
    rdoc = odml.tools.odmlparser.ODMLReader('RDF').from_file(
        os.path.join(WORKDIR, slf, (new_fn_base % 'r')), 'turtle')[0]
    print("-- Done...")

    print("\n\n-- Testing equality ...")
    assert doc == xdoc
    assert doc == jdoc
    #assert doc == rdoc
    assert doc == ydoc

    assert sec == xdoc[0]
    assert sec == jdoc[0]
    #assert sec == rdoc[0]
    assert sec == ydoc[0]

    assert subsec == xdoc[0][0]
    assert subsec == jdoc[0][0]
    assert subsec == rdoc[0]["subsec"]
    assert subsec == ydoc[0][0]

    assert prop == xdoc[0].properties[0]
    assert prop == jdoc[0].properties[0]
    assert prop == rdoc[0].properties[0]
    assert prop == ydoc[0].properties[0]
    print("-- Done...")

    print("\n\n-- Test complex file loading ...")
    print("XML:\t%s" % odml.load(os.path.join(WORKDIR, compdir, (comp_fn_base % 'xml'))))
    print("JSON:\t%s" % odml.load(os.path.join(WORKDIR, compdir, (comp_fn_base % 'json')), 'JSON'))
    print("YAML:\t%s" % odml.load(os.path.join(WORKDIR, compdir, (comp_fn_base % 'yaml')), 'YAML'))

    print("\n\n-- Test format conversion from XML ...")
    conv_file = conv_fn_base % "xml"
    _ = VersionConverter(
        os.path.join(WORKDIR, convdir, conv_file)).write_to_file(
            os.path.join(WORKDIR, convdir, "1.4__%s" % conv_file))

    print("\n-- Test format conversion from JSON ...")
    conv_file = conv_fn_base % "json"
    _ = VersionConverter(
        os.path.join(WORKDIR, convdir, conv_file)).write_to_file(
            os.path.join(WORKDIR, convdir, "1.4__%s" % conv_file), 'JSON')

    print("\n-- Test format conversion from YAML ...")
    conv_file = conv_fn_base % "yaml"
    _ = VersionConverter(
        os.path.join(WORKDIR, convdir, conv_file)).write_to_file(
            os.path.join(WORKDIR, convdir, "1.4__%s" % conv_file), 'YAML')

    print("\n-- Done ...\n")


if len(sys.argv) == 2:
    if not os.path.isdir(sys.argv[1]):
        print("Cannot access directory '%s'\n" % sys.argv[1])
        quit()

    print("Using base path '%s'\n" % sys.argv[1])
    WORKDIR = sys.argv[1]

else:
    print("Using default path '%s'\n" % WORKDIR)

run()
