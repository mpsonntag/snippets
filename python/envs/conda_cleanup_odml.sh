#!/usr/bin/env bash

CONDABIN='$CONDABIN'

echo -- Running odml_conda_deps_reset.sh
echo -- make sure we are clean and not in an environment.
source deactivate

echo -- Cleanup previous environments

$CONDABIN/conda remove -n o2 --all -y
$CONDABIN/conda remove -n ot2 --all -y
$CONDABIN/conda remove -n o3 --all -y
$CONDABIN/conda remove -n ot3 --all -y

echo -- Create test environments

$CONDABIN/conda create -n o2 python=2.7 -y
$CONDABIN/conda create -n ot2 python=2.7 -y
$CONDABIN/conda create -n o3 python=3.5 -y
$CONDABIN/conda create -n ot3 python=3.5 -y

echo -- List current environments

$CONDABIN/conda info --envs

