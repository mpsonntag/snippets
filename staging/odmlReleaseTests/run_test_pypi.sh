#!/usr/bin/env bash

echo "-- MAKE SURE TO RUN THIS SCRIPT IN INTERACTIVE MODE '-i' --"

PYVER=3.8
ROOT_DIR=$(pwd)

CHECK_DIR=$(basename $ROOT_DIR)
if [ ! "$CHECK_DIR" = "odmlReleaseTests" ]; then
    echo "-- In wrong directory $ROOT_DIR"
    exit -1
fi

CONDA_ENV=testpypi

echo "-- Cleanup and create the conda environment"
conda remove -n $CONDA_ENV --all -y

conda create -n $CONDA_ENV python=$PYVER -y

conda activate $CONDA_ENV
pip install --upgrade pip
pip install ipython

echo "-- Install odml and odml-ui from PyPI test"
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple -I odml

conda install -c pkgw/label/superseded gtk3 -y
conda install -c conda-forge pygobject -y
conda install -c conda-forge gdk-pixbuf -y
conda install -c pkgw-forge adwaita-icon-theme -y

pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple -I odml-ui

conda deactivate

echo "-- Done"
