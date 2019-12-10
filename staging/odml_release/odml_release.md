# run this script partially manually to test various features
# and the command line scripts before a new release

PYTHON=python2.7
NAME=release_$PYTHON
TESTHOME=/home/$USER/Chaos/staging
TESTDIR=$TESTHOME/odml_release/testfiles
TESTCONV=$TESTDIR/v1_conv
TESTOUT=$TESTDIR/$NAME/out

# cleanup
conda remove -n $NAME --all -y

# create env
conda create -n $NAME python=$PYTHON -y
condact $NAME

pip install ipython
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple -I odml

mkdir -p $TESTOUT
cd $TESTOUT

# manually from here on

odmlconversion -o $TESTOUT -r $TESTDIR

odmlconvert -o $TESTOUT -r $TESTDIR

odmltordf -o $TESTOUT -r $TESTDIR

odmlview --fetch


# manually test load
import odml
fn = '/home/msonntag/Chaos/staging/odml_release/testfiles/load.odml.xml'
doc = odml.load(fn)
doc.pprint(max_depth=5)

# test odml-ui as well if templates or terminology specifics have changed
conda install -c pkgw/label/superseded gtk3 -y
conda install -c conda-forge pygobject -y
conda install -c conda-forge gdk-pixbuf -y
conda install -c pkgw-forge adwaita-icon-theme -y
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple -I odml-ui

odmlui
