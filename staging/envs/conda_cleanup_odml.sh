#!/usr/bin/env bash

echo "-- Running conda_cleanup_odml.sh"
echo "-- Searching for conda"

if [ $(which conda) ]; then
    CONDA=$(which conda)
fi

if [ ! -e "$CONDA" ]; then
    CONDA=$(find $HOME -type d -path '*/conda/bin')
    if [ -d "$CONDA" ]; then
        CONDA=$(echo "$CONDA/conda")
    fi
fi

if [ ! -e "$CONDA" ]; then
    CONDA=$(find $HOME -type d -path '*/miniconda2/bin')
    if [ -d "$CONDA" ]; then
        CONDA=$(echo "$CONDA/conda")
    fi
fi

if [ ! -e "$CONDA" ]; then
    echo "-- Could not find conda executable"
    exit
fi

echo "-- Using conda at $CONDA"

echo "-- make sure we are clean and not in an environment."
deactivate
$CONDA deactivate

echo "-- Cleanup previous environments"

$CONDA remove -n o2 --all -y
$CONDA remove -n ot2 --all -y
$CONDA remove -n o3 --all -y
$CONDA remove -n ot3 --all -y
$CONDA remove -n ot36 --all -y

echo "-- Create empty test environments"

$CONDA create -n o2 python=2.7 -y
$CONDA create -n ot2 python=2.7 -y
$CONDA create -n o3 python=3.5 -y
$CONDA create -n ot3 python=3.5 -y
$CONDA create -n ot36 python=3.6 -y

echo "-- List current environments"

$CONDA info --envs

