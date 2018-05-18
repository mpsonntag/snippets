#!/usr/bin/env bash

PYENV='/home/msonntag/Chaos/software/pyvirtualenv/'

echo "Activating pyenv"
source $PYENV"pymain/bin/activate"

echo "Trying to pip uninstall odml"
pip uninstall odml-ui
pip uninstall odml

deactivate

echo "Activating pyenv3"
source $PYENV"py3main/bin/activate"

echo "Trying to pip uninstall odml"
pip uninstall odml-ui
pip uninstall odml

deactivate

echo "Removing odML dist folder"
find $PYENV -name "odML*" -exec rm -r -v {} \;

echo "Removing odml folder and additional files"
find $PYENV -name "odml*" -exec rm -r -v {} \;
