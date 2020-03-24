general idea: have dependent code repos run tests periodically via github and ci to check if the core libraries have been changed and the changes have broken the dependent code.


# move files to nixworks
https://github.com/G-Node/nixworks

- dependencies optional

## nix-mne
https://github.com/G-Node/nix-mne

- create `nixworks/converters/mne`
- migrate `readrawnix.py` and `mnetonix.py`;
- maybe rename both to `nix2mne.py` and `mne2nix.py`?
- should we migrate the examples to `nixworks/converters/mne/resources`?
- installable command line scripts? check out one CL script per module

- what to do with the repository
  - There are additional files in there e.g. ./new_experiment_workflow.pdf
  - update readme and archive repo?

## nix-nwb
https://github.com/G-Node/nix-nwb

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

-> move jupyter notebooks that are up to date to nix-examples
-> update readme and archive the demo repo


## nix-examples
https://github.com/G-Node/nix-examples

-> should be a repo to collect usage examples in different languages: keep repo and add readme
-> add ipython notebook from nix-demo

-> add issue to import library specific docs as git submodules from the code libs

-> Enable recurring CI builds to check if scripts are runnable
-> Update submodules when running builds to make sure newer versions also work (maybe allow failure?)

## mea2nix (private repo)
https://github.com/G-Node/mea2nix

- is there anything to upgrade and migrate to nixworks?
- archive it to make clear that the repo is no longer used?

-> leave as is

## jnode_nix
https://github.com/G-Node/jnode_nix

- jan: is there any useful code that should be migrated
- should we archive the repo

-> archive, point to wagatonix

