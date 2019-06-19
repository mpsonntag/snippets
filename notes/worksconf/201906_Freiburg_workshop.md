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

