import odml

from odml.tools import RDFWriter

# Section type term defined in odml/resources/section_subclasses.yaml that will
# be converted to an RDF Section Subclass of Class "Cell".
sub_class_term = "cell"

# Create minimal document
doc = odml.Document()
_ = odml.Section(name="test_subclassing", type=sub_class_term, parent=doc)

# Test default subclassing
print("-- Default behavior")
rdf_writer = RDFWriter([doc])
print(rdf_writer.get_rdf_str())

# Test inactivation of subclassing feature
print("-- Inactivation")
rdf_writer = RDFWriter([doc], rdf_subclassing=False)
print(rdf_writer.get_rdf_str())
