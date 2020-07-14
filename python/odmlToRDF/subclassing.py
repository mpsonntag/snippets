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


# Test subclassing queries

import odml

from odml.tools import RDFWriter
from odml.tools.rdf_converter import ODML_NS

from owlrl import DeductiveClosure, RDFS_Semantics

from rdflib import Namespace, RDF, RDFS
from rdflib.plugins.sparql import prepareQuery

NAMESPACE_MAP = {"odml": Namespace(ODML_NS), "rdf": RDF, "rdfs": RDFS}

# -- Test default subclassing
doc = odml.Document()
_ = odml.Section(name="test_subclass", type="cell", parent=doc)
_ = odml.Section(name="test_regular_class", type="regular", parent=doc)

rdf_writer = RDFWriter([doc])
_ = rdf_writer.get_rdf_str()

use_graph = rdf_writer.graph
DeductiveClosure(RDFS_Semantics).expand(use_graph)

q_string = "SELECT * WHERE {?s rdf:type odml:Section .}"
curr_query = prepareQuery(q_string, initNs=NAMESPACE_MAP)

# Make sure the query finds two sections
assert len(use_graph.query(curr_query)) == 2

# Make sure the query finds
result_section = []
for row in use_graph.query(curr_query):
    result_section.append(row.s)

q_string = "SELECT * WHERE {?s rdf:type odml:Cell .}"
curr_query = prepareQuery(q_string, initNs=NAMESPACE_MAP)

assert len(use_graph.query(curr_query)) == 1
for row in use_graph.query(curr_query):
    assert row.s in result_section

# -- Test custom subclassing
type_custom_class = "species"
type_overwrite_class = "cell"
custom_class_dict = {type_custom_class: "Species", type_overwrite_class: "Neuron"}

doc = odml.Document()
sec = odml.Section(name="test_subclass", type="species", parent=doc)
_ = odml.Section(name="test_subclass_overwrite", type="cell", parent=sec)
_ = odml.Section(name="test_regular_class", type="regular", parent=sec)

rdf_writer = RDFWriter([doc], custom_subclasses=custom_class_dict)
_ = rdf_writer.get_rdf_str()

use_graph = rdf_writer.graph
DeductiveClosure(RDFS_Semantics).expand(use_graph)

q_string = "SELECT * WHERE {?s rdf:type odml:Section .}"
curr_query = prepareQuery(q_string, initNs=NAMESPACE_MAP)

# Make sure the query finds three sections
assert len(use_graph.query(curr_query)) == 3

# Make sure the query finds
result_section = []
for row in use_graph.query(curr_query):
    result_section.append(row.s)

# Custom class 'Species' should be found.
q_string = "SELECT * WHERE {?s rdf:type odml:Species .}"
curr_query = prepareQuery(q_string, initNs=NAMESPACE_MAP)

assert len(use_graph.query(curr_query)) == 1
for row in use_graph.query(curr_query):
    assert row.s in result_section

# Custom class 'Neuron' should be found.
q_string = "SELECT * WHERE {?s rdf:type odml:Neuron .}"
curr_query = prepareQuery(q_string, initNs=NAMESPACE_MAP)

assert len(use_graph.query(curr_query)) == 1
for row in use_graph.query(curr_query):
    assert row.s in result_section

# Default class 'Cell' was replaced and should not return any result.
q_string = "SELECT * WHERE {?s rdf:type odml:Cell .}"
curr_query = prepareQuery(q_string, initNs=NAMESPACE_MAP)

assert len(use_graph.query(curr_query)) == 0

# -- Test inactivated subclassing
doc = odml.Document()
_ = odml.Section(name="test_regular_class", type="regular", parent=doc)
_ = odml.Section(name="test_subclass", type="cell", parent=doc)

rdf_writer = RDFWriter([doc], rdf_subclassing=False)
_ = rdf_writer.get_rdf_str()

use_graph = rdf_writer.graph
DeductiveClosure(RDFS_Semantics).expand(use_graph)

q_string = "SELECT * WHERE {?s rdf:type odml:Section .}"
curr_query = prepareQuery(q_string, initNs=NAMESPACE_MAP)

assert len(use_graph.query(curr_query)) == 2

q_string = "SELECT * WHERE {?s rdf:type odml:Cell .}"
curr_query = prepareQuery(q_string, initNs=NAMESPACE_MAP)

assert len(use_graph.query(curr_query)) == 0

# -- Test Subclass definition entry


