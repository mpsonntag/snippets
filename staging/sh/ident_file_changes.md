#!/usr/bin/env bash

SURVEY_DIR=/home/$USER/Chaos/DL/stat_test

# set up test dir structure
echo "Setting up test directory structure"
mkdir -vp "$SURVEY_DIR"/dir_one
mkdir -vp "$SURVEY_DIR"/dir_two
mkdir -vp "$SURVEY_DIR"/dir_three
touch "$SURVEY_DIR"/readme.md

# run stat
echo ""
echo "Checking root directory"
stat "$SURVEY_DIR"

# run stat for all dirs
echo ""
echo "Running stat on subdirectories"
for d in "$SURVEY_DIR"/*; do
  echo "Working on $d"
  if [ -d "$d" ]; then
    echo "$d"
    stat "$d"
  fi
done
