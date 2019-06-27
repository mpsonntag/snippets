## Pre-Workshop notes:

question for the tutors:
- are there any parameters they would like to get analysed across courses?
- is there any particular part of the course we should focus on?
- should we do a short git/github tutorial and require students to upload
  there data there or to gin?
- is there a specific part / topic that might be helpful to students and that
  we should focus on?

-> if the students are required to save defined parameters in a standardized way,
these kind of analysis should not be hard to do.

question for the students:

why is consistent recording, structuring of data necessary:

in your context there are a couple of cases to consider:
a) personal stake: when you write the protocol for this course not tomorrow, but in one or two weeks from now
   (I've heard it happen, that protocols arrive half a year later...)
   you need to remember the details of the experiment to make sense of the resulting
   data.
   this means saving the raw data + stimulus data + analysis data + metadata (information 
   how the experiment was conducted and which equipment and ingredients were used)
b) the protocol - and subsequently the underlying data - needs to be understandable
   by the ones trying to make sense out of your results. in your case your tutors, 
   in the larger sense it will be your PIs or your reviewers -> how can they
   review the data, if they do not have access to proprietory software.

c) comparative analysis - when trying to figure out if a procedure works well
   multiple same experiments from various experimenters need to be compared
   e.g. to see if antibodies for the same question perform differently - 
   in your case your data and metadata should be uniformly saved so that comparisons
   across all your results can be possible, ideally in an automated fashion.


- you should be provided with a pre-defined description of the setups you use.
  but you should check if all components and settings that you use are actually 
  the same as in the documented form.
  In a real experiment it will be up to you to make sure that the
  setup is properly prepared and your experiment properly documented 
  in case of "debugging" you stumble across unexpected results or 
  figure out that a specific setup had issues and need to figure out
  which results can be used and which have to be discarded. Without
  proper documentation that might not be possible and you will need to
  discard more data then you might have otherwise.
  
  ideally a lab has such a set of reusable documentation prepared for 
  every setup and variations thereof, but it is up to the user to
  use and verify such templates with every use.

  Use checklists to fight against sloppy routines and attach them to
  your labbook / reports.


### Immunohistochemistry

Metadata part:
- date, experiment title and brief desc, experimenter
- experimental conditions: organic material (mouse), age, temperature
- Antibodies; primary and secondary (chicken, rabbit, mouse, goat)
- Staining Protocols
- Microscope setups
- Results

### MEA retina recordings

is this experiment actually performed within the scope of the practical course? [???]

Metadata part:
- date, experiment title and brief desc, experimenter
- experimental conditions: organic material (chicken), age, temperature, which piece of the eye?
- MEA
- LED
- Whole setup (cfg "Chicken retina skript: Overall layout of the setup")
- Stimulus protocols (software MCStim)
- buffer solutions
- software used
  - Operating system; version; build/update state
  - MCStim; version
  - MCRack recorder; version

- Raw data are MEA voltage traces stored on disk
- Analysis is done online during the course of two days using specific software
  -> what are the raw and analysed data output formats [???]


Information from the scriptum:

Recording
o MEAs with 0.2 mm spacing and 30 μm electrode diameter, 60 electrodes
o MEA1060 recording system (Multi Channel Systems, Reutlingen, Germany), 10-3200 Hz
bandpass filter, sampling frequency 25 kHz
o MCRack recording software (Multi Channel Systems, Reutlingen, Germany)

Stimulation
o Function generator: STG2004 (Multi Channel Systems, Reutlingen, Germany) with control
software MCStim.
o Current amplifier for STG
o LED array, max. 6000 cd per LED; projected at 100:1 onto the retina, attenuated with a neutral
density filter


### Patch clamp recordings

Metadata part:
- date, experiment title and brief desc, experimenter
- experimental conditions: organic material (cells, rat cortex), age (DIV), temperature
- buffers used - either full documentation or reference to a specific lab table / notebook
- pipettes used documentation and description of used in which experiment
- setup documentation
- software spike2
- stimulation protocols [???]



