### data model

- add as RDF triples
- use namespace "miso"; http://mpsmiso/notesgraph

- main graph layout
  - category
    - pred name
  - gifterl
    - pred status - active/inactive
    - pred date_created
    - pred date_changed
  - snippet
    - pred tagged
      -> category (circular graph?)
    - pred content

### various concepts
- current/offset day date as pass-part
