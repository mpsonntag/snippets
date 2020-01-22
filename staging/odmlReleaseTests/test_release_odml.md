# Tests for an odml release

These tests create conda environments for a specified Python release and both `pip` and `setup.py` installation of local `python-odml` library source code.

Create conda environments for both installation options

## Basic setup

    PYVER=3.5
    ODML_SOURCE=/home/$USER/Chaos/work/python-odml
    CURR_DIR=$(pwd)

    echo "cleanup and create python setup install environment"
    conda remove -n pyinst --all -y
    conda create -n pyinst python=$PYVER -y
    conda activate pyinst
    pip install --upgrade pip
    pip install ipython
    conda deactivate

    echo "cleanup and create pip install environment"
    conda remove -n pipinst --all -y
    conda create -n pipinst python=$PYVER -y
    conda activate pipinst
    pip install --upgrade pip
    pip install ipython
    conda deactivate

    echo "switching to Python source directory and use both installations"
    cd $ODML_SOURCE
    conda activate pyinst
    python setup.py install
    echo "running tests once"
    python setup.py test
    conda deactivate
    conda activate pipinst
    pip install .
    conda deactivate

    echo "switching back to the test directory"
    cd $CURR_DIR

## Basic ipython tests

Activate python installation environment

    ROOT_DIR=$(pwd)
    cd $ROOT_DIR/resources/test_load
    conda activate pyinst
    echo "Running basic tests"
    python ../scripts/test_odml_basics.py

Exit and switch to pip environment 

    conda deactivate
    conda activate pipinst
    echo "Running basic tests"
    python ../scripts/test_odml_basics.py

Exit and go back to main directory

    conda deactivate
    cd $ROOT_DIR

## Test conversion script

Run tests with the Python setup installation  

    ROOT_DIR=$(pwd)
    OUT_DIR=$ROOT_DIR/resources/out/convert
    mkdir -vp $OUT_DIR
    cd $ROOT_DIR/resources/test_convert_script
    conda activate pyinst
    odmlconvert -o $OUT_DIR -r .
    conda deactivate

Run tests with the pip installation

    conda activate pipinst
    odmlconvert -o $OUT_DIR -r .
    conda deactivate
    cd $ROOT_DIR

## Test rdf export script

Run test with the python install environment  

    ROOT_DIR=$(pwd)
    OUT_DIR=$ROOT_DIR/resources/out/rdf
    mkdir -vp $OUT_DIR
    cd $ROOT_DIR/resources/test_rdf_export_script
    conda activate pyinst
    odmltordf -o $OUT_DIR -r .
    conda deactivate

Run test with the pip install environment

    conda activate pipinst
    odmltordf -o $OUT_DIR -r .
    conda deactivate
    cd $ROOT_DIR

## Test odmlview script

Run test with the python install environment

    ROOT_DIR=$(pwd)
    cd $ROOT_DIR/resources/test_odmlview
    conda activate pyinst
    odmlview --fetch
    odmlview

Run test with the pip install environment

    conda deactivate
    conda activate pipinst
    odmlview --fetch
    odmlview

    # cleanup
    conda deactivate
    cd $ROOT_DIR
    rm $ROOT_DIR/resources/out -r

## Test current PyPI package odml-ui with the built local library

Test if loading, saving and importing of templates/terminologies works

    conda activate pyinst
    conda install -c pkgw/label/superseded gtk3 -y
    conda install -c conda-forge pygobject -y
    conda install -c conda-forge gdk-pixbuf -y
    conda install -c pkgw-forge adwaita-icon-theme -y
    pip install odml-ui
    odmlui

    conda deactivate
    conda activate pipinst
    conda install -c pkgw/label/superseded gtk3 -y
    conda install -c conda-forge pygobject -y
    conda install -c conda-forge gdk-pixbuf -y
    conda install -c pkgw-forge adwaita-icon-theme -y
    pip install odml-ui
    odmlui