Table 1 Information about the different cells, as age, temperature, pipette resistance and access resistance.
Cell1
Cell1
Cell2
Cell3
Age [days]
22
22
13
23
Temperature [°C]
23.9
30.3
23.4
22.7
R pip [MΩ]
11
11
8
5
R access [MΩ]
33
48
29
21

Table 2 Calculation of the cell size by using the capacitance of each cell (0.9 μF/cm2)
Cell 1
Cell 2
Cell 3
Capacitance [pF]
106.97
62.75
38.6
Size [μm2]
11885.56
6972.22
4288.89


#### Ad Fig 3

NIX: voltage vs time traces at different temperatures; stimulus data array, stimulus onset and offset

DataArray: specific temperature
probably sampled dimension
- units: ms and mV
- label: Time [ms]; Voltage [mV]
- dimension: sampling interval (ms)
- name/type/definition: temperature

DataArray ... different temp
DataArray ... different temp
DataArray ... different temp

DataArray ... stimulus protocol
- units: ??? probably ms
- label: ???
- dimension: ??? probably irregularly sampled

MultiTag + Feature to link stimulus to all data arrays

#### Ad Fig 4

NIX: Raw traces of the response to low and high current injections at different temperatures

#### Ad Fig 6 TTX application

Analysis via Matlab


### LFP

Metadata part:
- date, experiment title and brief desc, experimenter
- experimental conditions: organic material (rat hippocampal slices), age (rat and slice), temperature
- buffers used - either full documentation or reference to a specific lab table / notebook
- setup documentation
- stimulation protocols [???]
- Matlab version; script documentation; figure creation documentation [???]


#### Recordings A
Recording of the stimulus intensity/response relation in a paired-pulse-facilitation
paradigm after electrical stimulation in CA3.

#### Recordings B
Recording of the pulse latency/response relation in a paired-pulse-facilitation
paradigm after electrical stimulation in CA3.

#### Recordings C
Induction of long-term-potentiation

Ideally each DataArray is connected to a metadata section/property that references
the script used to generate the data



Analysis via Matlab


toDo: read into script and results again: which stimulus, how could the different 
results be represented in NIX.




# 26.06.2019

08:30 - 18:00

- gnode: talk with Ulricht Egert re workshop
- gnode: talk wih Diego ... re Data Management in his project
- gnode: first day of the practical course
- gnode: sanitizing notes
- gnode: email to Claude duppe re gnode banner



- Brief talk with Ulrich Egert outlining the course and some of the problems they face:
  - LTP: slice orientation for analysis; need to be documented when recording
  - LTP: should properly record the area they are recording in or stimulate
  - LTP: properly annotating graphs ... always fun
  - LTP: tying stimulus to recording data, recording times
  - LTP: properly documenting the analysis steps e.g. normalizing two potentials
  - LTP: always note the absolute time when changes occur or are introduced!
  - LTP: of course always note the absolute time when a recording starts!

- templates could make sense, but need to be taylored to the course so that the students still 
  think about the xperiment and what they are actually doing and not just tick off boxes in lists.

- tell the students its ok to be lost during this experiment since its complex and usually people need
  some time to be able to do things on their own.
  Therefore they will be provided with a template that contains non changing information for future 
  reference and documentation of the experiment. They still have to note which settings they use
  and if they change any settings over the course on an experiment! That is not specific to this
  particular experiment but true for all types of experiments:
  - make templates for recurring settings that can also be shared within a lab or with collaborators, 
    but never forget to record changes in an experiment in addition.
- ask the students at the end of the course where they had troubles recording metadata and in hindsight what 
  they should have recorded from the beginning.


- Brief introduction to Diego ... who is running the immunohisto part of the course

[Q] when recording LTP or patch clamp, can they distinguish cell types by form?


## Immunohistology

- when doing a stimulus in an area note where that stimulus would come from naturally ... might be a note(?)
  for the students
  - EC connections into both DG and CA3 ... when stimulating there what should the results be based on the
    site of excitation.
  - EC connections into CA1
- where are the eyes anatomically speaking with respect to a brain slice

- have a metadata schema/template for the experiment to show them how it would be done and could be used
- give every experiment a number so you can refer to it e.g. A###_custom_name

