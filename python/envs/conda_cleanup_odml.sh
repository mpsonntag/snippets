#!/usr/bin/env bash

CONDA=$HOME'/Chaos/software/mconda2/bin/conda'
if [ $(which conda) ]; then
    CONDA=$(which conda)
fi

echo "-- Running conda_cleanup_odml.sh"
echo "-- Using conda at $CONDA"

echo "-- make sure we are clean and not in an environment."
source deactivate

echo "-- Cleanup previous environments"

$CONDA remove -n o2 --all -y
$CONDA remove -n ot2 --all -y
$CONDA remove -n o3 --all -y
$CONDA remove -n ot3 --all -y

echo "-- Create empty test environments"

$CONDA create -n o2 python=2.7 -y
$CONDA create -n ot2 python=2.7 -y
$CONDA create -n o3 python=3.5 -y
$CONDA create -n ot3 python=3.5 -y

echo "-- List current environments"

$CONDA info --envs

