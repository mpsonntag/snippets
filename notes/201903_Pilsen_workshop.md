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
[C] Create slides specific for NIX features - with images and everything to make them more
    easily comprehensible - check checklog at the end of this doc for details


# Fr, 29.03.2019, 








### NIX features exmplanations

slightly_smiling_face:
jgrewe [11:28 AM]
they actually break the separation between data and metadata, as also the DataFrame will do
jgrewe [11:35 AM]
regarding the feature, we use them to store stimulus conditions such as the `contrast` of the stimulus that may change with each stimulus presentation.let's assume we record the membrane voltage `V-1` in a 1D regular sampled DataArray and the spike times `spikes` in a (alias)Ranged 1D DataArray. We further have `n` stimuli that each ahve a different `contrast` we store the contrast values in a separate 1D Set DataArray named `contrasts`.
Stimulus epochs are marked using a MTag with `n` positions and extents. The epochs refer to `V-1` and `spikes` (MTag.references). and the MTag also has an `indexed` feature that points to the `contrasts` DataArray.During analysis I can do something like this:

    nstimuli = mtag.positions.shape[0]
    for i in range(nstimuli):
        data = mtag.taggedData(i, 'V-1')[:]
        spikes = mtag.taggedData(i, 'spikes')[:]
        contrast = mtag.featureData(i, 'contrasts')[:]

since `contrasts` it is linked as an `indexed` feature, it will return `contrasts[i, :]` which is a single number, i.e. the actual contrast
more?
achilleas [11:43 AM]
Indexed seems like the most straightforward one then
what about the other two?
(you don't have to if you're busy :slightly_smiling_face: )
jgrewe [11:52 AM]
ok, let's assume The stimulus is complex and I store its waveform in a DataArray called `stimulus` it does not necessarily has to have the same size as `V-1`. For an `untagged` feature the size is actually irrelevant. Let's assume, `V-1` is long with shape (1000 x 1) and the stimulus (`shape=(100,1)`) was presented 5 times `nstims=5`.
So the stimulus was on for `nstims` epochs of the `V-1` recording. The respective MTag references `V-1` with `nstims` position entries and uses `stimulus` as an `untagged` feature.

    nstims = mtag.positions.shape[0]
    for i in range(nstims):
        voltage = mtag.taggedData(i, 'V-1')[:]
        stim = mtag.featureData(i, 'stimulus')[:]

it will always return the same stimulus data `stim.shape == stimulus.shape`
could have explained that simpler... actually the `untagged` feature is the easiest
you want to know more?
jgrewe [12:06 PM]
just for the sake of completeness and we wait for the boss before we go for food: (edited) 
achilleas [12:07 PM]
right, yeah, I REMEMBER THIS (untagged)

jgrewe [12:14 PM]
the trickiest beast is the `tagged` feature because it applies the MTag's `positions` and `extents` to the data linked as a feature. It is meant for a second way of linking between DataArrays.
For example I do record the membrane voltage `V-1` as above and also have a recording of the room `temperature` I stimuluate the cell with a stimulus but I also want to highlight the `temperature` during that epoch, (I did not stimulate the room temperature so it would be nonsensical to suggest a causal relation between the stimulus and the temperature...)
In brief, positions and extent have to be compatible with the dimensionality of an `tagged` feature. I think we are forgiving in the sense that the provided positions must match. That is if `temperature` would be 2D but `positions[i,:]` is only a single number `mtag.featureData(i, 'temperature')`  would return `temperature[indexof(positions[i]): indexof(positions[i] + extents[i]), :]` (edited) 
kind of
