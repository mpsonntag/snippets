#!/usr/bin/env bash

PYENV='/home/msonntag/Chaos/software/pyvirtualenv/'

echo "Removing odML dist folder"
find $PYENV -name "odML*" -exec rm -r -v {} \;

echo "Removing odml folder and additional files"
find $PYENV -name "odml*" -exec rm -r -v {} \;
