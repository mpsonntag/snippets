# move files to nixworks
https://github.com/G-Node/nixworks

## nix-mne
https://github.com/G-Node/nix-mne
- create `nixworks/converters/mne`
- migrate `readrawnix.py` and `mnetonix.py`;
- maybe rename both to `nix2mne.py` and `mne2nix.py`?
- should we migrate the examples to `nixworks/converters/mne/resources`?
- installable command line scripts?

- what to do with the repository
  - There are additional files in there e.g. ./new_experiment_workflow.pdf
  - update readme and archive repo?

## nix-nwb
- create `nixworks/converters/nwb`
- move `nix2nwb` and `nwb2nix`
- installable command line scripts?

- update readme and archive repo
  - is christian ok with it
  - are there any dependencies we are unaware of

## nix-demo
https://github.com/G-Node/nix-demo

- not sure if this should be integrated into nixworks
- if yes, which folder structure

## mea2nix
https://github.com/G-Node/mea2nix

- private repo
- is there anything to upgrade and migrate to nixworks?
- archive it to make clear that the repo is no longer used?

## nix-examples
https://github.com/G-Node/nix-examples

- is there any code that can be migrated to nix readthedocs?
- add readme with link to nix github repo and nix readthedocs.
- archive this repo

## jnode_nix
https://github.com/G-Node/jnode_nix

- jan: is there any useful code that should be migrated
- should we archive the repo


# nixworks readthedocs and pypi package

- should we create a pypi package

# repos that stay independent

- nix
- nixpy
- nix-odml-converter -> since the code should not live in either of the nix or odml repos
- all bindings repos
