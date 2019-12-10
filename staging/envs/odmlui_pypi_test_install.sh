#!/usr/bin/env bash

echo "-- Running odmlui_pypi_test_install.sh"
echo "-- Using pip at $(which pip)"

pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple -I odml-ui

