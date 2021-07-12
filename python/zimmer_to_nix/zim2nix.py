import matplotlib.pyplot as plt
import pandas as pd

import nixio

head_col = ['curr_frame', 'time_elapsed', 'obj_substracted', 'substracted_value',
            'obj_value', 'obj_size', 'background_value', 'xold', 'yold']

ca_data = pd.read_csv('20120705Pflp178GCaMP5kshift210421W8BAG.log',
                      header=None, names=head_col)

filename = "/home/msonntag/Chaos/DL/ca_imaging.nix"
nf = nixio.File.open(filename, nixio.FileMode.Overwrite)

# Main block holding CA experiment data
b = nf.create_block(name="ca_imaging_data")

basic_name = "CA-data.20120705.W8"

# Group data by experiment data arrays
g = b.create_group(name=basic_name, type_="CA-primary-data")

# time elapsed data
da = b.create_data_array(name=f"{basic_name}-time", array_type="CA.time_elapsed",
                         data=ca_data["time_elapsed"])
da.label = "time elapsed"
da.unit = "ms"
da.append_sampled_dimension(1, label="frame", offset=1)

g.data_arrays.append(da)

# object substracted value data
da = b.create_data_array(name=f"{basic_name}-obj-sub", array_type="CA.object_substracted",
                         data=ca_data["obj_substracted"])
da.label = " F object value minus background value"
da.append_sampled_dimension(1, label="frame", offset=1)

g.data_arrays.append(da)

# substracted value
da = b.create_data_array(name=f"{basic_name}-sub-val", array_type="CA.substracted_value",
                         data=ca_data["substracted_value"])
da.label = "F value substracted"
da.append_sampled_dimension(1, label="frame", offset=1)

g.data_arrays.append(da)

# object value
da = b.create_data_array(name=f"{basic_name}-obj-val", array_type="CA.object_value",
                         data=ca_data["obj_value"])
da.label = "F object value absolute"
da.append_sampled_dimension(1, label="frame", offset=1)

g.data_arrays.append(da)

# object size
da = b.create_data_array(name=f"{basic_name}-obj-size", array_type="CA.object_size",
                         data=ca_data["obj_size"])
da.label = "object size"
da.unit = "pixel"
da.append_sampled_dimension(1, label="frame", offset=1)

g.data_arrays.append(da)

# background value
da = b.create_data_array(name=f"{basic_name}-bgd-val", array_type="CA.background_value",
                         data=ca_data["background_value"])
da.label = "F background value average"
da.append_sampled_dimension(1, label="frame", offset=1)

g.data_arrays.append(da)

# previous ROI x position
da = b.create_data_array(name=f"{basic_name}-roi-old-x", array_type="CA.ROI_old_x",
                         data=ca_data["xold"])
da.label = "previous ROI x position"
da.append_sampled_dimension(1, label="frame", offset=1)

g.data_arrays.append(da)

# previous ROI y position
da = b.create_data_array(name=f"{basic_name}-roi-old-y", array_type="CA.ROI_old_y",
                         data=ca_data["yold"])
da.label = "previous ROI y position"
da.append_sampled_dimension(1, label="frame", offset=1)

g.data_arrays.append(da)

# make an example plot
b = nf.blocks[0]
da = b.data_arrays["CA-data.20120705.W8-obj-sub"]
x_axis = da.dimensions[0]
x = x_axis.axis(da.data.shape[0])
y = da.data[:]

plt.plot(x, y, label=da.name)
plt.xlabel(x_axis.label)
plt.ylabel(da.label)
plt.legend()
plt.show()

nf.close()
