#!/usr/bin/env bash

SURVEY_DIR=/home/$USER/Chaos/DL/stat_test

# set up test dir structure
mkdir -vp $SURVEY_DIR/dir_one
mkdir -vp $SURVEY_DIR/dir_two
mkdir -vp $SURVEY_DIR/dir_three

# run stat

stat $SURVEY_DIR

