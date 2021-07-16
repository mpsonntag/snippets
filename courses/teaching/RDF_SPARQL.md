RDF, SPARQL and OWL
===================

RDF ... resource description framework
RDFS ... RDF schema
SPARQL ... SPARQL protocol and RDF query language

# RDF
- All RDF data is stored as a graph
- An RDF graph is a set of RDF triples


## RDF term syntax

### RDF triple
An RDF triple always consists of three components and is usually written in the following order:
- subject
    - can be an IRI named resource or a blank node.
    - called start node in an RDF graph.
    - used to denote RESOURCE to the world.
- predicate
    - also called property.
    - has to be an IRI named resource.
- object
    - can be an IRI named resource, a literal or a blank node.
    - called end node in an RDF graph.
    - used to denote RESOURCE to the world.
    - also called property value.

NOTE: IRIs, literals and blank nodes are called "RDF terms"


### IRIs
IRI ... internationalized resource identifier; internet standard to extend the URI (uniform resource identifier) scheme.
IRIs can contain characters from the unicode/ISO 10646 universal character set whereas URI uses only ASCII.

There are specific rules how an IRI has to be constructed:
- http://www.w3.org/TR/rdf-sparql-query/#rIRIref

In detail:

    [67]    IRIref          ::=     IRI_REF | PrefixedName
    [68]    PrefixedName    ::=     PNAME_LN | PNAME_NS
    [69]    BlankNode       ::=     BLANK_NODE_LABEL | ANON
    [70]    IRI_REF         ::=     '<' ([^<>"{}|^`\]-[#x00-#x20])* '>'
    [71]    PNAME_NS        ::=     PN_PREFIX? ':'
    [72]    PNAME_LN        ::=     PNAME_NS PN_LOCAL

e.g. `<http://example.org/book/book1>`

There are different ways how to make the IRI above relative. These two ways require the keywords `BASE` and `PREFIX`:

    BASE <http://example.org/book/>
    <book1>

or

    PREFIX book: <http://example.org/book/>
    book:book1

### Literals
Literals are used for values such as strings, numbers and dates.

A literal consists of 2-3 elements
- a lexical form, being a UNICODE string
- a datatype IRI ... this determines how the lexical form maps to a literal value
- if the datatype IRI is `http://www.w3.org/1999/02/22-rdf-syntax-ns#langString`,
then it is a non-empty language tag. If this element is present, then the literal is considered to be a language-tagged string.

Simple literals consist only of the lexical form. 

The literal value associated with a literal has to be interpreted depending on the present elements:
1. If it happens to be a language-tagged string, the literal value is a pair of the lexical form and the language tag (in this order)
2. xxx

## RDF terminology:
Subjects can have properties, which are called "predicates"

e.g.

    subject ... rdf:Description
    predicate ... feature:size

    <rdf:Description>
        <feature:size>12</>
    </rdf:Description>


### OWL properties/predicates can be divided into two groups
- Object properties (owl:ObjectProperty) relates individuals (instances) of two OWL classes.
- Datatype properties (owl:DatatypeProperty) relates individuals (instances) of OWL classes to literal values.


## Nodes in an RDF Graph:
There are three kinds of nodes in an RDF graph:
- Resource nodes ... a resource is anything that can have things said about it. In triples this refers to subjects and
objects. In graphical representations resources are depicted by ovals.
- Literal nodes ... all actual values, In graphical representations literals are depicted by rectangles.
- Blank nodes ... A resource without a URI; should be avoided as much as possible (can make automatic merges harder).


### Breaking Down An RDF Statement
Here you see the subject of the statement (what the statement is about) and the two forms of predicates
(literal values and resources, which reference other RDF statements).

    <rdf:Description rdf:about="subject">
        <predicate rdf:resource="object" />
        <predicate>literal value</predicate>
    <rdf:Description>



## Nice to Know:
- In Jena an RDFNode is a superclass of both Resource and Literal.


## RDF vocabulary:

Syntax names:
- `rdf:RDF`
- `rdf:Description`
- `rdf:ID`
- `rdf:about`
- `rdf:parseType`       ... RDF/XML specific tells the parser how to interpret a node depending on the value of the parseType attribute.
- `rdf:resource`
- `rdf:li`              ... Alt, Bag or Seq item
- `rdf:nodeID`
- `rdf:datatype`

Class names:
- `rdf:Seq`             ... contains an ordered list of rdf:li items
- `rdf:Bag`             ... contains an unordered list of rdf:li items
- `rdf:Alt`             ... contains list of alternative rdf:li items (user can select which)
- `rdf:Statement`
- `rdf:Property`
- `rdf:XMLLiteral`
- `rdf:List`

Property names:
- `rdf:subject`
- `rdf:predicate`
- `rdf:object`
- `rdf:type`            ... defining which class an instance belongs to
- `rdf:value`
- `rdf:first`
- `rdf:rest_n`          ... (where n is a decimal integer > 0)

Resource names:
- `rdf:nil`

e.g. the hashURI of rdf:type is:
- http://www.w3.org/1999/02/22-rdf-syntax-ns#type


## RDFS vocabulary:

### RDF:type
RDF:type is an RDFS property, that defines the CLASS of a resource. one resource can have multiple classes

e.g.

    @prefix RDF: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix RDFS: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix exp: <someURI/example> .

    exp:MyHondaCivic RDF:type exp:UsedCarForSale
    exp:MyHondaCivic RDF:type exp:PassengerVehicle
    exp:MyHondaCivic RDF:type exp:ThingForSale


### RDF:Class, RDFS:Property, RDFS:Domain and RDFS:Range

Analogy to relational database:
- table ... class
- column ... property

- `rdf:domain` ... "[] is property of []"
- `rdfs:range` ... "[] property allows value []"

Instances can inherit properties from all of the classes they belong to. To define the properties of a class,
the definition has to be in the same database as the instances. Properties require `RDFS:Domain` and `RDFS:Range`
to know to which class they belong to.

- `RDFS:Domain` states all things to which the current property applies.
- `RDFS:Range` states which data types can be excepted by the current property.

e.g.

    @prefix RDF: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix RDFS: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    @prefix exp: <someURI/example> .

    exp:UsedCarForSale RDF:Type RDF:Class       ... define class UsedCarForSale within "namespace" exp
    exp:Person RDF:Type RDF:Class               ... define class Person within "namespace" exp
    exp:Price RDF:Type RDFS:Property            ... define property Price within "namespace" exp
    exp:PastOwners RDF:Type RDFS:Property       ... define property PastOwners within "namespace" exp
    exp:Price RDFS:Domain exp:UsedCarForSale    ... define that "exp:Price" (which is a property in our case)
                                                ... applies to "exp:UsedCarForSale" (which is a class in our case)
                                                ... meaning: exp:Price is a property of exp:UsedCarForSale
    exp:Price RDFS:Range XSD:int                ... define that "exp:Price" accepts only XSD:int as value,
                                                ... more than one Ranges can be defined for a property
                                                ... meaning exp:Price accepts XSD:int
    exp:PastOwners RDFS:Range exp:Person        ... define that "exp:PastOwners" accepts only exp:Persons as value


### RDFS:subClassOf

`X RDFS:subClassOf  Y`  ... all instances of class X have are also instances of class Y and
have all properties of Y in addition to all properties of X.

e.g.

    @prefix RDF: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix RDFS: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    @prefix exp: <someURI/example> .

    exp:ThingsForSale RDF:type RDF:Class
    exp:Car RDF:type RDF:Class
    exp:UsedCarForSale RDF:type RDF:Class

    exp:Price RDF:type RDFS:Property
    exp:MilesPerGallon RDF:type RDFS:Property

    exp:Price RDFS:Domain exp:ThingForSale                          ... Price is a property of ThingsForSale
    exp:MilesPerGallon RDFS:Domain exp:Car                          ... MilesPerGallon is a property of Car
    exp:UsedCarForSale RDFS:subClassOf exp:Car, exp:ThingForSale    ... UsedCarForSale has properties Price and MilesPerGallon


### RDFS:subPropertyOf

`X RDFS:subPropertyOf Y` ... subproperty allows for specifying different types of properties while
making them all available by a common superProperty.

e.g.

    exp:Mother RDFS:subPropertyOf exp:Parent

    exp:Fred exp:Mother exp:Franny
    exp:Fred exp:Father exp:Bert

We use searching for exp:Mother to get the Mother of Fred, we use searching for exp:Father to get the Father of Fred,
we use searching for exp:Parent to get both parents of Fred even though `exp:Fred exp:Parent exp:Franny`
and `exp:Fred exp:Parent exp:Bert` are not explicitly stored in the database!



## Turtle language features

A Turtle document is a collection of RDF statements in the format

    <sub> <pred> <obj> .

- subject and predicate must be represented by a URI
- object can be a URI or a literal
- a URI has to be enclosed in `<>` brackets.
- a statement has to end with a period
- a language specific literal is marked by an @ followed by the language shorthand e.g. `"this is english"@en`
- specific data types are denoted by `^^` and the URI of the corresponding data type

        "10"^^<.../XMLSchema#decimal>



# SPARQL (SPARQL Protocol and RDF Query Language)
- Query language for data stored in RDF databases. Can be translated into SQL statements to also access relational databases
e.g. MongoDB, Cassandra. SPARQL access data stored as "key-value" pairs or "subject-predicate-object" triples.
- SPARQL queries actually look for "graph patterns" in an RDF graph.
- Variables in SPARQL queries start with a question mark; e.g. `?x`

### Full SPARQL query example

    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT ?name
    FROM <http://example.com/dataset.rdf>
    WHERE {
      ?x foaf:name ?name .
    }
    ORDER BY ?name

### SPARQL return clauses
- `ASK` ... `ASK` can be used instead of `SELECT`. It returns a boolean value depending
if there is at least one result for the connected query or not.
- `DESCRIBE` ... returns an RDF graph that describes a resource.
- `CONSTRUCT` ... used to construct a new graph from the data returned by the query.

## SPARQL protocol

SPARQL queries can be done via simple http requests!

Example:

    curl –I http://dbpedia.org/sparql?query=PREFIX%20rdf%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0ASELECT%20*%20WHERE%20%7B%0A%3Fcity%20rdf%3Atype%20%3Chttp%3A%2F%2Fdbpedia.org%2Fclass%2Fyago%2FCitiesInTexas%3E%0A%7D%0A


# OWL

### OWL functions as a kind of schema for data stored as RDF
There are different so called OWL profiles. The choice which to use is always a trade off of
modeling vs reasoner performance. Check out performance
[here](http://www.w3.org/TR/owl-profiles/#Computational_Properties).

### OWL Profiles:
#### OWL 2/full
- most expressive profile
- inference rules contained are extensive, automatic reasoning is slow even on current machines

#### OWL 2 / EL
- excessive profile
- useful when there are complex relationships between many different classes and properties
- infers which instances belong to which classes fairly quickly

#### OWL 2 / QL
- useful when there are many instances of not many different classes
- optimized to run on top of a relational DB: it is fairly easy for an ontology written in QL to rewrite its
SPARQL queries to SQL queries

#### OWL 2 / RL
- optimized to work well with business logic rules

#### Profiles Conclusion:
- If you need to reason efficiently over intricately related classes and properties, use OWL 2 / EL.
- If you have a large amount of instance data and you primarily just want to query it efficiently using some
moderately complex class relationships, use OWL 2 / QL.
- If you have more complicated class relationships and are building on a typical business rules engine, use OWL 2 / RL.

### OWL properties and restrictions:
- http://www.cambridgesemantics.com/semantic-university/owl-reference-humans


## Link list:
- [w3c RDF primer](https://www.w3.org/2000/10/swap/Primer.html)
- [w3c another RDF primer](https://www.w3.org/TR/2004/REC-rdf-primer-20040210/)
- http://www.linkeddatatools.com/introducing-rdfs-owl
- https://books.google.de/books?id=vcmoBQAAQBAJ
- http://www.w3.org/TR/rdf-schema/
- [w3c/RDF 1.1 Concepts and Abstract Syntax](http://www.w3.org/TR/rdf11-concepts)
- [RDF 1.1 XML syntax](https://www.w3.org/TR/rdf-syntax-grammar/)
- http://www.w3.org/TR/rdf-sparql-query/
- http://www.w3.org/TR/owl-profiles/#Computational_Properties
- http://www.w3schools.com/webservices/ws_rdf_intro.asp
- http://www.cambridgesemantics.com/semantic-university/rdfs-introduction
- http://www.cambridgesemantics.com/semantic-university/owl-reference-humans
- https://jena.apache.org/tutorials/rdf_api.html

## RDF libraries

- [Python/RDFlib github](https://github.com/RDFLib/rdflib)
- [Python/RDFlib](https://rdflib.readthedocs.io/en/stable/)
- [Python/RDFlib tutorial](http://code.alcidesfonseca.com/docs/rdflib/index.html)

## RDF library tutorials

- [RDF and SPARQL with Sesame and python](http://www.jenitennison.com/2011/01/25/getting-started-with-rdf-and-sparql-using-sesame-and-python.html)

