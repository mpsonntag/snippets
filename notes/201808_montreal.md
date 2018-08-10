incf conference notes

Tom Close - core trust seal ... trusted neuroimaging informatics
https://www.coretrustseal.org/apply/

Camille Maumet, inria - reusable neuroimaging data

https://zenodo.org/

nidm data format
https://github.com/incf-nidash

statistical brain maps
https://neurovault.org/

https://www.openaire.eu/
https://archive.softwareheritage.org/
https://github.com/NeuralEnsemble/NeuroinformaticsTutorial


FAIR talk

https://github.com/bio2rdf

(T) Adding support for interlex to odML(ui)

- use your own scicrunch api key (otherwise the odML user one)
- add feature 'add Section from InterLex term' and 'add Property from InterLex'.

https://scicrunch.org/browse/api-docs/index.html?url=https://scicrunch.org/swagger-docs/swagger.json

e.g. query:

curl -X GET "https://scicrunch.org/api/1/ilx/search/term/electrode?key=ZRt6argPOzoqCwk8ULK5N7agk731VsZy" -H  "accept: application/json"


(T) publish odML RDF/OWL resource!

(T) odML - templates w custom validation rules?


## Collections of tools
nix
https://fairsharing.org/bsg-s001169/
https://scicrunch.org/resources/Any/record/nlx_144509-1/SCR_016196/resolver

odML
https://scicrunch.org/scicrunch/Resources/record/nlx_144509-1/SCR_001376/resolver
(C) referenced by to get a feel for users


(T) nix - nwb(new) converter?


(T) HiWi project - doc and examples for nix n odML

(T) yet another microservice ... sift through nix files of a gin repo and create plots like done in nixview.
    store the resulting graphs as images and provide them on demand in gin? this way we don't directly touch
    files on gin, but in a different service that might fail.

(T) if we are thinking about gin-CI, maybe we can think about running processes on a cluster as well?



