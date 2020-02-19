import sys
import unittest

try:
    # Test possible imports of all parsers without importing the full odML package
    from odml.tools import ODMLReader, ODMLWriter, RDFReader, RDFWriter
    from odml.tools.converters import FormatConverter, VersionConverter
    from odml.tools import XMLReader, XMLWriter, DictReader, DictWriter

    import odml
except Exception as exc:
    print("-- Failed on an import: %s" % exc)
    sys.exit(-1)


class TestODMLBasics(unittest.TestCase):

    def testLoad(self):
        print("-- Load odml xml file")
        doc = odml.load('./load.odml.xml')
        print(doc.pprint())

    def testVersionLoad(self):
        print("-- Test invalid version exception xml file load")
        with self.assertRaises(odml.tools.parser_utils.InvalidVersionException):
            _ = odml.load('./load_v1.odml.xml')


if __name__ == "__main__":
    try:
        unittest.main()

    except Exception as exc:
        print("-- Failed on a test: %s" % exc)
        sys.exit(-1)
