#!/usr/bin/env bash

set -eu

# Container specifics
GCAROOT=/home/msonntag/Chaos/DL/gcatest
COMPOSE_PROJECT_NAME=gca_felban

GCAPGRESIMG=postgres:11
GCAIMG=mpsonntag/gca:felban
GCAPGRES=pgres_gca_bee

# Make sure these are the proper installation options
echo "These are the docker installation options:"
echo "Installation path: ${GCAROOT}/${COMPOSE_PROJECT_NAME}"
echo "Docker compose project name: ${COMPOSE_PROJECT_NAME}"
echo "Postgres docker image: ${GCAPGRESIMG}"
echo "Postgres docker name: ${GCAPGRES}"
echo "GCA-Web docker image: ${GCAIMG}"

echo -n "Continue [y/n]: "
read -s continue

if [[ $continue != "y" ]]; then
    echo "User abort"
    exit 1
fi

# Home folder containing data base, config files and figures
# Use the docker container name as directory name all files will live in
GCAHOME=$GCAROOT/$COMPOSE_PROJECT_NAME
GCAENV=$GCAHOME/env
GCALOGS=$GCAHOME/logs

# Set up project data base folders
GCAPGRESDB=$GCAHOME/postgres/
GCASCRIPTS=$GCAHOME/scripts/

# Play framework setup
GCACONF=$GCAHOME/conf/
GCAIMAGES=$GCAHOME/images
GCAFIG=$GCAIMAGES/figures/
GCAFIGMOBILE=$GCAIMAGES/figures_mobile/
GCABANNER=$GCAIMAGES/banners/
GCABANMOBILE=$GCAIMAGES/banners_mobile/
GCABACKUP=$GCAHOME/backup

# Create all required directories
mkdir -p $GCAHOME
mkdir -p $GCAENV
mkdir -p $GCALOGS

mkdir -p $GCAPGRESDB
mkdir -p $GCASCRIPTS

mkdir -p $GCACONF
mkdir -p $GCAFIG
mkdir -p $GCAFIGMOBILE
mkdir -p $GCABANNER
mkdir -p $GCABANMOBILE
mkdir -p $GCABACKUP

# Create docker-compose .env file
echo "COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME}" > $GCAENV/.env
echo "GCAHOME=${GCAHOME}" >> $GCAENV/.env
echo >> $GCAENV/.env
echo "# GCA WEB VARS" >> $GCAENV/.env
echo "GCAIMG=${GCAIMG}" >> $GCAENV/.env
echo >> $GCAENV/.env
echo "# DATABASE VARS" >> $GCAENV/.env
echo "GCAPGRES=${GCAPGRES}" >> $GCAENV/.env
echo "GCAPGRESIMG=${GCAPGRESIMG}" >> $GCAENV/.env
