#!/usr/bin/env bash

ENV_FILE=/home/$USER/Chaos/staging/stats/server_env
STATS_FILE=/home/$USER/Chaos/staging/stats/report.md

source ${ENV_FILE}

# append to report
echo "" >> ${STATS_FILE}
echo "" >> ${STATS_FILE}
date '+%Y-%m-%d %H:%M' >> ${STATS_FILE}

# check backups
echo "" >> ${STATS_FILE}
echo "Backups stats" >> ${STATS_FILE}
ssh ${SUSER}@${BACKUP} 'ls -lart ${BACKUPLOCATION}' >> ${STATS_FILE}

# fetch server space stats
echo "" >> ${STATS_FILE}
echo "Meta space stat" >> ${STATS_FILE}
ssh ${SUSER}@${META} 'df -h' >> ${STATS_FILE}
