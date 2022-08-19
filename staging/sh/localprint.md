#!/usr/bin/env bash

TESTA=AAA
TESTB=BBB
alias blaprint='function __blaprint() { echo "$TESTA $TESTB"; }; __blaprint'
blaprint
TESTB=CCC
blaprint
