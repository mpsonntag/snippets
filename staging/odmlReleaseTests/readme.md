Used to document the minimal not fully automated tests for `python-odml`, `odmltools` and `odml-ui` installations with a special focus on the execution of command line scripts and gui with different local installation methods.
- `pip install .`
- `python setup.py install`

It tests
- basic import and file loading and saving
- command line scripts using realistic example files
  - odmlview
  - odmltordf
  - odmlconversion
- odmltools command line script
  - odmlimportdatacite
- odml-ui
  - installation
