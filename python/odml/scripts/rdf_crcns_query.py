from odml.tools.rdf_converter import ODML_NS

from rdflib import Graph, Namespace, RDF, RDFS
from rdflib.plugins.sparql import prepareQuery


FNAME = "./rdf_crcns_query.rdf.xml"
NAMESPACE_MAP = {"odml": Namespace(ODML_NS), "rdf": RDF, "rdfs": RDFS}


curr_graph = Graph()
curr_graph.parse(FNAME)

q_string = """
SELECT * WHERE {
  ?p rdf:type odml:Property .
  ?p odml:hasName ?prop_name .
  ?p odml:hasValue ?v .
}"""

curr_query = prepareQuery(q_string, initNs=NAMESPACE_MAP)

for row in curr_graph.query(curr_query):
    print("%s: %s" % (row.prop_name, row.v))

