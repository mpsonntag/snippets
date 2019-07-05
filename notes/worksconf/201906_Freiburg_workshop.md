Multichannel check mcd reader for files

Check with ljuba if she is interested in compiling a how to deal with specific data to odml cases.

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
-- Analysis_all ... more detailed description of procedures and sessions done according to mouse_name

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

- NOTE: when using abbreviations e.g. Vm, note what they mean at least somewhere in the metadata


# 28.06.2019

08:30 - 18:00
20:00 - 00:00 train


## LTP MEA / Paired pulses facilitation experiment

- [N] document the analysis chain in the metadata
- [N] how to document getting from raw data to analysis result

- get multiple recording data points for each stimulus intensity

- have paired pulses with enough time interval and then shorten interval over time

NOTE/odML: odML as build tool: this actually points to NIX with storage backend where odML contains and checks the data part!

NOTE/general/ for epilepsy: could one induce LTDepression in kez points of the affected network?

NOTE: odML / project folder should be a package that you can hand over to someone to describe the experiment

### LTP experiment

Using two paired pulses besides the titanic stimulus

MEA experiments: 
- setup
  - which electrodes: microschannel systems
  - which solutions used (Buffers)
  - note preparation and setup protocol 
    - T ~ RT
  - Reference electrode
  - MEA amplifier
  - Zeiss microscope
  - Stimulation electrode ... tungsten electrode ... shielded
  - Program MC Rack ... Multichannel systems
  - Operating system: Windows XP

- 1st check all individual MEA electrodes when redocording setup is empty via MC Rack
  - note if noise level is too high ... is currently not recorded
  - baseline noise not recorded for future reference
- these should be stable noise ~+/- 10uV
- use MC Stimulus II to write stimulus protocols

NOTE: why transform a stimulus protocol to odML? you cannot send a labbook! it should be in data

- MC Stim ... Testpulse e.g.

Pulse        | value | unit | time | unit | value | unit | time | unit | value | unit | time | unit | repeat row | repeat group 
------------ | ----- |
rectangular  | 80    | uA   | 160  | us   | -80   | uA   | 160  | us   | 80    | ua   | 160  | us   | 2          | 1
rectangular  | 80    | uA   | 160  | us   | 0     | uA   | 5    | s  

repeat row ... repeat stimulus of current row x times
repeat group ... repeat all rows x times


Different channels:
- Trigger channel ... defines and handles test pulses
- Synchronisation channel ... defines and handles the start of the testpulses to communicate with the recording software [??]
                          ... or tells the stimulus generator how long a stimulus will be and when
- Trigger channel = system channel 1
- Synchronisation channel = system channel 5

The length of the overall stimulus and the non stimulus times need to match the sum defined via the stimulus channel

Pulse       | value | unit | time | unit | value | unit | time | unit
rectangular | 1     |      | 960  | us   | 0     |      | 40   | s

Trigger and syc channels have to have the same overall length

120kHz sampling? Frequency ... for data points ... will lead to 2GB of data points within an hour ... to save space
only snippets around the testpulses will be recorded.

NOTE: templates to not document rationales behind experiments but only how the experiment was conducted!

- stimulus files are saved to "xx.stim" files ... binary files that are used to run the stimulus generator
- stimulus files can be saved in ASCII format

- the MEA used has 60 electrodes in total 12 ... 17, 21 ... 28 ....... 71 ... 78 ... 82 ... 87
- setup
  - buffer heating ... multichannel systems?
- note any electrodes are not usable e.g. #xy

MEAs usually have differences between batches ... these should be documented

NOTE/odML If we have custom validators, there should also be a way to tie a custom validator to a specific template
 ... or they should live within the space of the template itself, but not within the odML document
     e.g. to check if required properties have been properly filled

preparation specifics: absolute time 
 ... note time the experiment started to know delta t to slice preparation
- mouse, black 6, about 4-7 weeks old
- slice: thickness: 400um
- recordings with MC Rack
- Stimulation area ... CA3 [???]
- note image file of slice on top of electrodes
- note where one reference MEA electrode is positioned also in the metadata so that the image is not really required
  for data interpretation

- running the first test pulse ... this is just a single pulse +80/-80uA followed by ???s inactive, repeated indefinitely
  - how often a protocol is executed is actually not in the stimulus protocol, but can be deciffered by looking at
    the data itself. To easier interpret the data, it does not hurt to record this number separateley! 
