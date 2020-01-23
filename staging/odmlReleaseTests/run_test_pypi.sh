#!/usr/bin/env bash

echo "-- MAKE SURE TO RUN THIS SCRIPT IN INTERACTIVE MODE '-i' --"

PYVER=3.8
ROOT_DIR=$(pwd)
CONDA_ENV=testpypi

echo "-- Running directory check: ${ROOT_DIR}"
CHECK_DIR=$(basename ${ROOT_DIR})
if [[ ! "$CHECK_DIR" = "odmlReleaseTests" ]]; then
    echo "-- In wrong directory ${ROOT_DIR}"
    exit -1
fi

echo "-- Running active conda env check: ${CONDA_PREFIX}"
if [[ ! -z "${CONDA_PREFIX}" ]]; then
    echo "-- Deactivating conda env: ${CONDA_PREFIX}"
    conda deactivate
fi

echo
echo "-- Cleanup previous conda environment and create new one"
echo
conda remove -q -n ${CONDA_ENV} --all -y

conda create -q -n ${CONDA_ENV} python=${PYVER} -y

conda activate ${CONDA_ENV}
pip install -q --upgrade pip
pip install -q ipython

echo
echo "-- Installing odml from PyPI test"
echo

pip install -q --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple -I odml

echo
echo "-- Installing dependencies and odml-ui from PyPI test"
echo

conda install -q -c pkgw/label/superseded gtk3 -y
conda install -q -c conda-forge pygobject -y
conda install -q -c conda-forge gdk-pixbuf -y
conda install -q -c pkgw-forge adwaita-icon-theme -y

pip install -q --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple -I odml-ui

echo
echo "-- Creating output folder"
OUT_DIR=${ROOT_DIR}/resources/out/convert
mkdir -vp ${OUT_DIR}

echo
echo "-- Running basic tests"
cd ${ROOT_DIR}/resources/test_load
BASIC_SCRIPT=${ROOT_DIR}/resources/scripts/test_odml_basics.py
python ${BASIC_SCRIPT}

if [[ ! $? -eq 0 ]]; then
    cd ${ROOT_DIR}
    conda deactivate
    echo
    echo "-- Encountered error in script ${BASIC_SCRIPT}"
    exit
fi

echo
echo "-- Returning to root"
cd ${ROOT_DIR}

echo "-- Running conversion script tests"
cd ${ROOT_DIR}/resources/test_convert_script
odmlconvert -o ${OUT_DIR} -r .

echo
echo "-- Returning to root"
cd ${ROOT_DIR}

conda deactivate

echo
echo "-- Cleaning up output folder"
rm ${ROOT_DIR}/resources/out -r
echo "-- Done"
echo
