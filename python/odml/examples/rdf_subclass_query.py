"""
This script tests how to load an RDF file to an rdflib graph
and query the content.
Meant to test various additional libraries for their RDF inference/reasoning
since the basic rdflib implementation does not supply inference.
"""

from odml.tools.rdf_converter import ODML_NS

from rdflib import Graph, Namespace, RDF, RDFS
from rdflib.plugins.sparql import prepareQuery

from owlrl import DeductiveClosure, RDFS_Semantics


FNAME = "./rdf_subclass_query.rdf.xml"
NAMESPACE_MAP = {"odml": Namespace(ODML_NS), "rdf": RDF, "rdfs": RDFS}


def run_query(curr_graph):
    """
    Runs two queries on a provided graph. The first query tests
    a subclass "Cell" directly, the second query tests whether this
    subclass can also be found via its superclass "Section".

    Prints all results and the full graph to the command line.

    :param curr_graph: an rdflib in memory graph
    """
    q_string = "SELECT * WHERE {?s rdf:type odml:Cell .}"
    curr_query = prepareQuery(q_string, initNs=NAMESPACE_MAP)

    for row in curr_graph.query(curr_query):
        print(row.s)

    q_string = "SELECT * WHERE {?s rdf:type odml:Section .}"
    curr_query = prepareQuery(q_string, initNs=NAMESPACE_MAP)

    for row in curr_graph.query(curr_query):
        print(row.s)

    print(curr_graph.serialize(format='turtle').decode("utf-8"))

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
