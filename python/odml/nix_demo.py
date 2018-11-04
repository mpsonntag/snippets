import matplotlib.pyplot as plt
import pandas as pd

from pathlib import Path

import nixio as nix

fnbase = Path.joinpath(Path.home(), 'Chaos', 'work')


fnraw = str(Path.joinpath(fnbase,
                          '_Lab_Zimmer/calcium_imaging/results/N2/urx/shift210421/20120705Pflp178GCaMP5kshift210421W7URXx2.log'))

nixfn = str(Path.joinpath(fnbase, 'ginrepos', 'demo', 'elegans_oxygen.nix'))


# row_wise read in of csv file
data = pd.read_csv(fnraw)

# transpose to get columns
tdata = data.transpose()

# get df/f column as array
steps = tdata.values[0]
dff = tdata.values[5]

# load data into nix
nixfile = nix.File.open(nixfn, nix.FileMode.Overwrite)
b = nixfile.create_block(name="oxygen_shift_trials", type_="calcium_imaging")

# use a group to structure the individual trials within a block
g = b.create_group(name="N2_URX_shift_210421_20120705", type_="trial.datacollection")

# add steps column
da = b.create_data_array(name="20120705_frames", array_type="trial.column", data=steps)
da.label = "frames"

# add dF/F column
da = b.create_data_array(name="20120705_df_over_f", array_type="trial.column", data=dff)
da.label = "dF/F"

# Add the second dimension to the data array
dim = da.append_sampled_dimension(steps[1] - steps[0])
dim.label = "frames"

# Structuring our data
g.data_arrays.append(b.data_arrays["20120705_frames"])
g.data_arrays.append(b.data_arrays["20120705_df_over_f"])

# plot figure from file
fig, ax = plt.subplots()
ax.plot(b.data_arrays["20120705_df_over_f"][:])
ax.set(xlabel=b.data_arrays["20120705_df_over_f"].dimensions[0].label,
       ylabel=b.data_arrays["20120705_df_over_f"].label,
       title="URX oxygen shift trial (21-04-21)")
plt.show()

nixfile.close()
