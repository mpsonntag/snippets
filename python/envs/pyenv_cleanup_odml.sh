#!/usr/bin/env bash

PYLOCAL=$HOME'/.local/'
PYENV=$HOME'/Chaos/software/pyvirtualenv/'

echo "Removing local install"
pip uninstall odml-ui
pip uninstall odml

echo "Activating pyenv"
source $PYENV"pymain/bin/activate"

echo "Trying to pip uninstall odml"
pip uninstall odml-ui
pip uninstall odml

echo "Uninstalling dependencies"
pip uninstall lxml
pip uninstall pyyaml
pip uninstall rdflib

deactivate

echo "Activating pyenv3"
source $PYENV"py3main/bin/activate"

echo "Trying to pip uninstall odml"
pip uninstall odml-ui
pip uninstall odml

echo "Uninstalling dependencies"
pip uninstall lxml
pip uninstall pyyaml
pip uninstall rdflib

deactivate

echo "Removing pyenv odML dist folder"
find $PYENV -name "odML*" -exec rm -r -v -I {} \;

echo "Removing pyenv odml folder and additional files"
find $PYENV -name "odml*" -exec rm -r -v -I {} \;

echo "Removing local odML dist folder"
find $PYLOCAL -name "odML*" -exec rm -r -v -I {} \;

echo "Removing local odml folder and additional files"
find $PYLOCAL -name "odml*" -exec rm -r -v -I {} \;