- again. running the first test pulse protocol while the electrode is lowered closer to the slice, until we
  see a response in MC Rack electrode display

- problem with the MEA, a single electrode seems to be on contact with the chip, but the contact to the apparatus
  seems to have a problem - [N] should be a note in the metadata regarding the used MEA
  - [N] electrode #38 was not connected due to dirt in the apparatus connection to the chip readout

NOTE: Describe everything that is not written down, is implicit knowledge that can be learned by
interpreting the data, but would make understanding easier by writing it down at the proper place in the
metadata in the first place ... do your future me a favor when she tries to figure out what the data means

- recording interrupted, slice was not sufficiently responsive

new slice:
- electrode was lowered towards CA1?? CA3?? - between 37, 47, 38 and 48 (but actually flipped in the 33/34 range)
- Note for slice status: bright region over electrodes #65-75 ... 68-78; might have been tissue damage
- recording:
  - MC Rack recorder
    - Set recording window in recorder ... 180ms
    - start recording, will wait for the first trigger pulse from MC Stim sync channel
    - [N] sampling rate can be set in MC Rack ... usually stays the same during all experiments/recordings, but should 
      be noted for easier understanding
    - recording metadata will be exported with the recorded file "xy.mcd"
- setup
  - STG2004 Multichannel systems trigger / stimulus generator?
  - Zeiss microscope IM35
- Note recording output file name as it will be in the data repository
NOTE/odML: and here it makes total sense to check for filenames if an odML file will be opened - can easily happen between 
recording setup where an odML file might be started and data management later on, that the filenames change in these 
steps - and probably this change will not make it to the odml file...
NOTE/odML: could have a "checksum" property that will always be added, if a "filename" property is present and the file
is available - or checked, if a checksum already exists.
I like the idea of odML as a control tool for repositories more and more ... could have "project" and "viewing" modes
to ignore missing files messages, checks and validations.
- time between placing the slice in the setup and starting a recording
- time between preparing the slice and starting a recording
- file name "exp2_long.mcd"

- next experiment ... tripple Paired pulses over time
- set window to -30ms, 400ms length for recording windows
- [N] recording note: could be a problem with the fluid system, slice might be under oxygenated.

- next experiment ... filename "exp3_LTP.mcd"
- window -30ms / 190ms recording window
- trigger 1
- y axis ... uV
- recording time 15:47 ... 16:41
- tetanus stimulus ... "xy.stim" - 100Hz pulse in 1 second with 
- LTP stimulus ... "xy.stim"
- 15 interval pulses before tetanus 

- Tetanus ... shut off continuous mode for this signal - we only want 1 s of it

- at sweep 16 we stop the initial pulses and start tetanus pulse
- when done, restart initial pulses with continuous mode (repeat stim indefinitely)
- at sweep 22 start the 2nd tetanus w/o continuous mode
- start test pulse after tetanus again with continuous mode
- did not record num of sweeps after that one


- next experiment ... "exp2_3_KN.mcd"
- recording window -30ms / 190ms
- start 16:43 with testpulse, 11th sweep
- do a buffer switch to kunairic acid (???) ... wait until postsynaptic component in graph is gone


- exp23_long_KA.mcd
- recording temperature [N] 26.3 dC
- exp2_long_art.stm with standard intervals
- window start -30ms, length 180ms, 105 sweeps (3*5*7)

- same for exp23_short_art.stm
- window start -30, 530ms length, 35 sweeps

- Tetanus artifact recording, window -30ms, 10 sweeps

- add TTX to solution while solution exchange is stopped and keep stopped
  - concentration? volume?
- same as for KA recordings

- [N] location of the stimulus electrode: between electrodes 32, 42, 31, 41?
- [N] Name of the image displaying the electrode position and the slice orientation



NOTE: there is much additional data where it makes sense beside the initial data analysis to record it. but it
can easily get out of hand and requires structured recording - ideally checklists that have to be filled every time 
an experiment is run to make sure all metadata will be recorded. think about this list once before an experiment,
try it out, finetune it, and then keep it constant without deviating from it.

NOTE: and with respect to the paragraph above, it might also make sense to give every template a version number,
since templates probably evolve in time as well...

