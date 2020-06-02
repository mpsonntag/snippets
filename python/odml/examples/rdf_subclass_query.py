from odml.tools.rdf_converter import ODML_NS

from rdflib import Graph, Namespace, RDF, RDFS
from rdflib.plugins.sparql import prepareQuery

from owlrl import DeductiveClosure, RDFS_Semantics


def run_query(curr_graph):
    q_string = "SELECT * WHERE {?s rdf:type odml:Cell .}"
    curr_query = prepareQuery(q_string, initNs=NAMESPACE_MAP)

    for row in curr_graph.query(curr_query):
        print(row.s)

    q_string = "SELECT * WHERE {?s rdf:type odml:Section .}"
    curr_query = prepareQuery(q_string, initNs=NAMESPACE_MAP)

    for row in curr_graph.query(curr_query):
        print(row.s)

    print(curr_graph.serialize(format='turtle').decode("utf-8"))


FNAME = "./rdf_subclass_query.rdf.xml"
NAMESPACE_MAP = {"odml": Namespace(ODML_NS), "rdf": RDF, "rdfs": RDFS}

# Load a file containing subclasses to a default rdflib graph
graph = Graph()
graph.parse(FNAME)
run_query(graph)

# Test with an inference engine on top of the default rdflib graph
graph_expand = Graph()
graph_expand.parse(FNAME)

DeductiveClosure(RDFS_Semantics).expand(graph_expand)
run_query(graph_expand)

# For future test cases if a proper web endpoint is available the following implementation might
# be a faster RDFS inference implementation e.g. for subclass inference
# from SPARQLWrapper import SPARQLWrapper, JSON
# sparql = SPARQLWrapper("web address")
# sparql.addParameter('inference','true')
# sparql.setReturnFormat(JSON)
