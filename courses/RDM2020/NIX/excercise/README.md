# Recording description

InVivo single cell recording in strain N2 Caenorhabditis elegans.
Activity shown in oxygen sensitive neuron(s) using Calcium Indicator GCaMP5k.

## Oxygen shift paradigm

Experiments used an oxygen concentration shift paradigm:
- 110 seconds 21% O2 concentration; hard oxygen switch
- 360 seconds 04% O2 concentration; hard oxygen switch
- 140 seconds 21% O2 concentration

## Recording files

Calcium imaging traces can be found in files with the extension "*.log".

The nine columns contained in these log files are to be interpreted in this order:
"current_frame", "time_elapsed", "obj_substracted", "substracted_value", "obj_value", "obj_size", "background_value", "x_old", "y_old"

e.g.
[1],  [2],    [3],     [4],     [5],  [6], [7],     [8], [9] 
6046, 605491, 10768.6, 12809.4, 23578, 80, 160.118, 264, 65

The columns are interpreted as:

[1] current_frame       ... recorded frame
[2] time_elapsed        ... time in milliseconds [ms]
[3] obj_substracted     ... object_value - background_value; Fluorescence [AU]
[4] substracted_value   ... background_value; Fluorescence [AU]
[5] obj_value           ... average value of region of interest; Fluorescence [AU]
[6] obj_size            ... whole area of region of interest in pixel [px]
[7] background_value    ... average of designated background region; Fluorescence [AU]
[8] x_old               ... previous x position of region of interest [px]
[9] y_old               ... previous y position of region of interest [px]

## Recording files metadata
file name, strain, protocol [%], feeding condition [hour], worm resting time [min], tracked neuron, intensity, Comments, tracking comment, frames, genetic modification, shifting times [s], worm, paralytic agent, EM gain settig, LED I, Gray Filter, exposure

20121202Pflp178GCaMP5kN2shift_210421W1, N2, cs01_shift 21-04-21, 1h50, 7', BAG,	4000/400,'' ,'' 6100, Pflp-8; Pflp-17::GCaMP5.k, 110-360-150, 1, Tetramisol 5mM, 1500, 20, 0.2, 100 ms

20121202Pflp178GCaMP5kN2shift_210421W2, N2, cs01_shift 21-04-21, 2h17, 5'30'', BAG (+URX), 4400/500, process visible, '', 6100, Pflp-8; Pflp-17::GCaMP5.k, 110-360-150, 1, Tetramisol 5mM, 1500, 20, 0.2, 100 ms

20121205Pflp178GCaMP5kN2shift_210421W4, N2, cs01_shift, 21-04-21, 2h20, 5', BAG, 6200/500, process visible, '', 6100, Pflp-8; Pflp-17::GCaMP5.k, 110-360-150, 1, Tetramisol 5mM, 1500, 20, 0.2, 100 ms

## Recording equipment and settings

Zeiss epifluorescence microscope equipped with a CoolLED pE-100 excitation system.
Images were acquired with an Andor iXon 397 EMCCD camera and MetaMorph software (Universal Imaging)
Objective: Pln Apo 40x/1.3 oil DIC II

Zeiss recording settings:
pE LED intensity 2                      ... 20
Zeiss 6x reflector changer              ... none
Zeiss 3x Optovar turret                 ... 1x Tubelens
Zeiss 3x Beam Path Switching Baseport   ... 100% Baseport
Zeiss 3x Sideport Baseport              ... 100% L
Zeiss RL 6x FL Attenuator               ... 20%

Digitizer                               ... 14 bit (10MHz)
Exposure Time                           ... 100ms
EM Gain                                 ... 1500

# Background
The Caenorabdhitis elegans neurons labeled BAG and URX have been reported to be tonic signaling neurons. The constant high concentration of increased intracellular Ca 2+ is thought to be mediated by L-type voltage gated Ca 2+ channels (L-VGCC), IP3 and ryanodine receptor Ca 2+ channels. (Busch et al, 2011)
The activity of the oxygen de- and increase sensory neurons BAG and URX is tested in
an N2 strain (ZIM226) background. The strain contains an extra-chromosomal array expressing GCaMP5k under the flp-8 and the flp-17 promoter. Flp-8 is expressed in URX, flp-17 in BAG. GCaMP5k is a genetically encoded calcium indicator (Akerboom et al, 2012) which links calmodulin to an inactive form of GFP. Upon binding of Ca 2+ to calmodulin the conformation of GFP changes and becomes fluorescent. Depolarization of a neuron leads to an intracellular release of Ca 2+. GCaMP therefore is a useful second messenger in visualizing neuronal activity.

## Neuronal activity in an oxygen shift paradigm
To study the response of the sensory neurons to a harsh stimulus, animals were exposed to subsequent oxygen shifts from 21-4% and back to 21%, oxygen concentrations are always balanced with nitrogen. The oxygen "down shift" (DS) took place 110 seconds, the "up shift" (US) 470 seconds after the start of the experiment.

# Data provenance
All recordings were done at and by:
The Research Institute of Molecular Pathology (IMP), Vienna, Austria
Research Group Manuel Zimmer