- Slices are from WT and BomC-eGFP expressing mice
- all female
- WT
  - sex: female
  - slice-condition: fresh prepared
  - age: 8 weeks
  - thickness: 50um
  - slices: [frontal, horizontal]
- BomC-eGFP
  - sex: female
  - slice-condition: from frozen brains (2013)
  - age: not mature - exact age not known
  - thickness: 50um
  - slices: horizontal
  
Antibody combinations:
- Antibodies:
  - names
  - vendor
  - concentration used in experiment
  - equations used?
  - protocol used should be referred somehow within this documentation e.g. by having a reference number or name
    for the protocol


come up with an odML example in YAML documenting the experiment

S Slices used
  S Slice 
   P temporal
  S Slice
   P

S Antibodies used
  S Antibody name
    P name
    P vendor

S Protocols used
  S Protocol name
    P reference

S Experiments
  S Experiment Histo A
    Prop slice horizontal
    Prop slice frontal
    S AB pairing A
      Prop AB name A
       V [AB 1, AB 2]
      Prop AB concentration
       V [v1, v2]
  S Experiment Histo B


table in odml? check odmltables paper or odmltables

There are two sides to this story:
- students @ a course ... use your brain and figure out what is important to document
- show routine in a lab and examples how to make it easier from the start ... show structured example how to collect all necessary data


2nd part of the experiment:
Nissl staining:

- nissl_stain/experiment 
    - exerimenters []
    - date

    - frontal slices
      - slide 1
      - subject:
          - organism: mouse
          - strain: WT
          - sex:
          - age:
          - tissue:
              - typ: slice:
              - origin:
              - preparation:
    - horizontal slices
      - slides 1 & 2
      - animal: mouse
      - strain: WT
      - sex: ?
      - age: ?
      - slice origin: fresh prepared


## outside the course:

Brief overview of the work Diego is doing:
Works on epileptic mice (WT?) at the medical university of Freiburg and also fetches his data from there
- induce seizures by injecting butyric acid (?) into a brain region
- transfect this region with optogenetic viruses (optional?)
- do electrophysiology later in this brain region where due to the acid damage seizures start
- after the mice have been sacrificed, they also do fluorescent microscopy on brain slices of the region on interest

- goal check whether seizures can a) be indentfied when they start and b) suppress them by using theta wave like 
  excitation in the region.

Has a specific data management setup:
Data
- raw (all data files categorized by data type)
-- InVivo/
-- Microscope/ ... czi ... zeiss images and JPGs ... medical university usually just exports JPGs of all color channels and deletes the czi files due to file sizes
-- Tracking/ (Behavior)

- Project ACCESS/
-- KA437/ [mouse_name]
---- ephys data files
-- Config/
---- stimulation files
-- Clinic_spreadsheet ... containing recording session notes according to mouse_name
-- Animal_spreadsheet ... file keeping track of procedures done according to mouse_name
-- Analysis_all ... more detailled descrption of procedures and sessions done according to mouse_name

Ideally the university clinic captures all information required in a spreadsheet that can be converted into an odML file


Diego ... Brazil, automation engineer, that after working went back to science, specifically ephys 


## odML as build and management tool

Discussion with Ulrich Egert:



# 27.06.2019


## Notes patch clamp


- turn on amplifier
- prep cell cultures for recording
- pull pipettes ... document pipette protocol ?
-- document type of pipette used - refer to protocol
- setup of the ephys apparatus
-- heating for medium; Multichannel systems
-- ground
-- pipette / electrode attachement

- document cell culture contamination?

- pump/succion/liquid exchange settings?

- Medium thermostat settings should be recorded
    - 25.6dC ... will go up to 40?

- turn on
-- voltage clamp (Axon instruments)
-- Oscilloscope (Rigol)
-- Microscope camera -- Hammamatsu
-- Software Spike 2
--- for stimulus and recording
--- Test pulse: to check pipette resistance in general

- Axoclamp: all settings 0
- check pipette tip:
-- move objective into solution and identify a good cell
-- move objective up as far as the solution still sticks to the objective and increase brightness
-- put pressure into pipette
-- move pipette into solution and bring it into focus, check the tip is not blocked
-- move pipette tip close to cells and figure out pipette resistance



in general: do a PhD when your'e 60!


