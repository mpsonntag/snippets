import odml

from odml.tools.rdf_converter import ODML_NS

from rdflib import Graph, Namespace, RDF, RDFS
from rdflib.plugins.sparql import prepareQuery

fname = "/home/sommer/Chaos/tmp/odml/rdf/sub_class_query.rdf"

doc = odml.Document()
sec = odml.Section(name="Cell", type="cell", parent=doc)

odml.save(doc, fname, "RDF")

graph = Graph()
graph.parse(fname)

q_string = "SELECT * WHERE {?s rdf:type odml:Cell .}"

curr_query = prepareQuery(q_string, initNs={"odml": Namespace(ODML_NS), "rdf": RDF, "rdfs": RDFS})

for row in graph.query(curr_query):
    print(row.s)
