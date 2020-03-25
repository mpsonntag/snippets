TO-SHARE:
https://pad.lqdn.fr/p/nix

general idea: have dependent code repos run tests periodically via github and ci to check if the core libraries have been changed and the changes have broken the dependent code.


# move files to nixworks
https://github.com/G-Node/nixworks

- dependencies optional


## nix-mne
https://github.com/G-Node/nix-mne

-[x] create `nixworks/converters/mne`
-[x] migrate `readrawnix.py` and `mnetonix.py`;
-[x] maybe rename both to `nix2mne.py` and `mne2nix.py`?
-[x] should we migrate the examples to `nixworks/converters/mne/resources` -> no
-[] installable command line scripts? -> check out one CL script per module; create issue on nixworks

- what to do with the repository -> update readme and archive repo!
  -[x] There are additional files in there e.g. ./new_experiment_workflow.pdf -> will not be migrated to nixworks
  -[x] update readme
  -[] archive repo


## nix-nwb
https://github.com/G-Node/nix-nwb

-[x] create `nixworks/converters/nwb`
-[x] move `nix2nwb` and `nwb2nix`
-[] installable command line scripts?

- what to do with the repo -> update readme and archive repo!
  -[] is christian ok with editing, moving, archiving
  -[x] are there any dependencies we are unaware of -> Jan linked the repo so it should be kept as long as the readme points to the current dev point
  -[x] update readme
  -[] archive repo


## jnode_nix
https://github.com/G-Node/jnode_nix

- is there any useful code that should be migrated -> code outdated, surpassed by wagatonix
- should we archive the repo -> yes

-[x] update readme and point to wagatonix
-[] archive repo


## mea2nix (private repo)
https://github.com/G-Node/mea2nix

- is there anything to upgrade and migrate to nixworks?
- archive it to make clear that the repo is no longer used?

-> leave as is


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
