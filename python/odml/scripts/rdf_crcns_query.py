"""
Example queries of a CRCNS data RDF graph.
"""
import os
import pathlib

from odml.tools.rdf_converter import ODML_NS

from rdflib import Graph, Namespace, RDF, RDFS
from rdflib.plugins.sparql import prepareQuery


# Prepare graph from RDF file.
CURR_PATH = pathlib.Path(__file__).parent.resolve()
FILE_NAME = "rdf_crcns_query.rdf.xml"
FILE_PATH = os.path.join(CURR_PATH, FILE_NAME)

curr_graph = Graph()
curr_graph.parse(FILE_PATH)

NAMESPACE_MAP = {"odml": Namespace(ODML_NS), "rdf": RDF, "rdfs": RDFS}

q_string = """
SELECT * WHERE {
  ?p rdf:type odml:Property .
  ?p odml:hasName ?prop_name .
  ?p odml:hasValue ?v .
  ?v ?pred ?value .
  FILTER (strstarts(str(?pred), str(rdf:_)))
}"""

curr_query = prepareQuery(q_string, initNs=NAMESPACE_MAP)

for row in curr_graph.query(curr_query):
    print(f"{row.prop_name}: {row.value}")

# Make sure there is a DataReference providing a uri
q = prepareQuery("""SELECT *
                   WHERE {
                   ?datasec a odml:DataReference .
                   ?datasec odml:hasName ?dataSecName .
                   ?datasec odml:hasProperty ?uriprop .
                   ?uriprop odml:hasName ?nameValue .
                   ?uriprop odml:hasValue ?urival .
             }""", initNs=NAMESPACE_MAP)

for row in curr_graph.query(q):
    print(f"Sec: {row.datasec}, DataSecName: {row.dataSecName}, Prop: {row.nameValue}")

# Return all identifiers in a graph
q = prepareQuery("""
SELECT * WHERE {
    ?d a odml:Document .
    ?d odml:hasSection* ?doisec .
    ?doisec a odml:Identifier .
    ?doisec odml:hasName ?doiSecName .
    ?doisec odml:hasProperty ?doiprop .
    ?doiprop odml:hasName "identifier" .
    ?doiprop odml:hasValue ?urival .
    ?urival ?pred ?uri .
    FILTER (strstarts(str(?pred), str(rdf:_)))
}""", initNs=NAMESPACE_MAP)

for row in curr_graph.query(q):
    print(f"Doc: {row.doisec}, Sec: {row.d}, "
          f"DataSecName: {row.doiSecName}, Prop: {row.uri}")

# Return all DataCite DOI identifiers in a graph
q = prepareQuery("""
SELECT * WHERE {
    ?d a odml:Document .
    ?d odml:hasSection* ?doisec .
    ?doisec a odml:Identifier .
    ?doisec odml:hasName ?dataSecName .
    ?doisec odml:hasProperty ?uriprop .
    ?uriprop odml:hasName "identifier" .
    ?uriprop odml:hasValue ?urival .
    ?urival ?uripred ?uri .
    ?doisec odml:hasProperty ?tprop .
    ?tprop odml:hasName "identifierType" .
    ?tprop odml:hasValue ?tpropval .
    ?tval ?tpred "DOI" .
    FILTER (strstarts(str(?uripred), str(rdf:_)))
}""", initNs=NAMESPACE_MAP)

for row in curr_graph.query(q):
    print(f"Doc: {row.d}, Sec: {row.doisec}, "
          f"DataSecName: {row.dataSecName}, Prop: {row.uri}")

# Searching for datasets that deal with Behavior or Extracellular recordings
q = prepareQuery("""
SELECT * WHERE {
    ?d a odml:Document .
    ?d odml:hasSection* ?s .
    ?s odml:hasType ?sectype . 
    ?s odml:hasName ?secname .
    { SELECT ?doiSecName ?uri WHERE {
        ?d a odml:Document .
        ?d odml:hasSection* ?doisec .
        ?doisec a odml:Identifier .
        ?doisec odml:hasName ?doiSecName .
        ?doisec odml:hasProperty ?uriprop .
        ?uriprop odml:hasName "identifier" .
        ?uriprop odml:hasValue ?urival .
        ?urival ?uripred ?uri .
        ?doisec odml:hasProperty ?tprop .
        ?tprop odml:hasName "identifierType" .
        ?tprop odml:hasValue ?tpropval .
        ?tval ?tpred "DOI" .
        FILTER (strstarts(str(?uripred), str(rdf:_)))
    }}
    FILTER (?sectype in ("Extracellular recordings", "Behavior"))
}""", initNs=NAMESPACE_MAP)

for row in curr_graph.query(q):
    print(f"Doc: {row.d}, SecName: {row.secname}, "
          f"DoiName: {row.doiSecName}, DOI: {row.uri}")

# Searching for datasets that contain specific keywords
q = prepareQuery("""
SELECT * WHERE {
    ?d a odml:Document .
    ?d odml:hasSection* ?s .
    ?s odml:hasName ?secname .
    ?s odml:hasProperty ?p .
    ?p odml:hasName "task_keyword" .
    ?p odml:hasValue ?pval .
    ?pval ?valpred ?val .
    { SELECT ?doiSecName ?uri WHERE {
        ?d a odml:Document .
        ?d odml:hasSection* ?doisec .
        ?doisec a odml:Identifier .
        ?doisec odml:hasName ?doiSecName .
        ?doisec odml:hasProperty ?uriprop .
        ?uriprop odml:hasName "identifier" .
        ?uriprop odml:hasValue ?urival .
        ?urival ?uripred ?uri .
        ?doisec odml:hasProperty ?tprop .
        ?tprop odml:hasName "identifierType" .
        ?tprop odml:hasValue ?tpropval .
        ?tval ?tpred "DOI" .
        FILTER (strstarts(str(?uripred), str(rdf:_)))
    }}
    FILTER (?val in ("reward", "response"))
    FILTER (strstarts(str(?valpred), str(rdf:_)))
}""", initNs=NAMESPACE_MAP)

for row in curr_graph.query(q):
    print(f"Doc: {row.d}, SecName: {row.secname}, Value: {row.val}, DOI: {row.uri}")

# Searching for datasets that contain diverse sets of values
# e.g. Organisation, Organism, etc
q = prepareQuery("""
SELECT * WHERE {
    ?d a odml:Document .
    ?d odml:hasSection* ?s .
    ?s odml:hasName ?secname .
    ?s odml:hasProperty ?p .
    ?p odml:hasName ?propName .
    ?p odml:hasValue ?pval .
    ?pval ?valpred ?val .
    { SELECT ?uri ?doiSecName WHERE {
        ?d a odml:Document .
        ?d odml:hasSection* ?doisec .
        ?doisec a odml:Identifier .
        ?doisec odml:hasName ?doiSecName .
        ?doisec odml:hasProperty ?doiprop .
        ?doiprop odml:hasName ?nameValue .
        ?doiprop odml:hasValue ?urival .
        ?urival ?uripred ?uri .
        FILTER (?nameValue in ("identifier"))
        FILTER (strstarts(str(?uripred), str(rdf:_)))
    }}
    FILTER (?val in ("Dataset/Neurophysiology", "CRCNS.org", "mice"))
    FILTER (strstarts(str(?valpred), str(rdf:_)))
}""", initNs=NAMESPACE_MAP)

for row in curr_graph.query(q):
    print(f"Doc: {row.d}, SecName: {row.secname}, PropName: {row.propName}, "
          f"Value: {row.val}, DOI: {row.uri}")
