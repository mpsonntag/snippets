from rdflib import Graph, Namespace, RDF, RDFS
from rdflib.plugins.sparql import prepareQuery

from owlrl import DeductiveClosure, RDFS_Semantics

import odml

from odml.tools import RDFWriter
from odml.tools.rdf_converter import ODML_NS

NAMESPACE_MAP = {"odml": Namespace(ODML_NS), "rdf": RDF, "rdfs": RDFS}

doc = odml.Document()
_ = odml.Section(name="test_cell", type="cell", parent=doc)
_ = odml.Section(name="test_desc", type="datacite/description", parent=doc)

rdf_writ = RDFWriter([doc])

curr_graph = rdf_writ.graph

DeductiveClosure(RDFS_Semantics).expand(curr_graph)

q_string = "SELECT * WHERE {?s rdf:type odml:Cell .}"
curr_query = prepareQuery(q_string, initNs=NAMESPACE_MAP)

for row in curr_graph.query(curr_query):
    print(row.s)

q_string = "SELECT * WHERE {?s rdf:type odml:Section .}"
curr_query = prepareQuery(q_string, initNs=NAMESPACE_MAP)

for row in curr_graph.query(curr_query):
    print(row.s)

print(curr_graph.serialize(format='turtle').decode("utf-8"))
