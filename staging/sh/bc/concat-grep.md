#!/usr/bin/env bash

OUTFILE=bc.full.json

# concatenate all gallery web docker logs
cat bc-web*.json > $OUTFILE

grep "BernsteinConference" $OUTFILE > bc.all.json
grep ".pdf" bc.all.json | grep "BernsteinConference/Posters" > bc.pdf.json
grep "BernsteinConference/Posters/wiki/Poster" bc.all.json | grep "Completed" > poster.access.json
grep "BernsteinConference/ContributedTalks/wiki/Contributed" bc.all.json | grep "Completed" > contributed.access.json
grep "BernsteinConference/InvitedTalks/wiki/Invited" bc.all.json | grep "Completed" > invited.access.json
grep "BernsteinConference/Workshops/wiki/Workshop" bc.all.json | grep "Completed" > workshop.access.json
grep "BernsteinConference/Exhibition/wiki/Exhibition" bc.all.json | grep "Completed" > exhibition.access.json
grep "BernsteinConference/ConferenceInformation/wiki" bc.all.json | grep "Completed" > info.access.json
grep "git" bc.all.json > bc.git.json

# use the docker_log_stats.py script to extract statistics from the log files
