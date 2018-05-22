#!/usr/bin/env bash

CONDABIN=$HOME'/Chaos/software/mconda2/bin'
if [ $(which conda) ]; then
    CONDABIN=$(which conda)"/bin"
fi

echo "-- Running conda_cleanup_odml.sh"
echo "-- Using conda at $CONDABIN"

echo "-- make sure we are clean and not in an environment."
deactivate

echo "-- Cleanup previous environments"

$CONDABIN/conda remove -n o2 --all -y
$CONDABIN/conda remove -n ot2 --all -y
$CONDABIN/conda remove -n o3 --all -y
$CONDABIN/conda remove -n ot3 --all -y

echo "-- Create empty test environments"

$CONDABIN/conda create -n o2 python=2.7 -y
$CONDABIN/conda create -n ot2 python=2.7 -y
$CONDABIN/conda create -n o3 python=3.5 -y
$CONDABIN/conda create -n ot3 python=3.5 -y

echo "-- List current environments"

$CONDABIN/conda info --envs