NOTE: think about what makes most sense to have as the root of an odml tree - experiment? animal? project? trial?
And give all pros and cons for the variants.


# 30.06.2019

19:00 - 23:30 train, documentation


# 01.07.2019

08:30 - 18:30 / 22:30 - 00:00

Matlab MEA toolbox for analysis

- Matlab 2007a



- which sweeps need to be analysed?
  - 3x5x7 = 105 sweeps
  - which pulses to average
        1,4,... |
        2,5,... | ... isolating individual artifacts from the individual sweeps that can be averaged:
        3,6,... |      1st, 2nd and 3rd artifact in a stimulus sweep
  - 20s interval: first 15 sweeps

NOTE: when using a script, then either write down ALL used parameters OR use a parameter file that is dated and 
  described in the metadata ... but needs to be independent from the script to ensure that a reused script does not
  contain changed parameters.

MEA Tools: Matlab toolbox
- extract LFP features, works with averaged artifacts from mcd files

- exp2_long.mcd ... load with Matlab
- MEA tools ... plot subplots for 8x8 MEA
- Load control, KA, TTX mcd in Matlab and load via MEA toolbox 8x8 plot into same plot windows with different colors
  - add legend to distinguish. note filename.
- when subtracting TTX from KA we get presynaptic component of LFP
- select interval start by sweep in subplots
- document the subplot settings
- loading various long sweeps, every 15 sweeps:
  - 16,...61,71,91
  - 6, 11, 16

- subplots can change axis resolution
- [N] there seems to be a shift in the data for unknown reasons

- electrode was in CA1
- electrode #25 was in CA3

- save plots as mat figure - these should be linked in metadata with the parameters used to create them

- sweep ids to average in experiment 2:
    - avgid_long = [1,4,7,10,13,...]
    - avgid_short = num2cell(reshape(1:35,5,7),1)
- avgids in matlab workspace, open MEATools and use average

- total of 21 averages ... 3*7
- average across sets of triggered sweeps
- save target variable in workspace

- [N] MEA Tools version 2.8

NOTE: when analysing - get someone unfamiliar with your experiment and let them redo the analysis with your notes.
see if they are able to come to the same results w/o problems. when there are problems, these are the points that
still need to be documented.

- LFP tools - file handling - loads recording files or averages into MEA workspace

- exp2_short.mcd - MEA tools - average - provide avgid_xy variable

- exp2_short_KA.mcd ... avgid_short
- outvar ... exp2_short_KA_avg

- MEA Tools Plot MxN
  - datasource e.g. exp2_short_KA_avg
  - blue ... control    |
  - red ... KA          |  ...  legend has to be added manually to a subplot
  - green ... TTX       |

- how the average sweeps were created and the legend should be put in a script fle and linked

- MEA Tools MxN Plot

- input: exp2_short_(control/KA/TTX)_avg is used as the datasource in the MxN plot
- sweep 3
- legend('ctrl','KA','TTX')
- output filename: exp2_short_20s_sweep3_avg_8x8.fig

- again for sweep 7 ... same legend
- output filename: exp2_short_80ms_sweep7_avg_8x8.fig


- Plot presynaptic part of transmission
  - input: (exp2_long_KA_avg;;1) - (exp2_long_TTX_avg;;1)
  - sweep 1

  - input: exp2_short_KA_avg - exp2_short_TTX_avg
  - sweep 3

  - input: exp2_short_KA_avg - exp2_short_TTX_avg
  - sweep 7

Note: ideally the plot creating part is automated with a script, which also already writes to an odML file, that
cna be copy pasted or loaded. This is a good part to show the students how practical scripting is ... everything 
is documented and less tedious and error prone; no more copy paste errors.

NOTE/odML: sub odML using the following on file: <doc><sec><prop> or <odoc><osec><oprop> to reduce file size


Extract LFP features:

Automatically identifying maxima and minima after stimulus

- sweeps 1 4 7 10 13 ... were averaged
- sweeps 2 5 8 11 14 ... were averaged

- avgid_long ... check m code snippet
- avgid_short ... check m code snippet

Open MEA extract LFP features
form variables:
- input file
- trigger_position
- sweep_range_ID
- evaluation time window
- result variable
- subtraction template artifacts and atrifact_index

