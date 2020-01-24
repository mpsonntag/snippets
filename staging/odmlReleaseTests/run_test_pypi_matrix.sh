#!/usr/bin/env bash

echo
echo "-- Running Test PyPI python-odml package test installation matrix"

ROOT_DIR=$(pwd)
LOG_DIR=/tmp/odml/pypi_test_install
SCRIPT=./run_test_pypi.sh

echo
echo "-- Running directory check: ${ROOT_DIR}"
CHECK_DIR=$(basename ${ROOT_DIR})
if [[ ! "${CHECK_DIR}" = "odmlReleaseTests" ]]; then
    echo
    echo "-- In wrong directory ${ROOT_DIR}"
    exit 1
fi

echo
echo "-- Creating log directory ${LOG_DIR}"
mkdir -vp ${LOG_DIR}
if [[ ! -d "${LOG_DIR}" ]]; then
    echo
    echo "-- Cannot find ${LOG_DIR} output directory"
    exit 1
fi

echo
echo "-- Log files of all tests can be found in ${LOG_DIR}"

PYVER=3.8
echo
echo "-- Running script for Python version ${PYVER}"
bash -i ${SCRIPT} ${PYVER} > ${LOG_DIR}/${PYVER}_testrun.log 2>&1

PYVER=3.7
echo
echo "-- Running script for Python version ${PYVER}"
bash -i ${SCRIPT} ${PYVER} > ${LOG_DIR}/${PYVER}_testrun.log 2>&1

PYVER=3.6
echo
echo "-- Running script for Python version ${PYVER}"
bash -i ${SCRIPT} ${PYVER} > ${LOG_DIR}/${PYVER}_testrun.log 2>&1

PYVER=3.5
echo
echo "-- Running script for Python version ${PYVER}"
bash -i ${SCRIPT} ${PYVER} > ${LOG_DIR}/${PYVER}_testrun.log 2>&1

PYVER=2.7
echo
echo "-- Running script for Python version ${PYVER}"
bash -i ${SCRIPT} ${PYVER} > ${LOG_DIR}/${PYVER}_testrun.log 2>&1

echo "-- Done"
