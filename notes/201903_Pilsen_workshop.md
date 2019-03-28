# Mo, 25.03.2019, 06:00 - 18:00 (12h ... +27h)

- Travel to venue

-- nix issues

[C] is there a NIX issue for a NIX file UUID to properly reference a whole data file?


-- odml issues

[C] odml_to_rdf ... report StringIO: check if we can use `with` for the deferred close of the StringIO

[C] doc/section_subclasses.yaml is in docs but not used there. it is required in odml/tools/rdf_converter
    maybe move it there and remove the monkey_patch read of file.

[C] rdf_converter: does writer.save_element actually need to return the self.g? The changes are already accessible
                   via the class...

[C] rdf_converter: rdf_converter.write_file appends to its own graph every time it is called! Something very
                   wrong is going on here!


-- general odml topics to discuss

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


# Tu, 26.03.2019, 09:00 - 18:00 (9h ... +28h)

- odml to RDF discussion with Thomas Wachtler, Jeff Teeters, Pavel ...
- odml-terminologies update to accommodate data reference
- example odml files with added data references
- discussions with Jeff Teeters, Roman Moucek and Radjeet regarding G-Node tools and features

# We, 27.03.2019, 10:00 - 18:00 (8h ... +28h)

- gnode: email to GSoC applicant
- gnode: documentation of last days
- odml-terminologies update to accommodate data reference
- example odml files with added data references

[C] ... with odml RDF an unresolved issue is, if the exported odml file does not have 
UUIDs yet. if they are re-imported, they will be added to the graph and reside there as 
double entries.

[C] The conversion script should already add uuids to all new properties and sections if 
there are none. This way the converted script will at least always feature the same IDs 
as compared to when someone currently opens a converted file without saving, the ids 
will always be different.

[C] Check state of matlab - odml library
    - check how hard the update would be
    - check how hard the bridge - use python library in MatLab - is.


# Th, 28.03.2019, 09:30 - ()

- odml: creating template repository and populating it.
- odml: fixing terminologies, data reference PR.
- gnode: assisting with converting and annotating Pilzen odml files and putting them on gin
- odml: working on Plzen templates


[C] put conversion script notices and descriptions everywhere (github, tutorial, etc)
[C] Better description in the commandline tools
[C] Extract DataReference on gin from odml docs and prominently display them under the rendered display
[C] Check odml renderer on gin for Neuroinf group / eeg-erp datasets


# Fr, 29.03.2019, 

