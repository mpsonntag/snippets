import pandas as pd

import nixio

head_col = ['curr_frame', 'time_elapsed', 'obj_substracted', 'substracted_value',
            'obj_value', 'obj_size', 'background_value', 'xold', 'yold']

ca_data = pd.read_csv('20120705Pflp178GCaMP5kshift210421W8BAG.log',
                   header=None, names=head_col)

filename = "/home/msonntag/Chaos/DL/ca_imaging.nix"
nf = nixio.File.open(filename, nixio.FileMode.Overwrite)

b = nf.create_block(name="ca_imaging_data")
da = b.create_data_array(name="ca_data_20120705", array_type="time_elapsed",
                         data=ca_data["time_elapsed"])
da.label = "time elapsed"
da.unit = "ms"
da.append_sampled_dimension(1, label="frame", offset=1)

# Group experiment data
g = b.create_group(name="ca_data_20120705", type_="CA-primary-data")
g.data_arrays.append(da)

nf.close()
