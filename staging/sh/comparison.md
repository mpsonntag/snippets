#!/usr/bin/env bash

ZIPCOMMIT=abcd
DLCOMMIT=abcd

if [[ $ZIPCOMMIT = $DLCOMMIT ]]; then
  echo "... repo is at the DOI request state; commits are identical"
else
  echo "... repo is not at the DOI request state; expected commit: $ZIPCOMMIT; found commit: $DLCOMMIT"
fi
