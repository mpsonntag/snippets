import matplotlib.pyplot as plot
import numpy as np

import nixio as nix

# read data from file
nixf = nix.File.open("module2.h5", nix.FileMode.ReadOnly)

# inspect contents
nixf.blocks


# get overview of block contents
for b in nixf.blocks:
    tlst = list(filter(lambda x: x.type == "nix.trial", b.tags))
    print('session %s: %d trials' % (b.name, len(tlst)))
    for s in b.sources:
        print('\t'+s.name)


# select data from one session
b108 = nixf.blocks["joe108"]


# select data arrays
dalst = filter(lambda x:
               ("SpikeActivity" in x.name) &
               (filter(lambda s: s.name == "Unit 7", x.sources) != []) &
               (x.metadata['Target'] == 2) & 
               (x.metadata['BehavioralCondition'] == 3),
               b108.data_arrays)

# plot spiketrains
[tind, jind] = np.nonzero(list(dalst))
plot.scatter(tind, jind)
