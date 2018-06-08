#!/usr/bin/env bash

CONDA=$HOME'/Chaos/software/miniconda2/bin/conda'
if [ $(which conda) ]; then
    CONDA=$(which conda)
fi
CONDABIN=$(echo $CONDA | sed 's/bin\/conda/bin/g')

echo "-- Running odml_conda_deps_reset.sh"
echo "-- Using conda at $CONDA"

echo "-- make sure we are clean and not in an environment."
source deactivate

echo "-- Cleanup previous environments"

$CONDA remove -n o2 --all -y
$CONDA remove -n ot2 --all -y
$CONDA remove -n o3 --all -y
$CONDA remove -n ot3 --all -y

echo "-- Create test environments"

$CONDA create -n o2 python=2.7 -y
$CONDA create -n ot2 python=2.7 -y
$CONDA create -n o3 python=3.5 -y
$CONDA create -n ot3 python=3.5 -y

echo "-- Install dependencies"

source $CONDABIN/activate ot2

conda install -c pkgw/label/superseded gtk3 -y
conda install -c conda-forge pygobject -y
conda install -c conda-forge gdk-pixbuf -y
conda install -c pkgw-forge adwaita-icon-theme -y

if [ $(uname) == "Darwin" ]; then
    echo "-- Setting up conda environment activation script"
    mkdir -p $CONDA_PREFIX/etc/conda/activate.d
    touch $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
    echo '#!/bin/sh' > $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
    echo "" >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
    echo 'export GSETTINGS_SCHEMA_DIR=$CONDA_PREFIX/share/glib-2.0/schemas' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
    echo "" >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh

    mkdir -p $CONDA_PREFIX/etc/conda/deactivate.d
    touch $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
    echo '#!/bin/sh' > $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
    echo "" >> $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
    echo "unset GSETTINGS_SCHEMA_DIR" >> $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
    echo "" >> $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
fi

source $CONDABIN/activate ot3

conda install -c pkgw/label/superseded gtk3 -y
conda install -c conda-forge pygobject -y
conda install -c conda-forge gdk-pixbuf -y
conda install -c pkgw-forge adwaita-icon-theme -y

if [ $(uname) == "Darwin" ]; then
    echo "-- Setting up conda environment activation script"
    mkdir -p $CONDA_PREFIX/etc/conda/activate.d
    touch $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
    echo '#!/bin/sh' > $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
    echo "" >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
    echo 'export GSETTINGS_SCHEMA_DIR=$CONDA_PREFIX/share/glib-2.0/schemas' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
    echo "" >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh

    mkdir -p $CONDA_PREFIX/etc/conda/deactivate.d
    touch $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
    echo '#!/bin/sh' > $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
    echo "" >> $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
    echo "unset GSETTINGS_SCHEMA_DIR" >> $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
    echo "" >> $CONDA_PREFIX/etc/conda/deactivate.d/env_vars.sh
fi

echo "-- List current environments"

$CONDA info --envs

