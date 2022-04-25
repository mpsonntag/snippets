#!/usr/bin/env bash

# User providing ssh access to all machines noted above.
SSH_USER=$USER
SSH_TARGET=setmachine
BACKUPLOCATION=/set/me

echo ""
echo ""
echo "... Report $(date '+%Y-%m-%d %H:%M')"

# Fetch server information
echo ""
echo "... Server information"
echo "... Server specs"
ssh ${SSH_USER}@${SSH_TARGET} 'hostnamectl | grep -v "ID" && lscpu | grep "^CPU(" && lsmem | grep "Total"'

# Fetch latest backup status
echo ""
echo "... Backup stats"
ssh ${SSH_USER}@${SSH_TARGET} "ls -lart ${BACKUPLOCATION} | tail -n 7"


# Fetch server disc usage stats
echo ""
echo "... Server disc usage stats"

echo ""
echo "... Server space stat"
ssh ${SSH_USER}@${SSH_TARGET} 'df -h | grep -v "/dev/loop" | grep -v "tmpfs"'


# Check docker status
echo ""
echo "... Server docker status"
ssh ${SSH_USER}@{SSH_TARGET} 'docker ps'


# Check docker resource status
echo ""
echo "... Server docker resource status"
ssh ${SSH_USER}@{SSH_TARGET} 'docker stats --no-stream'


# Done
echo ""
echo "... Done"
echo ""