#!/usr/bin/env bash

echo
echo "-- MAKE SURE TO RUN THIS SCRIPT IN INTERACTIVE MODE '-i' --"

ROOT_DIR=$(pwd)

echo
echo "-- Running directory check: ${ROOT_DIR}"
CHECK_DIR=$(basename ${ROOT_DIR})
if [[ ! "${CHECK_DIR}" = "odmlReleaseTests" ]]; then
    echo
    echo "-- In wrong directory ${ROOT_DIR}"
    exit 1
fi

LOG_DIR=/tmp/local_test_odml
mkdir -vp ${LOG_DIR}
if [[ ! -d "${LOG_DIR}" ]]; then
    echo
    echo "-- Cannot find ${LOG_DIR} output directory"
    echo
    exit 1
fi

SCRIPT=./run_local_tests.sh

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
