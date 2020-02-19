# Tests for an odmltools release

These tests create conda environments for a specified Python release and both `pip` and `setup.py` installation of local `odmltools` library source code.

Create conda environments for both installation options

## Basic setup

    PYVER=3.8
    ODML_SOURCE=/home/$USER/Chaos/work/python-odml
    ODMLTOOLS_SOURCE=/home/$USER/Chaos/work/odmltools
    CURR_DIR=$(pwd)

    # cleanup and create python setup install environment
    conda remove -n pyinst --all -y
    conda create -n pyinst python=$PYVER -y
    conda activate pyinst
    pip install --upgrade pip
    pip install ipython
    conda deactivate

    # cleanup and create pip install environment
    conda remove -n pipinst --all -y
    conda create -n pipinst python=$PYVER -y
    conda activate pipinst
    pip install --upgrade pip
    pip install ipython
    conda deactivate

    # switch to python source directory and use both installations
    cd $ODML_SOURCE
    conda activate pyinst
    python setup.py install
    cd $ODMLTOOLS_SOURCE
    python setup.py install
    conda deactivate

    cd $ODML_SOURCE
    conda activate pipinst
    pip install .
    cd $ODMLTOOLS_SOURCE
    pip install .
    conda deactivate

    # switch back to the test directory
    cd $CURR_DIR

## Conversion tests

Run tests with the Python setup installation

    ROOT_DIR=$(pwd)
    OUT_DIR=$ROOT_DIR/out/odmltools
    mkdir -vp $OUT_DIR
    cd $ROOT_DIR/resources/test_odmltools/datacite
    conda activate pyinst
    odmlimportdatacite -o $OUT_DIR -r .
    odmlimportdatacite -o $OUT_DIR -r -f RDF .
    odmlimportdatacite -o $OUT_DIR -r -f YAML .
    odmlimportdatacite -o $OUT_DIR -r -f JSON .
    conda deactivate

Run tests with the pip installation

    conda activate pipinst
    odmlimportdatacite -o $OUT_DIR -r .
    odmlimportdatacite -o $OUT_DIR -r -f RDF .
    odmlimportdatacite -o $OUT_DIR -r -f YAML .
    odmlimportdatacite -o $OUT_DIR -r -f JSON .
    conda deactivate

Move back and cleanup

    cd $ROOT_DIR
    rm $ROOT_DIR/resources/out -r
