#!/usr/bin/env bash

ENV_FILE=/home/$USER/Chaos/staging/stats/server_env
STATS_FILE=/home/$USER/Chaos/staging/stats/report.md

source "${ENV_FILE}"

# append to report
echo "" >> "${STATS_FILE}"
echo "" >> "${STATS_FILE}"
echo "... Report $(date '+%Y-%m-%d %H:%M')" >> "${STATS_FILE}"

# check backups
echo "" >> "${STATS_FILE}"
echo "Backups stats" >> "${STATS_FILE}"
ssh ${SUSER}@${BACKUP} 'ls -lart ${BACKUPLOCATION} | tail -n 5' >> "${STATS_FILE}"

# fetch server space stats
echo "" >> "${STATS_FILE}"
echo "Meta space stat" >> "${STATS_FILE}"
ssh ${SUSER}@${META} 'df -h | grep -v "/dev/loop" | grep -v "tmpfs"' >> "${STATS_FILE}"

# Check docker running status
echo "" >> "${STATS_FILE}"
echo "Meta docker stat" >> "${STATS_FILE}"
ssh ${SUSER}@${META} 'docker ps' >> "${STATS_FILE}"

# Check docker resource status
echo "" >> "${STATS_FILE}"
echo "Meta docker resource stats" >> "${STATS_FILE}"
ssh ${SUSER}@${META} 'docker stats --no-stream' >> "${STATS_FILE}"
