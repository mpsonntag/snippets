#!/usr/bin/env bash

echo "-- Searching for conda"

if [ $(which conda) ]; then
    CONDA=$(which conda)
fi

if [ ! $CONDA ]; then
    CONDA=$(find $HOME -type d -path '*/conda/bin')
    if [ -d "$CONDA" ]; then
        CONDA=$(echo "$CONDA/conda")
    fi
fi

if [ ! -d "$CONDA" ]; then
    CONDA=$(find $HOME -type d -path '*/miniconda2/bin')
    if [ -d "$CONDA" ]; then
        CONDA=$(echo "$CONDA/conda")
    fi
fi

if [ ! $CONDA ]; then
    echo "-- Could not find conda executable"
    exit
fi

CONDABIN=$(echo $CONDA | sed 's/bin\/conda/bin/g')

echo "-- Running odml_conda_deps_reset.sh"
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

echo "-- Create test environments"

$CONDA create -n o2 python=2.7 -y
$CONDA create -n ot2 python=2.7 -y
$CONDA create -n o3 python=3.5 -y
$CONDA create -n ot3 python=3.5 -y
$CONDA create -n ot36 python=3.6 -y

echo "-- Install dependencies"

source $CONDABIN/activate ot2

$CONDA install -c pkgw/label/superseded gtk3 -y
$CONDA install -c conda-forge pygobject -y
$CONDA install -c conda-forge gdk-pixbuf -y
$CONDA install -c pkgw-forge adwaita-icon-theme -y

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

$CONDA deactivate

source $CONDABIN/activate ot3

$CONDA install -c pkgw/label/superseded gtk3 -y
$CONDA install -c conda-forge pygobject -y
$CONDA install -c conda-forge gdk-pixbuf -y
$CONDA install -c pkgw-forge adwaita-icon-theme -y

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

$CONDA deactivate

source $CONDABIN/activate ot36

$CONDA install -c pkgw/label/superseded gtk3 -y
$CONDA install -c conda-forge pygobject -y
$CONDA install -c conda-forge gdk-pixbuf -y
$CONDA install -c pkgw-forge adwaita-icon-theme -y

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

$CONDA deactivate

echo "-- List current environments"

$CONDA info --envs

