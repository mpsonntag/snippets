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

[C]
- a) Check how other projects actually handle the RDF namespace. is the namespace actually the 
     place where the resources have to be linked? should our namespace change to meta.gnode.org or should
     https://g-node.org/projects/odml-rdf resolve to meta.gnode.org? Where and how should the odml OWL be
     available from then?
- b) The current odml rdf ontology should be served and available at a place defined in a)
- c) check auto-deployment of the odml OWL from python-odml via github to the appropriate place when
     new version get released.

        :param data_repository: URI pointing to where the odml documents or the data
                                these documents are describing can be found.
                                Default is None. If a data_repository is provided, it will
                                be attached to all passed documents under the RDF


https://docs.google.com/document/d/1JZaq_NzJy9u33pF2HS9mDejaUuzn9xSLZ8LuPGlJcHc/


# Tu, 26.03.2019,


# We, 27.03.2019, 


# Th, 28.03.2019, 


# Fr, 29.03.2019, 

