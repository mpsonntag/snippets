Used to document the minimal automated tests for `python-odml`, `odmltools` and not fully automated tests for `odml-ui` installations with a special focus on the execution of command line scripts and gui with different local installation methods.
- `pip install .`
- `python setup.py install`

## Automated odml and odmltools tests

It tests
- basic import and file loading and saving
- command line scripts using realistic example files
  - odmlview
  - odmltordf
  - odmlconversion
- the odmltools command line script
  - odmlimportdatacite
- odml-ui
  - installation

## Manual odml-ui tests

To set up conda environments and run local or Test PyPI installations run the script `run_test_matrix.sh` with option `B` from the current directory.
Once set up, the conda environments can be used to manually test `odml-ui` as well.

Activate python installation environment

    CONDA_ENV_SETUP=pyinst
    CONDA_ENV_PIP=pipinst
    ROOT_DIR=$(pwd)
    cd $ROOT_DIR/resources/test_load
    conda activate ${CONDA_ENV_SETUP}
    odmlui

Run the following most tests:
- open `test_load\load_v1.odml.xml`
- check fail message
- import `test_load\load_v1.odml.xml`
- save as `pyi_conv.xml`
- save as `pyi_conv.yaml`
- save as `pyi_conv.json`
- open `pyi_conv.xml`
- open `pyi_conv.yaml`
- open `pyi_conv.json`
- check importing a terminology using the document wizard

Exit and switch to pip environment 

    conda deactivate
    conda activate ${CONDA_ENV_PIP}
    odmlui

Run manual tests again

Test odmltables plugin

    pip install odmltables
    pip install odmltables[gui]
    odmlui

Run the following minimal tests
- open `pyi_conv.xml`
- use odmltables `convert` button, save as csv file
- use odmltables `filter` button

Exit, move back to the root and cleanup

    cd $ROOT_DIR
    conda deactivate
    rm $ROOT_DIR/resources/test_load/load_v1.odml_converted.xml
    rm $ROOT_DIR/resources/test_load/pyi_conv.json
    rm $ROOT_DIR/resources/test_load/pyi_conv.xml
    rm $ROOT_DIR/resources/test_load/pyi_conv.yaml
