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

# Section type term defined in odml/resources/section_subclasses.yaml that will
# be converted to an RDF Section Subclass of Class "Cell".
sub_class_term = "cell"

# Create minimal document
doc = odml.Document()
_ = odml.Section(name="test_subclassing", type=sub_class_term, parent=doc)

# Test None dict
rdf_writer = RDFWriter([doc], custom_subclasses=None)
print(rdf_writer.get_rdf_str())
assert "odml:Cell" in rdf_writer.get_rdf_str()

# Test invalid dict
rdf_writer = RDFWriter([doc], custom_subclasses=["invalid"])
print(rdf_writer.get_rdf_str())
assert "odml:Cell" in rdf_writer.get_rdf_str()

# Test value whitespace
invalid_dict = {"type_1": "Class 1", "type_2": "Class 2"}
rdf_writer = RDFWriter([doc], custom_subclasses=invalid_dict)

# Test custom subclassing
type_custom_class = "species"
custom_class_dict = {type_custom_class: "Species"}

doc = odml.Document()
_ = odml.Section(name="test_subclassing", type="cell", parent=doc)
_ = odml.Section(name="test_custom_subclassing", type=type_custom_class, parent=doc)

rdf_writer = RDFWriter([doc], custom_subclasses=custom_class_dict)
print(rdf_writer.get_rdf_str())
assert "odml:Cell" in rdf_writer.get_rdf_str()
assert "odml:Species" in rdf_writer.get_rdf_str()

# Test custom subclassing overwrite
sub_class_type = "cell"
custom_class_dict = {sub_class_type: "Neuron"}

doc = odml.Document()
_ = odml.Section(name="test_subclassing", type=sub_class_type, parent=doc)

rdf_writer = RDFWriter([doc], custom_subclasses=custom_class_dict)
print(rdf_writer.get_rdf_str())
assert "odml:Cell" not in rdf_writer.get_rdf_str()
assert "odml:Neuron" in rdf_writer.get_rdf_str()

# Test lower case value
custom_class_dict = {sub_class_type: "neuron"}
rdf_writer = RDFWriter([doc], custom_subclasses=custom_class_dict)
print(rdf_writer.get_rdf_str())
