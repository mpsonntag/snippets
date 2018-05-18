#!/usr/bin/env bash

echo -- Running odml_conda_deps_reset.sh

echo -- Cleanup previous environments

/home/msonntag/Chaos/software/mconda2/bin/conda remove -n o2 --all -y
/home/msonntag/Chaos/software/mconda2/bin/conda remove -n oui2 --all -y
/home/msonntag/Chaos/software/mconda2/bin/conda remove -n o3 --all -y
/home/msonntag/Chaos/software/mconda2/bin/conda remove -n oui3 --all -y

echo -- Create test environments

/home/msonntag/Chaos/software/mconda2/bin/conda create -n o2 python=2.7 -y
/home/msonntag/Chaos/software/mconda2/bin/conda create -n oui2 python=2.7 -y
/home/msonntag/Chaos/software/mconda2/bin/conda create -n o3 python=3.5 -y
/home/msonntag/Chaos/software/mconda2/bin/conda create -n oui3 python=3.5 -y

echo -- Install dependencies

source /home/msonntag/Chaos/software/mconda2/bin/activate oui2

conda install -c pkgw/label/superseded gtk3 -y
conda install -c conda-forge pygobject -y
conda install -c conda-forge gdk-pixbuf -y
conda install -c pkgw-forge adwaita-icon-theme -y

source /home/msonntag/Chaos/software/mconda2/bin/activate oui3

conda install -c pkgw/label/superseded gtk3 -y
conda install -c conda-forge pygobject -y
conda install -c conda-forge gdk-pixbuf -y
conda install -c pkgw-forge adwaita-icon-theme -y

echo -- List current environments

/home/msonntag/Chaos/software/mconda2/bin/conda info --envs

