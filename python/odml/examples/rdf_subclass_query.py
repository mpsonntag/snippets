from odml.tools.rdf_converter import ODML_NS, RDFWriter

from rdflib import Graph, Namespace, RDF, RDFS
from rdflib.plugins.sparql import prepareQuery

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
