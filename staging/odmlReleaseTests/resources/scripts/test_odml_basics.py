# Test possible imports of all parsers without importing the full odML package
from odml.tools import ODMLReader, ODMLWriter, RDFReader, RDFWriter
from odml.tools.converters import FormatConverter, VersionConverter
from odml.tools import XMLReader, XMLWriter, DictReader, DictWriter
import odml

print("\nLoading odml document")
doc = odml.load('./load.odml.xml')

doc.pprint()

print("\nLoading previous version odml document")
try:
    doc = odml.load('./load_v1.odml.xml')
except odml.tools.parser_utils.InvalidVersionException as exc:
    print("\n Could not load file: %s" % exc)
