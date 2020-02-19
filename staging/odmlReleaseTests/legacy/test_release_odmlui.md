# Tests for an odml-ui release

These tests create conda environments for a specified Python release and both `pip` and `setup.py` installation of local `odml-ui` library source code and documents the manual steps for minimal conversion, file loading+saving and loading a terminology via the document wizard.

Create conda environments for both installation options

## Basic setup

    PYVER=3.8
    ODML_SOURCE=/home/$USER/Chaos/work/python-odml
    ODML_UI_SOURCE=/home/$USER/Chaos/work/odml-ui
    CURR_DIR=$(pwd)

    # cleanup and create python setup install environment
    conda remove -n pyinst --all -y
    conda create -n pyinst python=$PYVER -y
    conda activate pyinst
    pip install --upgrade pip
    pip install ipython

    conda install -c pkgw/label/superseded gtk3 -y
    conda install -c conda-forge pygobject -y
    conda install -c conda-forge gdk-pixbuf -y
    conda install -c pkgw-forge adwaita-icon-theme -y
    conda deactivate

    # cleanup and create pip install environment
    conda remove -n pipinst --all -y
    conda create -n pipinst python=$PYVER -y
    conda activate pipinst
    pip install --upgrade pip
    pip install ipython

    conda install -c pkgw/label/superseded gtk3 -y
    conda install -c conda-forge pygobject -y
    conda install -c conda-forge gdk-pixbuf -y
    conda install -c pkgw-forge adwaita-icon-theme -y
    conda deactivate

    # switch to python source directory and use both installations
    cd $ODML_SOURCE
    conda activate pyinst
    python setup.py install
    conda deactivate
    conda activate pipinst
    pip install .
    conda deactivate

    # switch to ui python source dir and use both installations
    cd $ODML_UI_SOURCE
    conda activate pyinst
    python setup.py install
    conda deactivate
    conda activate pipinst
    pip install .
    conda deactivate

    # switch back to the test directory
    cd $CURR_DIR

## Run basic manual tests

Activate python installation environment

    ROOT_DIR=$(pwd)
    cd $ROOT_DIR/resources/test_load
    conda activate pyinst
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
    conda activate pipinst
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
