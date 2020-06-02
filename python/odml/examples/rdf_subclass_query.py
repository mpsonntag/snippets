from odml.tools.rdf_converter import ODML_NS, RDFWriter

from rdflib import Graph, Namespace, RDF, RDFS
from rdflib.plugins.sparql import prepareQuery

from owlrl import DeductiveClosure, RDFS_Semantics

# Load a file containing subclasses to a default rdflib graph
fname = "./rdf_subclass_query.rdf.xml"

graph = Graph()
graph.parse(fname)

q_string = "SELECT * WHERE {?s rdf:type odml:Cell .}"
curr_query = prepareQuery(q_string, initNs={"odml": Namespace(ODML_NS), "rdf": RDF, "rdfs": RDFS})

for row in graph.query(curr_query):
    print(row.s)

q_string = "SELECT * WHERE {?s rdf:type odml:Section .}"
curr_query = prepareQuery(q_string, initNs={"odml": Namespace(ODML_NS), "rdf": RDF, "rdfs": RDFS})

for row in graph.query(curr_query):
    print(row.s)

print(g.serialize(format='turtle').decode("utf-8"))


# Test with an inference engine on top of the default rdflib graph
graph_expand = Graph()
graph_expand.parse(fname)

DeductiveClosure(RDFS_Semantics).expand(graph_expand)

q_string = "SELECT * WHERE {?s rdf:type odml:Cell .}"
curr_query = prepareQuery(q_string, initNs={"odml": Namespace(ODML_NS), "rdf": RDF, "rdfs": RDFS})

for row in graph_expand.query(curr_query):
    print(row.s)

q_string = "SELECT * WHERE {?s rdf:type odml:Section .}"
curr_query = prepareQuery(q_string, initNs={"odml": Namespace(ODML_NS), "rdf": RDF, "rdfs": RDFS})

for row in graph_expand.query(curr_query):
    print(row.s)

# For future test cases if a proper web endpoint is available the following implementation might
# be a faster RDFS inference implementation e.g. for subclass inference
# from SPARQLWrapper import SPARQLWrapper, JSON
# sparql = SPARQLWrapper("web address")
# sparql.addParameter('inference','true')
# sparql.setReturnFormat(JSON)
