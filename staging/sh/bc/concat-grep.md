#!/usr/bin/env bash

OUTFILE=bc.full.json

cat bc-web*.json > $OUTFILE

grep "BernsteinConference" $OUTFILE > bc.all.json
grep ".pdf" bc.all.json > bc.pdf.json
grep "BernsteinConference/Posters/wiki/Poster" bc.all.json | grep "Completed" > poster.access.json
grep "BernsteinConference/ContributedTalks/wiki/Contributed" bc.all.json | grep "Completed" > contributed.access.json
grep "BernsteinConference/InvitedTalks/wiki/Invited" bc.all.json | grep "Completed" > invited.access.json
grep "BernsteinConference/Workshops/wiki/Workshop" bc.all.json | grep "Completed" > workshop.access.json
grep "BernsteinConference/Exhibition/wiki/Exhibition" bc.all.json | grep "Completed" > exhibition.access.json
