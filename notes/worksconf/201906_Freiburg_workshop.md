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

- gnode: talk with Ulrich Egert re workshop
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
  think about the experiment and what they are actually doing and not just tick off boxes in lists.

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
- show routine in a lab and examples how to make it easier from the start ... 
  show structured example how to collect all necessary data


2nd part of the experiment:
Nissl staining:

- nissl_stain/experiment 
    - experimenters []
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
Works on epileptic mice (WT?) at the medical university of Freiburg and also fetches 
his data from there
- induce seizures by injecting butyric acid (?) into a brain region
- transfect this region with optogenetic viruses (optional?)
- do electrophysiology later in this brain region where due to the acid damage seizures 
  start
- after the mice have been sacrificed, they also do fluorescent microscopy on brain 
  slices of the region on interest

- goal check whether seizures can a) be indentfied when they start and b) suppress 
  them by using theta wave like excitation in the region.

Has a specific data management setup:
Data
- raw (all data files categorized by data type)
-- InVivo/
-- Microscope/ ... czi ... Zeiss images and JPGs ... medical university usually just 
   exports JPGs of all color channels and deletes the czi files due to file sizes
-- Tracking/ (Behavior)

- Project ACCESS/
-- KA437/ [mouse_name]
---- ephys data files
-- Config/
---- stimulation files
-- Clinic_spreadsheet ... containing recording session notes according to mouse_name
-- Animal_spreadsheet ... file keeping track of procedures done according to mouse_name
-- Analysis_all ... more detailed description of procedures and sessions done according 
   to mouse_name

Ideally the university clinic captures all information required in a spreadsheet that 
can be converted into an odML file


Diego ... Brazil, automation engineer, that after working went back to science, 
specifically ephys 


## odML as build and management tool

Discussion with Ulrich Egert:

A general idea is to use the metadata of a project as the project management tool to keep 
control of the actual data and scripts:

when the odml file is opened, a control layer on top of the core library (ideally a GUI) 
will check 
- whether all files listed within an odml file are available
- when there are script, then they should be executed if possible
- listed files should be checked against a saved checksum, that is also saved within
  the odml file next to the file location to see, if a file has changed or is missing all 
  together which needs to be reported back to the user
- comparison with Mendeley deduplication to ensure not having same files under different 
  names
  
This idea might be out of the scope of the current odML project, but adding custom 
validators, that check whether a file is available or if it has changed (providing the 
checksum is available) should be do-able.

Freeform notes:
- Use an additional layer on top of odML core
- basically use odML as build tool
- if a file path is provided in an odML file, add a checksum and validate this checksum 
  every time the odML file is opened and the filepath is available. If not available 
  provide message to the user; if checksum does not match, do the same and ask user for 
  feedback.
- basically odML as container which files belong to an experiment and odML file checks 
  which of the linked files are available
- what we can do for sure: add a validator to odML that checks if provided files paths 
  in an odML file are available on the current system and also checks whether 
  a checksum matches.


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
   -- [N] T_suspension = 35dC
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

IF current - I_steps that are increasing until the cell spikes
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
  - which electrodes: microchannel systems
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

- next experiment ... triple Paired pulses over time
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


NOTE: it would probably have been better, if we had focused on one particular experiment 
and thoroughly documented that one.


http://www.bcf.uni-freiburg.de/people
Heining, Katharina
Diego M Vieira
Rodríguez Flores, Esther
Okujeni, Samora, Dr.
works on development of in vitro neuronal cell networks, how they change over time and 
which factors are important for survival from a cell activity point of view

- already set up a good pipeline from raw data to analysis and has a lot of metadata 
  automatically documented
- should add morphology data documented in odml and might have to move his ephys 
  documentation to odml as well
  - advised to first come up with a feasible scheme for morphology and then write an 
    extractor from matlab to odml to merge these two datasets. should not mess around 
    with a pipeline that has been developed over years until a parallel pipeline works 
    as good as this.
- File structure: PIDXXX_CISXXX_MEAXXX_DIVXXX_[Drugs].mcd
  ... recording data contains setup metadata, on analysis this metadata is 
      extracted and put into well defined matlab structure.
- Next to the mcd is a metadata file with the same name; on analysis, the metadata 
  from this file is added to the setup specific metadata.


### Neuro course, Data management part


#### Questions for the tutors
- are there any parameters they would like to get analysed across courses?
- is there a specific part / topic that might be helpful to students and that
  we should focus on?


#### Question for the students:

why is consistent recording, structuring of data necessary:

in your context there are a couple of cases to consider:
a) personal stake: when you write the protocol for this course not tomorrow, but in one 
   or two weeks from now
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
exp - animal - region - slice - protocol - dye-process - images
- would be nice to have the process in reverse to travel with the images w/o having 
  to keep other branches e.g. from other images
-> export a leaf to the root

region: should contain a list of available subregions that can mapped to electrode 
        positions or tissue damage
mapping electrodes with region selection and note about tissue damage

- export variant from leaf including all parent nodes until the root 
    discarding all sibling branches
