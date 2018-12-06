------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

import uuid
from rdflib import Graph, Namespace, RDF, URIRef

g = Graph()

# create custom odml namespace
ns = Namespace("http://g-node.org/odml-rdf#")

# use a specific prefix for our custom odml namespace
g.bind('odml', ns)

# create named hub node - since the custom id is supposed to be a uuid,
# it should be unique wherever, making it unlikely that two different instances 
# have the same id - needs to be replaced 
# maybe there is a nicer way to get a proper uuid tough, I'm not a python guy ;)
hubNode = URIRef(uuid.uuid4().urn[9:])

# create named document node
docNode = URIRef(uuid.uuid4().urn[9:])

# add hubNode to graph, add it as RDF type "odml:Hub"
g.add( (hubNode, RDF.type, ns.Hub) )

# add docNode to graph, add it as RDF type "odml:Document"
g.add( (docNode, RDF.type, ns.Document) )

# connect docNode as child of hubNode via predicate "odml:hasDocument"
g.add( (hubNode, ns.hasDocument, docNode) )

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

odml/RDF

PREFIX odml: <https://g-node.org/projects/odml-rdf#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?d ?f ?name ?name ?pname
WHERE {
    ?d rdf:type odml:Document .
    ?d odml:hasFileName ?f .
    ?d odml:hasSection ?s .
    ?s odml:hasName ?name .
    ?s odml:hasProperty ?p .
    ?p odml:hasName ?pname .
}



PREFIX odml: <https://g-node.org/projects/odml-rdf#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?file ?sec_name ?prop_name ?value
WHERE {
    ?d rdf:type odml:Document .
    ?d odml:hasFileName ?file .
    ?d odml:hasSection ?s .
    ?s odml:hasName ?sec_name .
    ?s odml:hasProperty ?p .
    ?p odml:hasName ?prop_name .
    ?p odml:hasValue ?v .
    ?v rdfs:member ?value .
    {?p odml:hasName "experiment"} UNION {?p odml:hasName "Recording duration"} .
}
ORDER BY ?file
LIMIT 100

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

Issues

- odml/rdf: are version/docversion floats or should they be literals as well
- odml/rdf: address property reference vs source/filename with Jan as soon as possible to include it in 
    RDF as well.
- odml/rdf: next steps / to discuss
    - Converter v1.3/v1.4
- odml2rdf Version converter:
    - L45 add check, if file is version 1 before converting to 1.1
- odml2rdf: add id label to graph
- odml2rdf: odml Ontology: ###  https://g-node.org/projects/odml-rdf#hasId does not seem to be
    defined for Terminology or rather does not include it in the rdfs:domain 

odml2rdf: 

- write a proper namespace document with the proposed RDF model that we can provide via a URL.
- no rdf:about yet (not instances of a class)
- values are not individual values yet
- call namespace shorthand "odml"
- the node ids are document internal and not uuids (howto deal with uuids that are not supposed to start with digits?)

- odml2rdf: point https://g-node.org/projects/odml-rdf to the owl file; preferably in the github page
- odml2rdf: namespace prefix number issue
- odml2rdf: version converter: does sthg weird with some values - e.g. &#956;m in terminologies/v1.0/electrode/electrode.xml#TipSize
