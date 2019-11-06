Create conda environments for both installation options

## Basic setup

    ODML_SOURCE=/home/$USER/Chaos/work/python-odml
    CURR_DIR=$(pwd)

    # cleanup and create python setup install environment
    conda remove -n pyinst --all -y
    conda create -n pyinst python=3.7 -y
    conda activate pyinst
    pip install ipython
    conda deactivate

    # cleanup and create pip install environment
    conda remove -n pipinst --all -y
    conda create -n pipinst python=3.7 -y
    conda activate pipinst
    pip install ipython
    conda deactivate

    # switch to python source directory and use both installations
    cd $ODML_SOURCE
    conda activate pyinst
    python setup.py install
    conda deactivate
    conda activate pipinst
    pip install .
    conda deactivate

    # switch back to the test directory
    cd $CURR_DIR

## Basic ipython tests

Activate python installation environment

    ROOT_DIR=$(pwd)
    cd $ROOT_DIR/resources/test_load
    conda activate pyinst
    ipython

Run script

    import odml

    doc = odml.load('./load.odml.xml')

    doc.pprint()

    doc = odml.load('./load_v1.odml.xml')

Exit and switch to pip environment 

    conda deactivate
    conda activate pyinst
    ipython

Run script again

    import odml

    doc = odml.load('./load.odml.xml')

    doc.pprint()

    doc = odml.load('./load_v1.odml.xml')

Exit and go back to main directory

    conda deactivate
    cd $ROOT_DIR

## Test conversion script

Run test with the python install enviroment  

    ROOT_DIR=$(pwd)
    OUT_DIR=$ROOT_DIR/resources/out
    mkdir -vp $OUT_DIR
    cd $ROOT_DIR/resources/test_convert_script
    conda activate pyinst
    odmlconvert -o $OUT_DIR -r .
    conda deactivate

Run test with the pip install environment

    conda activate pipinst
    odmlconvert -o $OUT_DIR -r .
    conda deactivate