- small script to pull a short description out of an odML file / template - 
    such a reporting tool would be an awesome feature to document the 
    usefullness of documenting metadata.
- with three groups, we could have three odML documents that could be diff'ed
    to display the differences in note keeping

odml: would be nice to have a file name generator from specific fields that already
      are present in an odML file - that would be use case specific, but maybe we
      could generalize the functionality.

Next steps: Contact Diego and Samora re talking about first draft of odML


## G-Node meeting notes
- UEgert was very interested in continuing the collaboration and to include a data 
management part in the course next year. Given, that we continue working on 
the templates, odML usage and the didactic part.

- too little time to come up with a thorough documentation
- would have made sense to focus on one, outmost two experiments
- was exposed to various shortcomings of odML and our own knowledge in using it
- showed how important templates are and that we also should have a good understanding
in how to create, apply and nest them if odML is supposed to be use- and helpful.
- showed how hard it is and how long it takes to identify important metadata and to 
come up with a useful odML template.
- came up with a first template for one branch of experiments - needs to be overhauled
and discussed with Freiburg people

- used template as basis for discussion with UEgert:
- general structure: odML file should be deeply branched 
  experiment - animal - region - tissue - procedure A - procedure B - imaging - results
  at every node the file should branch!
- there should not be references to sub files or templates to reduce redundancy. every
  file should always contain all data to reduce chance of a template being changed after
  it has been referenced in a "root" odML file that would include sub odML files.
- using the yaml format would be the most desireable for data collection
  ideally via a GUI, but text subtemplates that are copy pasted can be used as a crutch
  until a usable GUI is available.
- there should be easily plugin-able templates for setup, AB, protocols
- ideally these templates should be easily plugged into each other on a graphical
  user interface 
- the protocols should be documented and contained in odML IN DETAIL
- ideally at the end of a course there will be a script, that generates a short
  report from the collected metadata to show the students the benefit of 
  thoroughly documenting metadata
- at the end do a diff on the metadata the student groups collected to show
  which data is missing

- roadmap would be:
- would require dedication on our end of one day per week
- finalize and fine tune first experiment odML (immunohistochemistry)
- add second experiment odML (MEA ephys)
- be done in ~3 weeks and check back and discuss with Diego, Samora
- finetune again and discuss with Ulrich
- discuss which further templates (setup, lab protocols) are required and need to
  be added.
- once the templates are defined, add a list of ranked usability features
  and successively work through the list until the course.

- ideas for odML usage, further development and general statements:
- UEgert stressed, that all tools have to be available for Windows and should
ideally provide easy to use GUIs as well. Otherwise adoption in experimental labs
is highly unlikely from his experience - and he would probably have a hard time
adopting it in his lab as well.
- Ulrich would like to use odML as a projects metadata management tool
required features for this:
- filechecks of files listed in an odML file: via filename and checksum, if a file is present 
                                                            and has changed when an odML file is opened.
- A general idea is to use the metadata of a project as the project management tool to  
  keep control of the actual data and scripts.
  odML used as a 'make' tool e.g.: when opening an odML file, creating analysis files and
  extracting metadata, adding and linking sub odML files via scripts and raw files that 
  are mentioned in an odML file.
- due to deeply nested odML files it would be necessary to 
  - have a visual representation of nodes in an odML file analogous 
    to the DAG in snakemake
  - it would be required to have a 'Leaf-export' feature to create an odML file from a leaf
    to its root without any of its siblings e.g. an image that is based on a specific 
    electrode in a MEA should be exportable without any of the other electrodes or
    information about other animals or tissues in the same experiment.
- it would be nice to have additional tools e.g. like ouput file name generators that
  create structured filenames dependent on previous documented data in odML and
  automatically add that to odML analogous to mp3 filename creators 
  e.g. %date%_%Tissue%_%AntiBody1%_%AntiBody2%

- during the course I stumbled across a couple of bugs and shortcomings:
- matlab/java implementation of odML is severely out of date but would
be required for windows users; also does not support json or yaml
- yaml and json are not supported when using sub-odml files


## JGrewe meeting notes

UEgert hat einige interessante Ideen bezüglich odML.

- alle Tools müssen auf Windows verfügbar und einfach installier und benutzbar sein.

- odML als Quality magangement / build tool
  Ulrich würde odML am liebsten aus einer PI/Quality management verwenden. Metadaten
  sollten via odML dazu benutzt werden die Daten eines Projektes zu kontrollieren.
  d.h. wenn eine odML Datei geöffnet wird, sollte die Library selbständig alle
  in  der Datei gelisteten verlinkten Dateien prüfen, ob sie
  a) vorhanden sind
  b) über eine Checksum prüfen, ob sie sich verändert haben
  c) verlinkte Scripts ausführen, um z.b. Endresultate aus den verlinkten
     Dateien erzeugen -> das wäre quasi odML als 'make' tool für ein Projekt.
  d) einen 'Filebrowser' der eine odML Datei graphisch betrachtbar macht und
     über das verlinkte Dateien mit dem korrekten Program geöffnet werden können.

