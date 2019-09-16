## Notes on the G-Node metadata services

what would be good for a more standardized odML usage:

- a core odML construct, that is the same for everyone and
  that should be part of the validation and scream if the data is not
  there. also when uploaded to one of our services it should scream as well
  the marked fields are minimal requirements for upload to the 
  RDF server.
-> check bioinfo platforms, which minimal info is required to upload
  - section "citation"
    - author* (name + email)
    - data repository*
    - title*
    - description tags* e.g. ephys, eeg, brain region, etc. ... we should
    - published/upload date* (if not there, upload date)
    - lab/institute
- a custom part, where people can do whatever they like.

services that we need running:
- a) the meta data service
- b) an upload service for people that do not want to use gin
  - this upload server should support a) odML RDF files b) odML files, c) NIX files
  - [C] mapping python to go so that we may use the python-odml library
        in with the go graphpush server
  - requires minimal info set; see above.
  - the repo URL needs to be accessible
  - [?] should there be a 
- c) a gin related meta service, that enables webhooks to extract odML data from gin and
  uploads it to the meta service - should probably be within the scope of service b) but
  could also be detached, so that the services can run independently.
- d) the meta service should automatically 


- we really need templates for people - thats what they want - reduction of work for them
- ask jan if we can sit together and make a template for electric fish recordings