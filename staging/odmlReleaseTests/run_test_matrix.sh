#!/usr/bin/env bash

echo
echo "-- Running python-odml package test installation matrix"

ROOT_DIR=$(pwd)

# Local test installations
# LOG_DIR=/tmp/odml/local_install
# SCRIPT=./run_test_local_odml.sh

# PyPI test odml installations
LOG_DIR=/tmp/odml/pypi_test_install_odml
SCRIPT=./run_test_pypi_odml.sh

# PyPI test odmltools installations
# LOG_DIR=/tmp/odml/pypi_test_install_odmltools
# SCRIPT=./run_test_pypi_odmltools.sh

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

function run_script () {
    echo
    echo "-- Running script for Python version ${PYVER}"
    bash -i ${SCRIPT} ${PYVER} > ${LOG_DIR}/${PYVER}_testrun.log 2>&1
    FAIL_COUNT=$(cat ${LOG_DIR}/${PYVER}_testrun.log | grep -c FAILED)
    if [[ "${FAIL_COUNT}" -gt 0 ]]; then
        echo "-- Test fail in Python ${PYVER} tests. Check ${LOG_DIR}/${PYVER}_testrun.log"
    fi
}

PYVER=3.8
run_script

PYVER=3.7
run_script

PYVER=3.6
run_script

PYVER=3.5
run_script

PYVER=2.7
run_script

echo "-- Done"
