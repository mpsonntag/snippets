#!/usr/bin/env bash

echo
echo "-- MAKE SURE TO RUN THIS SCRIPT IN INTERACTIVE MODE '-i' --"

PY_VER_ARRAY=("|2.7|3.5|3.6|3.7|3.8|")

if [[ $# != 1 ]]; then
    echo
    echo "-- [FAILED] Please provide a valid Python version: ${PY_VER_ARRAY}"
    exit 1
fi

PYVER=$1

if [[ ! "${PY_VER_ARRAY}" =~ "|${PYVER}|" ]]; then
    echo
    echo "-- [FAILED] Please provide a valid Python version: ${PY_VER_ARRAY}"
    exit 1
fi

echo
echo "-- Using Python version ${PYVER}"

ROOT_DIR=$(pwd)
CONDA_ENV=odmlpip${PYVER}

echo
echo "-- Running directory check: ${ROOT_DIR}"
CHECK_DIR=$(basename ${ROOT_DIR})
if [[ ! "$CHECK_DIR" = "odmlReleaseTests" ]]; then
    echo "-- [FAILED] In wrong directory ${ROOT_DIR}"
    exit 1
fi

echo
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
echo "-- Installing nixodmlconverter from PyPI test"

pip install -q --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple -I nixodmlconverter

if ! [[ -x "$(command -v nixodmlconverter)" ]]; then
    conda deactivate
    cd ${ROOT_DIR}
    echo
    echo "-- [FAILED] nixodmlconverter not installed"
    exit
fi