- eine Projekt bezogene odML Struktur. Aus Ulrichs Sicht müssten alle odML
  odML files sollten immer komplett sein und nicht auf Sub-dateien verweisen.
  Dokumente im wesentlichen der folgenden Struktur folgen:
  [root] - [projekt] - [subjekt] - [tissue] - [Protokoll A] - [Resultat A] - [Protokoll B] - [Resultat B] - etc.
  Jedes Protokoll enthält verwendete Setups und chemische Komponenten sowie 
  Jeder Knoten in so einem odML Tree führt zu einem Branching point.
  Idealerweise hat man für jeden Knoten templates, die man einfach einfügen 
  und mit Werten befüllen kann. Aus Ulrichs sicht gibt es hier ein paar wesentliche 
  Punkte zu beachten:
  - Protokolle d.h. Arbeitsabläufe im Labor müssten vollständig eingefügt werden können.
  - Templates müssen ohne Probleme mehrfach eingefügt werden können z.b. 
      verschiedene Subjekte, verschiedene Antikörper oder Protokolle.
  - Zum zusammenbauen so eines Baumes müsste es eine einfache zu benutzende 
      graphische Oberfläche geben.
  - Es muss unter Windows verfügbar und einfach benutzbar sein.

- Zusatzfunktionen damit odML einen Mehrwert für den Benutzer darstellt
  - Verfügbare Templates
  - Nachdem in der oben beschriebenen Struktur die odML Dateien extrem groß und 
      unübersichtlich werden (sehr tiefe Bäume) muss es eine Möglichkeit geben,
      alle Informationen zu einem speziellen Resultat zu exportieren.
      E.g. wenn das Endresultat einer Analyse 100 Imagedateien für 10 
      verschiedenen Subjekte und 2 verschiedene Tissues sind, soll es möglich sein
      ausgehend von genau einer Imagedatei alle Informationen für diese Datei
      zurück zum root des Dokuments zu verfolgen und nur diese Informationen
      zu exportieren -> 'leaf-export'
  - eine Möglichkeit, um aus einer odML Datei einen lesbaren Report zu generieren.
  - Custom Validation: zu einem Template sollte es möglich sein, selbst validationen
     zu definieren z.b. welche Werte eines Templates beim Speichern auf jeden Fall 
     vorhanden sein müssen, ob eine gewissen Anzahl an sub-templates vorhanden sein
     muss; dass gewisse Dateien physisch vorhanden sind; etc.


#### Meeting with JGrewe

discussed Freiburg ideas:
- should have an FAQ section in how to create templates, what are main concepts e.g. 
  shallow vs deep trees and which are common problems in transforming metadata to odML 
  e.g. how do I get a table properly into odML
- with respect to the point above: get in touch with Lyuba Zehl, since she probably
  encountered multiple of these problems during her odML quest. 
- shorten section and property (and other attributes) when saving to file
  e.g. <section> -> <sec> or <osec>
- how to deal with ids when a template is imported -> should probably get a new id when
  a template becomes part of a different odML file.
- revision ids on template import -> keep the id of the template root or add revision
  sections/properties to a template
- custom validations:
  odML specific syntax, part of an odML template and will be imported when
  the template is imported, but will be executed whenever an odML file is saved.

        e.g.
        [sec:validation]
          [sec:required]
               [section_type#property_name]
           [sec:range]
               [section_type#property] [min, max]
           [sec:checks]
               []
            [auto_fill]

  things to consider here are a) how do we know all the validations? b) how do we know
  where the validations should be applied to - should only be applied to "their" template.
- with respect to the point above:
  saving a filename with a checksum should probably be a section template
  with filename, checksum etc as properties and then a validation for locally available,
  whether the checksum has changed etc. 
- it would be nice to move the odml-ui from gtk to pyqt to be more windows compatible


issues and questions
- in odmltables there is a bug when trying to save a document with a document date
- did lyuba ever save tabular data, and if yes, whats the best way to do it




Hi Thomas!

Since some of our team are english speakers, my reply is in english as well, I hope you don't mind.

With respect to your first questions: you could also install the DOI server we developed,
but only organisations registered with the DOI organisation can request a DOI, so
it would not help if you installed your own instance.
We do guarantee that repositories that are uploaded to the G-Node GIN and 
that request a DOI from such a repository will be hosted for at least 20 years.

You can easily upload a repository that is hosted in your in-house GIN to the G-Node
web gin by just changing the remote server of the repository in question and simply pushing 
the content again.

With respect to your second question: we ourselves are using an apache in front of the GIN instance we are running.
If you plan to make your GIN instance accessible from outside your institute we would recommend using an apache 
up front as well.

And finally with respect to the second email: we do not have any restrictions on repository size but rather encourage a fair use policy. so in theory you can upload as much data as you want, the 2 TB you mention should be no problem at all, since the main bottleneck would be the upload rate in any case.




hallo,

noch eine kurze frage: wenn wir statt einer in-house installation ihren server nutzen würden, wie groß darf ein einzelnes repository / ein file sein? wir suchen nach einem repository für MEG rohdaten. diese können pro studie bis zu 2TB (verteilt auf mehrere files <2GB) benötigen.

viele grüße,
thomas hartmann



