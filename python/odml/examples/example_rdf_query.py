from odml.tools.rdf_converter import ODML_NS

from rdflib import Graph, Namespace, RDF, RDFS
from rdflib.plugins.sparql import prepareQuery

NAMESPACE_MAP = {"odml": Namespace(ODML_NS), "rdf": RDF, "rdfs": RDFS}

res_cite = './resources/template_examples/rdf/i140703-001_datacite_conv.rdf'
res_uri = './resources/template_examples/rdf/datauri.rdf'

graph = Graph()

graph.parse(res_cite)
graph.parse(res_uri)

# Find a section by its type that is a direct child of a document
q = prepareQuery("""SELECT *
            WHERE {
               ?d rdf:type odml:Document .
               ?d odml:hasSection ?s .
               ?s rdf:type odml:Section .
               ?s odml:hasType "setup/daq" .
            }""", initNs=NAMESPACE_MAP)

for row in graph.query(q):
    print("Doc: %s, Sec: %s" % (row.d, row.s))

# Find a section by its type, and its document, that is a anywhere down any number of subsections

q = prepareQuery("""SELECT * 
             WHERE { 
                ?d a odml:Document . 
                ?d odml:hasSection* ?s . 
                ?s a odml:Section . 
                ?s odml:hasType "setup/daq/preprocessing" . 
                ?s odml:hasName ?name . 
             }""", initNs=NAMESPACE_MAP)

for row in graph.query(q):
    print("Doc: %s, Sec: %s, Name: %s" % (row.d, row.s, row.name))

# Make sure there is a DataReference providing a uri
q = prepareQuery("""SELECT * 
                   WHERE {
                   ?datasec a odml:Section .
                   ?datasec odml:hasType "DataReference" .
                   ?datasec odml:hasName ?dataSecName .
                   ?datasec odml:hasProperty ?uriprop .
                   ?uriprop odml:hasName ?nameValue .
                   ?uriprop odml:hasValue ?urival .
                   ?urival ?pred ?uri. 
                   FILTER (?nameValue in ("DataDOI", "DataURI"))
                   FILTER (strstarts(str(?pred), str(rdf:_)))
             }""", initNs=NAMESPACE_MAP)

for row in graph.query(q):
    print("Sec: %s, DataSecName: %s, DOI: %s" % (row.datasec, row.dataSecName, row.uri))


q = prepareQuery("""SELECT * 
             WHERE { 
                ?d a odml:Document . 
                ?d odml:hasSection* ?s .
                ?s a odml:Section . 
                ?s odml:hasType "setup/daq/preprocessing" . 
                ?s odml:hasName ?secname . 
                { SELECT ?dataSecName ?uri
                   WHERE {
                   ?d odml:hasSection ?datasec .
                   ?datasec odml:hasType "DataReference" .
                   ?datasec odml:hasName ?dataSecName .
                   ?datasec odml:hasProperty ?uriprop .
                   ?uriprop odml:hasName ?nameValue .
                   ?uriprop odml:hasValue ?urival .
                   ?urival ?pred ?uri. 
                   FILTER (?nameValue in ("DataDOI", "DataURI"))
                   FILTER (strstarts(str(?pred), str(rdf:_)))
                   }
                 }
             }""", initNs=NAMESPACE_MAP)

for row in graph.query(q):
    print("Doc: %s, secname: %s, DataSecName: %s, datauri: %s" % (row.d, row.secname,
                                                                  row.dataSecName, row.uri))


q = prepareQuery("""SELECT * 
             WHERE { 
                ?d a odml:Document . 
                ?d odml:hasSection* ?s .
                ?s a odml:Section . 
                ?s odml:hasType ?t . 
                ?s odml:hasName ?secname . 
                { SELECT ?dataSecName ?uri
                   WHERE {
                   ?d odml:hasSection ?datasec .
                   ?datasec odml:hasType "DataReference" .
                   ?datasec odml:hasName ?dataSecName .
                   ?datasec odml:hasProperty ?uriprop .
                   ?uriprop odml:hasName ?nameValue .
                   ?uriprop odml:hasValue ?urival .
                   ?urival ?pred ?uri. 
                   FILTER (?nameValue in ("DataDOI", "DataURI"))
                   FILTER (strstarts(str(?pred), str(rdf:_)))
                   }
                 }
                FILTER (?t in ("setup/daq/preprocessing", "stimulus/white_noise"))
             }""", initNs=NAMESPACE_MAP)

for row in graph.query(q):
    print("Doc: %s, secname: %s, DataSecName: %s, datauri: %s" % (row.d, row.secname,
                                                                  row.dataSecName, row.uri))


"""
PREFIX odml: <https://g-node.org/projects/odml-rdf#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?stype ?sec_name ?propname ?parent_type WHERE {
    ?parent odml:hasSection ?s .
    ?s rdf:type odml:Section .
    ?s odml:hasName ?sec_name .
    ?s odml:hasProperty ?p .
    ?p odml:hasName "LocalAnaesthesia" .
    ?s odml:hasProperty ?prop .
    ?prop odml:hasName ?propname .
    ?parent rdf:type ?parent_type .
    ?s rdf:type ?stype
}
"""
