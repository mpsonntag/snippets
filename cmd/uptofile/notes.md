### server layout

- upload page
  - schachtel selection list
  - new schachtel field (+)
  - schnippsel field
  - code form field
  - hidden code form field
- serve file -> requires auth

### data model

- add as RDF triples
- use namespace "miso"; http://mpsmiso/notesgraph

- main graph layout
  - schachtel
    - pred name -> text
  - gifterl
    - pred active -> bool
    - pred date_created -> date
    - pred date_changed -> rdf:Seq -> date
    - pred geschichte -> rdf:Seq -> inhalt_text
  - schnippsel
    - pred tagged -> category (circular graph?)
    - pred inhalt -> text

### various concepts
- current/offset day date as pass-part
- hiddenVal-date-knownVal