non changing form variables
- data_range_limits = [ms]
- filter_type Savizky-Golany
- filter_config [15 3]
- trigger_electrode 2?
- set_artifact_to_none True

- datafile short ... exp2_short_avg
- evaluation_window_extent ... 34ms?
- subtract template ... exp2_short_KA_avg
- index_var/artifact_idx: [1,1,1,1,1]
- trigger_pos 150ms window - 180.64 ???


- [N] Analysis note: trigger/sync seems to be a mismatch ... eval window extent needs to be shorter,
  otherwise the minima detector does not work properly and will detect the test pulse as minima instead 
  of the resposne directly afterwards
  a shift problem occurred at sweep #40

NOTE: as an exercise: reverse engineer a figure using all your notes. write down in reverse order every
parameter used to create the figure.

NOTE/general: Matlab uses \mu for mu

NOTE: use an appendix where the used terms e.g. sweeps, trigger etc are described

NOTE: Maybe an odML file for every figure? and they could be merged for the experiment? or the experiment folder 
includes the sub odML files?

NOTE/odML: only allow full filenames/path for the file check? or allow two path variants side by side, one absolute and
one relative for odML file checks?

NOTE: Its ok if the process of coming up with a metadata scheme takes longer (a month), but come up with it early and 
then use it from this point on.

NOTE/general: could grade a repo in terms of documentation via odML scripts and provide vanity badges, so API could always
check all repos within a lab for documentation quality ... since it is quantified, individuals might put effort into 
it on their own.

odML
- include/link path
  odML mcd
- include/link path
  odML fig

[C] try out include and link

Samora: Postdoc, working with MEA on cell culture "custom" nerve clusters

Katrina: Master? custom beamer projecting into Zeiss microscope to directed activate optogenetically modified cells. Uses
Python and wants to start with git.


LFP experiment:
- load mcd into Matlab, load "D" with MEA, get avg
- LFP feature extraction
- only two pulses in window
- average before tetanus and after

- Setup
  - Rigol Ultra Zoom Digital Oscilloscope

Sweep 16 was first Tetanus, sweep 22 second Tetanus
- sweep 17 should be strong response

NOTE/odML: add links to install conda and pip tutorials on odML for windows readme to help users with installation

NOTE/NIX: does NIX have support for NaN? talked about this, not sure if there is an issue

NOTE: at this point my head is already brimming with ideas for code restructuring, features and how to structure
course data ... hard to focus ... I think I would have needed two more days

NOTE: ask the students to think about an experiment: in a month from now, what will they probably not remember -
is that all written down? name a couple of things that should be additionally documented.

Lists and Scripts!

From a list it is actually not far to an automated script, since UIs have functions that take parameters... simply
call the function directly with the parameter notes in a script. but don't do everything at once, step by step.

NOTE/odML: have cli script for odML file verification + option to rectify file paths

NOTE/odML: do we need a built index for specific field contents in odML e.g. "filename" on load?

NOTE: LFP: let the students use the GUI for a while and then show them the same with a prepared script to show that
everything is documented, makes work less error prone and saves time.

NOTE: you will need to adapt this to your own experiments. There are no standards that apply to every individual experiment

NOTE: if you can, find out, if there is an automated hardware readout so you can automatically add hardware to your
metadata. Otherwise use templates all the time; if you link files in templates use a checksum to make sure that in
comparison over time an empty template has not changed - if it has, it should be renamed to a different template.

NOTE/odML: stupid bug? in odML include: one cannot specify a local absolute or relative path to specify a section to
be included - it always has to be a terminology!
discuss with Jan whether we want a function that actually builds a tree out of many local odML files.



# Tu, 02.07.2019

07:30 - 


NOTE: it would probably have been better, if we had focused on one particular experiment and thoroughly documented 
that one.



Katrin Heinig?
Diego Madado? Viera
Rodrigues Flores
Samora Okujuni:
works on development of in vitro neuronal cell networks, how they change over time and which factors are important
for survival from a cell activity point of view

- already set up a good pipeline from raw data to analysis and has a lot of metadata automatically documented
- should add morphology data documented in odml and might have to move his ephys documentation to odml as well
  - advised to first come up with a feasable scheme for morphology and then write an extractor from matlab to odml
    to merge these two datasets. should not mess around with a pipeline that has been developed over years until
    a parallel pipeline works as good as this.



