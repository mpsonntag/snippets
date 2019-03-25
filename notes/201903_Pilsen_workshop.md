# Mo, 25.03.2019, 06:00 - ()

- Travel to venue


[C] odml_to_rdf ... report StringIO: check if we can use `with` for the deferred close of the StringIO

[C] doc/section_subclasses.yaml is in docs but not used there. it is required in odml/tools/rdf_converter
    maybe move it there and remove the monkey_patch read of file.

[C] is there a NIX issue for a NIX file UUID to properly reference a whole data file?

[C] should odML feature a UUID for the referenced data at the document level.
    it would be good to have a data reference UUID and a data reference URI.
    In the python odml datamodel, `document` will gain two more attributes:
    - data_reference_uuid
    - data_reference_uri
    To export to RDF this would be a new Node:
    - Node: DataReference
    - Edge Document-DataReference: hasDataReference
    - Edge DataReference-DataUUID: hasDataUUID
    - Edge DataReference-DataURI: hasDataURI


https://docs.google.com/document/d/1JZaq_NzJy9u33pF2HS9mDejaUuzn9xSLZ8LuPGlJcHc/


# Tu, 26.03.2019,


# We, 27.03.2019, 


# Th, 28.03.2019, 


# Fr, 29.03.2019, 

