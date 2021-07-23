# various notes for the INCF-NIX workshop 2021

## zimmer data notes

document metamorph metadata
- document the process of how to record metadata of a software
 - document the reasoning
 - document the structure
 - check what we already have in the terminologies/templates

C.elegans ca imaging data in NIX file:

stimulus -> use tags to specify
    - ramp up
    - ramp down
    - resting
    - etc

with this all relevant data is already pre-tagged for future analysis

how to filter e.g. ramp up for a specific species strain as an example

## Metadata documentation
- always store dates!
- software
 - version and name
 - script used - name version
 - type: "software/version"; "software/name"

visualize different metadata tree options - where to attach which info

metadata approaches
- NIX metadata template files
- copy templates from file to other file

(?) NIX file: can we copy metadata templates? ID?
(?) how to nicely display a NIX metadata tree?
(?) does the NIX->odML converter work with the current NIX version?
(?) NIX report -> short table with all features? write this now while exploring the NEO file. export to PNG graph?
(?) function to print full sec-prop tree?

Usage concept: copy metadata from file to file

### Metadata concepts

    - Experiment
    - Software
    - Hardware
    - Stimuli
    - Subjects
    - Protocols

... import existing
- from file
- from server
- from templates/terminologies

Metadata collection approaches

(A) easiest: dump info in one field (sec - prop - value containing everything)
+ easy to do
+ easy to retrieve
- hard to fine grain filter
- hard to reuse
    [s]name [p]name [p]type [p]description -> text

(B) complex tree:
[s] software
  [s] metamorph-versionA
    [p] name
    [p] version
    [s] settings - fixed
  [s] metamorph-versionB
