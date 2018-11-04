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
col = tdata.values[5]

# load data into nix
nixfile = nix.File.open(nixfn, nix.FileMode.Overwrite)
b = nixfile.create_block(name="oxygen_shift_trials", type_="calcium_imaging")
da = b.create_data_array(name="N2_URX_shift_210421_20120705",
                         array_type="df_over_f", data=col)
da.label = "dF/F"

# Add the second dimension to the data array
dim = da.append_sampled_dimension(steps[1] - steps[0])
dim.label = "frames"

