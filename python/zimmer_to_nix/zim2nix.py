import matplotlib.pyplot as plt
import pandas as pd

import nixio

head_col = ['curr_frame', 'time_elapsed', 'obj_subtracted', 'subtracted_value',
            'obj_value', 'obj_size', 'background_value', 'xold', 'yold']

ca_data = pd.read_csv('20120705Pflp178GCaMP5kshift210421W8BAG.log',
                      header=None, names=head_col)

# ToDo
# - walk across multiple files and different protocols
# - second version with only one DataArray but 3 dims -> time as sampled, data as second and set with labels as third
# - add data arrays for stimulus protocols and use them as tags / multitags on all matching data for later filtering
# - add metadata for each worm -> think about how this can be structured

filename = "/home/msonntag/Chaos/DL/ca_imaging.nix"

nf = nixio.File.open(filename, nixio.FileMode.Overwrite)

# Main block holding CA experiment data

b = nf.create_block(name="ca_imaging_data", type_="CA-primary-data")

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

# object subtracted value data
da = b.create_data_array(name=f"{basic_name}-obj-sub", array_type="CA.object_subtracted",
                         data=ca_data["obj_subtracted"])
da.label = " F object value minus background value"
da.append_sampled_dimension(1, label="frame", offset=1)

g.data_arrays.append(da)

# subtracted value
da = b.create_data_array(name=f"{basic_name}-sub-val", array_type="CA.subtracted_value",
                         data=ca_data["subtracted_value"])
da.label = "F value subtracted"
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


# dict reference: date, strain, genetic modification, stimulus protocol,
file_dict = {
"/home/msonntag/Chaos/DL/calcium_imaging/results/N2/urx/shift210421/20120705Pflp178GCaMP5kshift210421W7URXx2.log": ["20120705", "N2", "Pflp178GCaMP5k", "O2-shift-210421", "URX", "W7"]
,"/home/msonntag/Chaos/DL/calcium_imaging/results/N2/urx/shift210421/20120705Pflp178GCaMP5kshift210421W8URX.log": ["20120705", "N2", "Pflp178GCaMP5k", "O2-shift-210421", "URX", "W8"]
,"/home/msonntag/Chaos/DL/calcium_imaging/results/N2/urx/shift210421/20120807Pflp178GCaMP5kShift210421W14URX.log": ["20120807", "N2", "Pflp178GCaMP5k", "O2-shift-210421", "URX", "W14"]
,"/home/msonntag/Chaos/DL/calcium_imaging/results/N2/urx/shift210421/20120807Pflp178GCaMP5kShift210421W15URX.log": ["20120807", "N2", "Pflp178GCaMP5k", "O2-shift-210421", "URX", "W15"]
,"/home/msonntag/Chaos/DL/calcium_imaging/results/N2/urx/shift210421/20120807Pflp178GCaMP5kShift210421W17URX.log": ["20120807", "N2", "Pflp178GCaMP5k", "O2-shift-210421", "URX", "W17"]
,"/home/msonntag/Chaos/DL/calcium_imaging/results/N2/urx/shift210421/20120807Pflp178GCaMP5kShift210421W18URX.log": ["20120807", "N2", "Pflp178GCaMP5k", "O2-shift-210421", "URX", "W18"]
,"/home/msonntag/Chaos/DL/calcium_imaging/results/N2/urx/shift210421/20120807Pflp178GCaMP5kShift210421W21URX.log": ["20120807", "N2", "Pflp178GCaMP5k", "O2-shift-210421", "URX", "W21"]
,"/home/msonntag/Chaos/DL/calcium_imaging/results/N2/urx/shift210421/20120823Pflp178GCaMP5kShift210421W4URX.log": ["20120823", "N2", "Pflp178GCaMP5k", "O2-shift-210421", "URX", "W4"]
,"/home/msonntag/Chaos/DL/calcium_imaging/results/N2/urx/shift210421/20120823Pflp178GCaMP5kShift210421W5URX.log": ["20120823", "N2", "Pflp178GCaMP5k", "O2-shift-210421", "URX", "W5"]
,"/home/msonntag/Chaos/DL/calcium_imaging/results/N2/urx/shift210421/20121123Pflp178GCaMP5kN2shift210421W1_2ndurx.log": ["20121123", "N2", "Pflp178GCaMP5k", "O2-shift-210421", "URX", "W1"]
,"/home/msonntag/Chaos/DL/calcium_imaging/results/N2/urx/shift210421/20121202Pflp178GCaMP5kN2shift_210421W3urx.log": ["20120802", "N2", "Pflp178GCaMP5k", "O2-shift-210421", "URX", "W3"]
,"/home/msonntag/Chaos/DL/calcium_imaging/results/N2/urx/shift210421/20121202Pflp178GCaMP5kN2shift_210421W4urx.log": ["20120802", "N2", "Pflp178GCaMP5k", "O2-shift-210421", "URX", "W4"]
,"/home/msonntag/Chaos/DL/calcium_imaging/results/N2/urx/shift210421/20121202Pflp178GCaMP5kN2shift_210421W5urx.log": ["20120802", "N2", "Pflp178GCaMP5k", "O2-shift-210421", "URX", "W5"]
,"/home/msonntag/Chaos/DL/calcium_imaging/results/N2/urx/shift210421/20121202Pflp178GCaMP5kN2shift_210421W8urx.log": ["20120802", "N2", "Pflp178GCaMP5k", "O2-shift-210421", "URX", "W8"]
,"/home/msonntag/Chaos/DL/calcium_imaging/results/N2/urx/shift210421/20121205Pflp178GCaMP5kN2shift_210421W2urx.log": ["20120805", "N2", "Pflp178GCaMP5k", "O2-shift-210421", "URX", "W2"]
,"/home/msonntag/Chaos/DL/calcium_imaging/results/N2/urx/shift210421/20121205Pflp178GCaMP5kN2shift_210421W3urx_probably_saturated.log": ["20120805", "N2", "Pflp178GCaMP5k", "O2-shift-210421", "URX", "W3"]
}

nf.close()
