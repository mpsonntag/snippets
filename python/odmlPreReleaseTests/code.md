Create conda environments for both installation options

## Basic setup

    PYVER=3.7
    ODML_SOURCE=/home/$USER/Chaos/work/python-odml
    CURR_DIR=$(pwd)

    # cleanup and create python setup install environment
    conda remove -n pyinst --all -y
    conda create -n pyinst python=$PYVER -y
    conda activate pyinst
    pip install ipython
    conda deactivate

    # cleanup and create pip install environment
    conda remove -n pipinst --all -y
    conda create -n pipinst python=$PYVER -y
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

    # Test possible imports of all parsers without importing the full odML package
    from odml.tools import ODMLReader, ODMLWriter, RDFReader, RDFWriter
    from odml.tools.converters import FormatConverter, VersionConverter
    from odml.tools import XMLReader, XMLWriter, DictReader, DictWriter
    import odml

    doc = odml.load('./load.odml.xml')

    doc.pprint()

    doc = odml.load('./load_v1.odml.xml')

Exit and switch to pip environment 

    conda deactivate
    conda activate pipinst
    ipython

Run script again

    # Test possible imports of all parsers without importing the full odML package
    from odml.tools import ODMLReader, ODMLWriter, RDFReader, RDFWriter
    from odml.tools.converters import FormatConverter, VersionConverter
    from odml.tools import XMLReader, XMLWriter, DictReader, DictWriter
    import odml

    doc = odml.load('./load.odml.xml')

    doc.pprint()

    doc = odml.load('./load_v1.odml.xml')

Exit and go back to main directory

    conda deactivate
    cd $ROOT_DIR

## Test conversion script

Run test with the python install environment  

    ROOT_DIR=$(pwd)
    OUT_DIR=$ROOT_DIR/resources/out/convert
    mkdir -vp $OUT_DIR
    cd $ROOT_DIR/resources/test_convert_script
    conda activate pyinst
    odmlconvert -o $OUT_DIR -r .
    conda deactivate

Run test with the pip install environment

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

## Test odml-ui

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
