
from nix import *

# read data from file
nixf = File.open("module2.h5", FileMode.ReadOnly)

# inspect contents
nixf.blocks


# get overview of block contents
for b in nixf.blocks:
    tlst = filter( lambda x : x.type == "nix.trial", b.tags)
    print 'session %s: %d trials' % (b.name,len(tlst))
    for s in b.sources:
        print '\t'+s.name
    tlst = filter( lambda x : x.type == "nix.trial", b.tags)


# select data from one session
b108 = nixf.blocks["joe108"]


# select data arrays
dalst = filter( lambda x : 
               ("SpikeActivity" in x.name) &
               (filter( lambda s : s.name == "Unit 7", x.sources) != []) & 
               (x.metadata['Target'] == 2) & 
               (x.metadata['BehavioralCondition'] == 3),
               b108.data_arrays)

# plot spiketrains
[tind,jind]=nonzero(dalst)
scatter(tind,jind)
