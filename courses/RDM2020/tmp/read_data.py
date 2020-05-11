from matplotlib.pyplot import scatter
from numpy import nonzero

import nixio

from .lib.joe_utils import Plotter

nixf = nixio.File.open("module2x.h5", nixio.FileMode.ReadOnly)

print(nixf.blocks)

for b in nixf.blocks:
    tlst = filter( lambda x : x.type == "nix.trial", b.tags)
    print('session %s: %d trials' % (b.name,len(tlst)))
    for s in b.sources:
        print('\t'+s.name)
    tlst = filter( lambda x : x.type == "nix.trial", b.tags)

b108 = nixf.blocks["joe108"]

b108.sources

dalst = filter( lambda x :
               ("SpikeActivity" in x.name) &
               (filter( lambda s : s.name == "Unit 7", x.sources) != []) &
               (x.metadata['Target'] == 2) &
               (x.metadata['BehavioralCondition'] == 3),
               b108.data_arrays)

print   (dalst)

[tind,jind]=nonzero(dalst[0])
scatter(tind,jind)

spike_times = [da for da in b108.data_arrays if da.type == "nix.spiketimes"]
plotter = Plotter(width=800, height=300,lines=1)
plotter.add(spike_times[0], xlim=[0, 2000], color="red")
plotter.add(spike_times[1], xlim=[0, 2000], color="red")
plotter.add(spike_times[2], xlim=[0, 2000], color="red")
plotter.plot()

nixf.close()
