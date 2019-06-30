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

A general idea is to use the metadata of a project as the project management tool to keep control
of the actual data and scripts:

when the odml file is opened, a control layer on top of the core library (ideally a GUI) will
check 
- whether all files listed within an odml file are available
- when there are script, then they should be executed if possible
- listed files should be checked against a saved checksum, that is also saved within
  the odml file next to the file location to see, if a file has changed or is missing alltogether
  which needs to be reported back to the user
- comparison with Mendeley deduplication as well - to reduce 
  
This idea might be out of the scope of the current odML project, but adding custom validators,
that check whether a file is available or if it has changed (providing the checksum is available)
should be doable.

Freeform notes:
- Use an additional layer on top of odML core
- basically use odML as build tool
- if a file path is provided in an odML file, add a checksum and validate this checksum everytime
  the odML file is opened and the filepath is available. If not available provide messasge to the user;
  if checksum does not match, do the same and ask user for feedback.
- basically odML as container which files belong to an experiment and odML file checks which of the linked
  files are available
- what we can do for sure: add a validator to odML that checks if provided files paths in an odML file are
  available on the current system and also checks whether a checksum matches.


# 27.06.2019

09:00 - 18:30


## Notes patch clamp


- turn on amplifier
- prep cell cultures for recording
  - document cell culture contamination? at least cell culture status notes
- pull pipettes ... document pipette protocol ?
-- document type of pipette used - refer to protocol
- setup of the ephys apparatus
-- heating for medium; Multichannel systems
-- Medium thermostat settings should be recorded
   - 25.6dC ... will go up to 40?
-- ground
-- pipette / electrode attachment

- pump/succion/liquid exchange settings?

- turn on
-- voltage clamp (Axon instruments)
   - note which Microelectrode channel? is used for the experiment: #1
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
-- move pipette into solution and bring it into focus, check that the tip is not blocked
-- move pipette tip close to cells, figure out and note pipette resistance
   e.g. pipette resistance: Rpip 3MOhm which is quite low
-- when close to cells run spike2 step pulse and check Oscilloscope voltage and current traces;
   the step should be visible there.
-- adjust holding position on Axoclamp in Bridge mode? until 0mV Vm is reached
-- check pulse on Oscilloscope, switch to SEVC on Axoclamp and adjust current with offset
-- what should the pressure in the pipette be before attaching? around 30-50bar?
-- position electrode on selected cell so that a "dimple" in the cell membrane is visible, open electrode pressure valve
   to attach to cell
-- check oscilloscope for "flat line", now the voltage should change so that we acchieve the "Gigaseal" resistance
-- Note Vm and I after attachment: Vm = -60mV, I = 0.01nA
-- Apply suction to the electrode until cell membrane ruptures and the signal on the oscilloscope changes again
   Note: Vm = -60mV, V2=16mV
-- switch from SEVC to Bridge
-- [N] adjust DC Current command on Microelectrode to get a good reading on the Oscilloscope
-- [N] On Spike2 move to pulse protocol
-- Note temperature in cell suspension at the time of the beginning of the experiment
   -- [N] Tsuspension = 35dC
-- [N] Also note when the Coverslip was first put out of the cell culture; note time of beginning of every experiment!
-- [N] Spike2: 500ms pulse ... current pulse, 1s pause, protocol "P"
-- membrane potential readout ~-50mV
-- manually applying current in addition to the pulse via the Filter
-- cell done

- have all pulse protocols and the pipette protocol in the scriptum appendix so students can refer to it in metadata?
- notes regarding the protocol:
-- ideally there is an in lab library containing all used protocols with an ID. additionally, any used protocol should
   reside with its ID number right next to the data files that were created with this stimulus protocol:
   this ensures that we can trace back the original protocol via the ID, but we can always check, if the library protocol
   might have deviated from the protocol used over time - should not happen, but could happen and then in a couple of
   years the results could not be properly interpreted any longer. If the stimulus is missing all together, then
   we have an interpretation problem in any case.

next trial, next pipette, next cell
- all settings on Axoclamp and filter back to 0
-- holding position, DC current, offset and amplifier/filter, axoclamp setting "bridge"
-- look for cell, pressurize pipette, object up, keep solution bridge, move pipette into bridge, find pipette, move tip close to cell
-- activate "zero line protocol" in spike2 ... check how it is actually called in spike2
-- adjust and check oscilloscope for voltage and current trace of stimulus
-- switch axoclamp to SEVC
   - adjust voltage clamp holding position, I to 0 ???
   - switch to bridge and adjust input offset MEL
   - switch SEVC and adjust holding position to I=0/I=0.01nA
   - find signal on Oscilloscope
   - Note Rpip, attach to cell by pipette pressure release, breach cell via pipette suction
- [N] setup:
  - AxoClamp 2B; Current and Voltage Clamp; Axon Instruments
  - Filter system ... lowpass, highpass filter, note filter settings!
    - filter at 3kHz
    - pre Amp Current Injection, adjust offset here, used to apply current?
  - Analog digital converter; Micro1401; CED
    - connects stimulus and recording software with Oscilloscope, Filter and Axoclamp
  - Microscope: Zeiss Axoscope

- cover slips/ cells used:
  - [N] DIV 27
  - hippocampal neurons?
  - rat pups (age?)

next try:
- pipette close to cell
- Bridge, holding position correction Vm to 0
- Rpip 4M Ohm
- switch to SEVC, use Clamp holding position to set I = 0
- Start spike2 test program "A" ... test pulse
- check both U and I in Oscilloscope
- move close in on cell, release pressure
- update clamp holding position (?) and check Oscilloscope for telltale activity trace in current channel (?) ... was
  in the experiment yellow. Telltale activity trace tells that a gigaseal has been formed
- Calculate gigaseal resistance ... Rpatch = 7G Ohm, Vm -60mV, V2 = 15mV, I = 0.02nA
- Break through membrane by suction, check Oscilloscope current trace (yellow) for telltale activity trace
- stop testpulse in Spike2
- switch to Bridge setting and note membrane potential Vm=-65mV
- Note: Raxon is parallel to Rpip
- adjust Oscilloscope util both U and I lines are visible
- Oscilloscope channel 1 was yellow and was Current!
- start second test protocol Spike2 [find out how this one was called]
- adjust MEL input offset
- adjust on filter (3kHz) pre Amp Injection setting to get a membrane resting potential of -50mV in Spike2 recording window
- note absolute time
- run test pulse program [???] for 100s and record
- stop recording, start IF current protocol[?]: should induce spikes ... adjust filter settings (gain of the filter) until cell spikes
- note gain settings on filter
- protocol: 50ms pulse, 1s interval ... due to membrane capacitance the recorded trace should have a sharkfin shape. from this shape 
  tau (latency?) of the cell can be calculated.

IF current - Isteps that are increasing until the cell spikes
- I is incresed via Filter pre Amp Current injection
- recording times Spike2 ... file contains recording start time absolute, but ziy have to note at which relative time the protocol starts. recorded in pA and mV



- when using abbreviations e.g. Vm, note what they mean at least somewhere in the metadata







in general: do a PhD when your'e 60!