### Neuro course, Data management part


#### Questions for the tutors
- are there any parameters they would like to get analysed across courses?
- is there a specific part / topic that might be helpful to students and that
  we should focus on?


#### Question for the students:

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

#### General part

where to start

- describe everything that is not written down. There is implicit information and procedural knowledge that can be 
learned by interpreting the data, but it would make understanding an experiment easier by writing it down at the proper 
place in the metadata in the first place ... do your future me a favor when she tries to figure out what the data means

how to start

- when analysing - get someone unfamiliar with your experiment and let them redo the analysis with your notes.
see if they are able to come to the same results w/o problems. when there are problems, these are the points that
still need to be documented.

- why document everything in easy to read files besides raw data, proprietory formats or labbook? You cannot send a 
labbook to a collaborator and you will need this information compiled for a publication in any case.

which details to think about

- give every experiment a number so you can refer to it e.g. A###_custom_name

- a project folder should be a package including as much information about the procedures and how the various data files
and plot were created, that you can hand it over to someone and they could understand the structure and the experimental
process.

- when using abbreviations e.g. Vm, note what they mean at least somewhere in the metadata

- when using a script, then either write down ALL used parameters OR use a parameter file that is dated and 
described in the metadata ... but needs to be independent from the script to ensure that a reused script does not
contain changed parameters.

- think about what makes most sense to have as the root of a file structure. By experiment, animal, project? trial? 
Weigh the pros and cons for the variants.

how to document and automation

- if you can, find out, if there is an automated hardware readout so you can automatically add hardware to your
metadata. Otherwise use templates all the time; if you link files in templates use a checksum to make sure that in
comparison over time an empty template has not changed - if it has, it should be renamed to a different template.

- Lists (Templates) and Scripts! From a template checklist it is actually not far to an automated script, since UIs have functions that take 
parameters... simply call the function directly with the parameter notes in a script. but don't do everything at once, 
step by step.

- Templates  are note meant to document rationales behind experiments but how the experiment was conducted!

- there is much additional data where it makes sense beside the initial data analysis to record it. but it
can easily get out of hand and requires structured recording - ideally checklists that have to be filled every time 
an experiment is run to make sure all metadata will be recorded. think about this list once before an experiment,
try it out, finetune it, and then keep it constant without deviating from it.

- and with respect to the paragraph above, it might also make sense to give every template a version number,
since templates probably evolve in time as well...

- you will need to adapt this to your own experiments. There are no standards that apply to every individual experiment

- Its ok if the process of coming up with a metadata scheme takes longer (a month), but come up with it early and 
then use it from this point on.


#### During the experiments

- have a metadata schema/template for the experiment to show them how it would be done and could be used

- students should be provided with a pre-defined description of the setups you use.
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

- LFP: let the students use the GUI for a while and then show them the same with a prepared script to show that
everything is documented, makes work less error prone and saves time.

- LFP: ideally the plot creating part is automated with a script, which also already writes to an odML file, that
can be copy pasted or loaded. This is a good part to show the students how practical scripting is ... everything 
is documented and less tedious and error prone; no more copy paste errors.


#### Exercises at the end

- reverse engineer a figure using all your notes. write down in reverse order every
parameter used to create the figure.

- ask the students to think about an experiment: in a month from now, what will they probably not remember -
is that all written down? name a couple of things that should be additionally documented.



## Example XML files

all nodes that define an odml tree and can have parallel branches
exp - animal - region - slice - protokoll - dyeprocess - images
- would be nice to have the process in reverse to travel with the images w/o having to keep other branches e.g. from other images
-> export a leaf to the root

region: should contain a list of available subregions that can mapped to electrode positions or tissue damage

mapping electrodes with region selection and note about tissue damage

- export variante aus einem leaf, um alle   
- kleines skript um aus dem template eine kurzbeschreibung rauszuziehen - bestes feature um die sinnhaftigkeit
  zu vermitteln.

- bei drei gruppen drei odml dateien die man diffen kann - einfach unterschiede zw exp ermitteln.

odml: waere nett einen dateinamen generator aus bestimmten bereits im odml enthaltenen feldern zu generieren.
- waere use case specific - waere eine funktionialitaet die man generalisieren koennte


contact diego and samora re talking about first draft of odML



in general: do a PhD when your'e 60!


