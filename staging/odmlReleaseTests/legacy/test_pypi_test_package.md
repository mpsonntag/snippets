# Tests for an odml release

These tests create conda environments for a specified Python release and both `pip` and `setup.py` installation of local `python-odml` library source code.

Create conda environments for both installation options

## Basic setup and running basic tests with the version test matrix

    # make sure we are in the correct folder
    bash -i ./run_test_pypi_matrix.sh

Check the test log files

## Test odmlview script

Activate the required conda environment

    PYVER=3.8
    CONDA_ENV=pypi_test_${PYVER}
    conda activate ${CONDA_ENV} 

Run test with the python install environment

    ROOT_DIR=$(pwd)
    cd $ROOT_DIR/resources/test_odmlview
    odmlview --fetch

## Test current PyPI package odml-ui with the built local library

Test if loading, saving and importing of templates/terminologies works

    cd $ROOT_DIR
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
