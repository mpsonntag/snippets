#!/usr/bin/env bash

echo "-- Running conda_install_odmlui_deps.sh"

conda install -c pkgw/label/superseded gtk3 -y
conda install -c conda-forge pygobject -y
conda install -c conda-forge gdk-pixbuf -y
conda install -c pkgw-forge adwaita-icon-theme -y

