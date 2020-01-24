#!/usr/bin/env bash

echo
echo "-- Running odml test matrix; default local pip install"

ROOT_DIR=$(pwd)
# Eventually upgrade to these; local_pip is the default run
# RUN_MODES=("|local_pip|local_setup|pypi_test|pypi|")
RUN_MODE_ARRAY=("|local_pip|pypi_test|")
RUN_MODE="local_pip"

if [[ ! "${RUN_MODE_ARRAY}" =~ "|${RUN_MODE}|" ]]; then
    echo
    echo "-- Please provide a valid run mode: ${RUN_MODE_ARRAY}"
    exit 1
fi

# -- This run will be default
LOG_DIR=/tmp/odml/local_test
SCRIPT=./run_local_tests.sh

if [[ "${RUN_MODE}" -eq "pypi_test" ]]; then
  LOG_DIR=/tmp/odml/pypi_test_install
  SCRIPT=./run_test_pypi.sh
  echo "-- Running Test PyPI installation matrix"
fi

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
FAIL_COUNT=$(cat ${LOG_DIR}/${PYVER}_testrun.log | grep -c FAILED)
if [[ "${FAIL_COUNT}" -gt 0 ]]; then
    echo "-- Test fail in Python ${PYVER} tests. Check ${LOG_DIR}/${PYVER}_testrun.log"
fi

PYVER=3.7
echo
echo "-- Running script for Python version ${PYVER}"
bash -i ${SCRIPT} ${PYVER} > ${LOG_DIR}/${PYVER}_testrun.log 2>&1
FAIL_COUNT=$(cat ${LOG_DIR}/${PYVER}_testrun.log | grep -c FAILED)
if [[ "${FAIL_COUNT}" -gt 0 ]]; then
    echo "-- Test fail in Python ${PYVER} tests. Check ${LOG_DIR}/${PYVER}_testrun.log"
fi

PYVER=3.6
echo
echo "-- Running script for Python version ${PYVER}"
bash -i ${SCRIPT} ${PYVER} > ${LOG_DIR}/${PYVER}_testrun.log 2>&1
FAIL_COUNT=$(cat ${LOG_DIR}/${PYVER}_testrun.log | grep -c FAILED)
if [[ "${FAIL_COUNT}" -gt 0 ]]; then
    echo "-- Test fail in Python ${PYVER} tests. Check ${LOG_DIR}/${PYVER}_testrun.log"
fi

PYVER=3.5
echo
echo "-- Running script for Python version ${PYVER}"
bash -i ${SCRIPT} ${PYVER} > ${LOG_DIR}/${PYVER}_testrun.log 2>&1
FAIL_COUNT=$(cat ${LOG_DIR}/${PYVER}_testrun.log | grep -c FAILED)
if [[ "${FAIL_COUNT}" -gt 0 ]]; then
    echo "-- Test fail in Python ${PYVER} tests. Check ${LOG_DIR}/${PYVER}_testrun.log"
fi

PYVER=2.7
echo
echo "-- Running script for Python version ${PYVER}"
bash -i ${SCRIPT} ${PYVER} > ${LOG_DIR}/${PYVER}_testrun.log 2>&1
FAIL_COUNT=$(cat ${LOG_DIR}/${PYVER}_testrun.log | grep -c FAILED)
if [[ "${FAIL_COUNT}" -gt 0 ]]; then
    echo "-- Test fail in Python ${PYVER} tests. Check ${LOG_DIR}/${PYVER}_testrun.log"
fi

echo "-- Done"
