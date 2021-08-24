import matplotlib.pyplot as plt
import pandas as pd

import nixio

head_col = ['curr_frame', 'time_elapsed', 'obj_subtracted', 'subtracted_value',
            'obj_value', 'obj_size', 'background_value', 'xold', 'yold']

# ToDo
# - walk across multiple files and different protocols
# - second version with only one DataArray but 3 dims -> time as sampled, data as second and set with labels as third
# - add data arrays for stimulus protocols and use them as tags / multitags on all matching data for later filtering
# - add metadata for each worm -> think about how this can be structured


def add_data(b, g, basic_name, basic_type, ca_data):
    # time elapsed data
    da = b.create_data_array(name=f"{basic_name}-time", array_type=f"{basic_type}.time_elapsed",
                             data=ca_data["time_elapsed"])
    da.label = "time elapsed"
    da.unit = "ms"
    da.append_sampled_dimension(1, label="frame", offset=1)

    g.data_arrays.append(da)

    # object subtracted value data
    da = b.create_data_array(name=f"{basic_name}-obj-sub",
                             array_type=f"{basic_type}.object_subtracted",
                             data=ca_data["obj_subtracted"])
    da.label = " F object value minus background value"
    da.append_sampled_dimension(1, label="frame", offset=1)

    g.data_arrays.append(da)

    # subtracted value
    da = b.create_data_array(name=f"{basic_name}-sub-val",
                             array_type=f"{basic_type}.subtracted_value",
                             data=ca_data["subtracted_value"])
    da.label = "F value subtracted"
    da.append_sampled_dimension(1, label="frame", offset=1)

    g.data_arrays.append(da)

    # object value
    da = b.create_data_array(name=f"{basic_name}-obj-val", array_type=f"{basic_type}.object_value",
                             data=ca_data["obj_value"])
    da.label = "F object value absolute"
    da.append_sampled_dimension(1, label="frame", offset=1)

    g.data_arrays.append(da)

    # object size
    da = b.create_data_array(name=f"{basic_name}-obj-size", array_type=f"{basic_type}.object_size",
                             data=ca_data["obj_size"])
    da.label = "object size"
    da.unit = "pixel"
    da.append_sampled_dimension(1, label="frame", offset=1)

    g.data_arrays.append(da)

    # background value
    da = b.create_data_array(name=f"{basic_name}-bgd-val",
                             array_type=f"{basic_type}.background_value",
                             data=ca_data["background_value"])
    da.label = "F background value average"
    da.append_sampled_dimension(1, label="frame", offset=1)

    g.data_arrays.append(da)

    # previous ROI x position
    da = b.create_data_array(name=f"{basic_name}-roi-old-x", array_type=f"{basic_type}.ROI_old_x",
                             data=ca_data["xold"])
    da.label = "previous ROI x position"
    da.append_sampled_dimension(1, label="frame", offset=1)

    g.data_arrays.append(da)

    # previous ROI y position
    da = b.create_data_array(name=f"{basic_name}-roi-old-y", array_type=f"{basic_type}.ROI_old_y",
                             data=ca_data["yold"])
    da.label = "previous ROI y position"
    da.append_sampled_dimension(1, label="frame", offset=1)

    g.data_arrays.append(da)


def run_single_raw(nf):
    ca_data = pd.read_csv('20120705Pflp178GCaMP5kshift210421W8BAG.log',
                          header=None, names=head_col)
    # Main block holding CA experiment data
    b = nf.create_block(name="ca_imaging_data", type_="CA-primary-data")
    basic_name = "CA-data.20120705.W8"
    # Group data by experiment data arrays
    g = b.create_group(name=basic_name, type_="CA-primary-data")

    add_data(b, g, basic_name, "CA", ca_data)

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


def run_multiple_raw(block, spec_path, file_dict, prot_type, prot_switch, strain, neuron, marker):
    g = block.create_group(name=f"Ca.{strain}.{neuron}", type_=f"Ca.{strain}.{neuron}")
    for fname in file_dict:
        ffname = f"{path_base_raw_files}{spec_path}{fname}"
        curr_data = pd.read_csv(ffname, header=None, names=head_col)
        print(file_dict[fname])

        # use date and worm number as name
        basic_name = f"Ca.{file_dict[fname][0]}.{file_dict[fname][1]}"
        basic_type = f"Ca.{prot_type}.{prot_switch}.{strain}.{neuron}"

        # Group data by experiment data arrays
        add_data(block, g, basic_name, basic_type, curr_data)


def run_shift_n2_urx(block):
    spec_path = "/N2/urx/shift210421/"
    # dict reference: date, strain, genetic modification, stimulus protocol,
    file_dict = {
        "20120705Pflp178GCaMP5kshift210421W7URXx2.log": ["20120705", "W7"],
        "20120705Pflp178GCaMP5kshift210421W8URX.log": ["20120705", "W8"],
        "20120807Pflp178GCaMP5kShift210421W14URX.log": ["20120807", "W14"],
        "20120807Pflp178GCaMP5kShift210421W15URX.log": ["20120807", "W15"],
        "20120807Pflp178GCaMP5kShift210421W17URX.log": ["20120807", "W17"],
        "20120807Pflp178GCaMP5kShift210421W18URX.log": ["20120807", "W18"],
        "20120807Pflp178GCaMP5kShift210421W21URX.log": ["20120807", "W21"],
        "20120823Pflp178GCaMP5kShift210421W4URX.log": ["20120823", "W4"],
        "20120823Pflp178GCaMP5kShift210421W5URX.log": ["20120823", "W5"],
        "20121123Pflp178GCaMP5kN2shift210421W1_2ndurx.log": ["20121123", "W1"],
        "20121202Pflp178GCaMP5kN2shift_210421W3urx.log": ["20120802", "W3"],
        "20121202Pflp178GCaMP5kN2shift_210421W4urx.log": ["20120802", "W4"],
        "20121202Pflp178GCaMP5kN2shift_210421W5urx.log": ["20120802", "W5"],
        "20121202Pflp178GCaMP5kN2shift_210421W8urx.log": ["20120802", "W8"],
        "20121205Pflp178GCaMP5kN2shift_210421W2urx.log": ["20120805", "W2"],
        "20121205Pflp178GCaMP5kN2shift_210421W3urx_probably_saturated.log": ["20120805", "W3"]
    }

    prot_type = "shift"
    prot_switch = "210421"
    strain = "N2"
    neuron = "URX"
    marker = "Pflp178GCaMP5k"

    run_multiple_raw(block, spec_path, file_dict, 
                     prot_type, prot_switch, strain, neuron, marker)


def run_shift_egl3_urx(block):
    spec_path = "/egl3/urx/shift210421/"
    # dict reference: date, strain, genetic modification, stimulus protocol,
    file_dict = {
        "20120906Pflp178GCaMP5kegl3Shift210421W2URX.log": ["20120906", "W2"],
        "20121017Pflp178GCaMP5kegl3Shift210421W1URX.log": ["20121017", "W1"],
        "20121017Pflp178GCaMP5kegl3Shift210421W2urx.log": ["20121017", "W2"],
        "20121202Pflp178GCaMP5kegl3shift_210421W1urx.log": ["20121202", "W1"],
        "20121202Pflp178GCaMP5kegl3shift_210421W5_lowSigurx.log": ["20121202", "W5"],
        "20121202Pflp178GCaMP5kegl3shift_210421W8urx.log": ["20121202", "W8"],
        "20121205Pflp178GCaMP5kegl3shift_210421W1urx.log": ["20121205", "W1"],
        "20121205Pflp178GCaMP5kegl3shift_210421W4urx.log": ["20121205", "W4"],
        "20121205Pflp178GCaMP5kegl3shift_210421W6_lowSigurx.log": ["20121205", "W6"],
        "20121205Pflp178GCaMP5kegl3shift_210421W11urx.log": ["20121205", "W11"]
    }

    prot_type = "shift"
    prot_switch = "210421"
    strain = "egl3"
    neuron = "URX"
    marker = "Pflp178GCaMP5k"

    run_multiple_raw(block, spec_path, file_dict, 
                     prot_type, prot_switch, strain, neuron, marker)


def run_shift_n2_bag(block):
    spec_path = "/N2/bag/shift210421/"
    # dict reference: date, strain, genetic modification, stimulus protocol,
    file_dict = {
        "20120705Pflp178GCaMP5kshift210421W8BAG.log": ["20120705", "W8"],
        "20120705Pflp178GCaMP5kshift210421W9BAG.log": ["20120705", "W9"],
        "20120807Pflp178GCaMP5kShift210421W16BAG.log": ["20120807", "W16"],
        "20120807Pflp178GCaMP5kShift210421W18BAG.log": ["20120807", "W18"],
        "20120807Pflp178GCaMP5kShift210421W20BAG.log": ["20120807", "W20"],
        "20120823Pflp178GCaMP5kShift210421W1BAG.log": ["20120823", "W1"],
        "20120823Pflp178GCaMP5kShift210421W2BAG.log": ["20120823", "W2"],
        "20121202Pflp178GCaMP5kN2shift_210421W1bag.log": ["20121202", "W1"],
        "20121202Pflp178GCaMP5kN2shift_210421W2bag.log": ["20121202", "W2"],
        "20121202Pflp178GCaMP5kN2shift_210421W6bag.log": ["20121202", "W6"],
        "20121202Pflp178GCaMP5kN2shift_210421W7bag.log": ["20121202", "W7"],
        "20121205Pflp178GCaMP5kN2shift_210421W1bag.log": ["20121205", "W1"],
        "20121205Pflp178GCaMP5kN2shift_210421W4bag.log": ["20121205", "W4"],
        "20121205Pflp178GCaMP5kN2shift_210421W5bag.log": ["20121205", "W5"]
    }

    prot_type = "shift"
    prot_switch = "210421"
    strain = "N2"
    neuron = "BAG"
    marker = "Pflp178GCaMP5k"

    run_multiple_raw(block, spec_path, file_dict,
                     prot_type, prot_switch, strain, neuron, marker)


def run_shift_egl3_bag(block):
    spec_path = "/egl3/bag/shift210421/"
    # dict reference: date, strain, genetic modification, stimulus protocol,
    file_dict = {
        "20120904Pflp178GCaMP5kegl3Shift210421W11BAG.log": ["20120904", "W11"],
        "20120906Pflp178GCaMP5kegl3Shift210421W1BAG.log": ["20120906", "W1"],
        "20120906Pflp178GCaMP5kegl3Shift210421W6BAG.log": ["20120906", "W6"],
        "20121017Pflp178GCaMP5kegl3Shift210421W4bag.log": ["20121017", "W4"],
        "20121202Pflp178GCaMP5kegl3shift_210421W1bag.log": ["20121202", "W1"],
        "20121202Pflp178GCaMP5kegl3shift_210421W4_lowSigbag.log": ["20121202", "W4"],
        "20121202Pflp178GCaMP5kegl3shift_210421W7bag.log": ["20121202", "W7"],
        "20121202Pflp178GCaMP5kegl3shift_210421W8bag.log": ["20121202", "W8"],
        "20121205Pflp178GCaMP5kegl3shift_210421W2_sigLowbag.log": ["20121205", "W2"],
        "20121205Pflp178GCaMP5kegl3shift_210421W3_2SECLATEbag_add20frm_at_beg.log": ["20121205", "W3"],
        "20121205Pflp178GCaMP5kegl3shift_210421W3_2SECLATEbag.log": ["20121205", "W3"],
        "20121205Pflp178GCaMP5kegl3shift_210421W5bag.log": ["20121205", "W5"],
        "20121205Pflp178GCaMP5kegl3shift_210421W7bag.log": ["20121205", "W7"],
        "20121205Pflp178GCaMP5kegl3shift_210421W8bag.log": ["20121205", "W8"]
    }

    prot_type = "shift"
    prot_switch = "210421"
    strain = "egl3"
    neuron = "BAG"
    marker = "Pflp178GCaMP5k"

    run_multiple_raw(block, spec_path, file_dict,
                     prot_type, prot_switch, strain, neuron, marker)


def run_ramp_n2_urx(block):
    spec_path = "/N2/urx/ramp210421/"
    # dict reference: date, strain, genetic modification, stimulus protocol,
    file_dict = {
        "20120703Pflp178GCaMP5kRamp210421W2URX.log": ["20120703", "W2"],
        "20120703Pflp178GCaMP5kRamp210421W3URX.log": ["20120703", "W3"],
        "20120703Pflp178GCaMP5kRamp210421W4URX.log": ["20120703", "W4"],
        "20120703Pflp178GCaMP5kRamp210421W6URX.log": ["20120703", "W6"],
        "20120705Pflp178GCaMP5kRamp210421W3URX.log": ["20120705", "W3"],
        "20120705Pflp178GCaMP5kRamp210421W4URX.log": ["20120705", "W4"],
        "20120807Pflp178GCaMP5kRamp210421W1URX.log": ["20120807", "W1"],
        "20120807Pflp178GCaMP5kRamp210421W2URX1.log": ["20120807", "W2"],
        "20120807Pflp178GCaMP5kRamp210421W6URXl.log": ["20120807", "W6"],
        "20120807Pflp178GCaMP5kRamp210421W11URXl.log": ["20120807", "W11"],
        "20121108Pflp178GCaMP5kN2Ramp210421W2urx.log": ["20121108", "W2"],
        "20121108Pflp178GCaMP5kN2Ramp210421W3urx.log": ["20121108", "W3"],
        "20121116Pflp178GCaMP5kN2Ramp210421W3urx.log": ["20121116", "W3"],
        "20121123Pflp178GCaMP5kN2Ramp210421W1urx.log": ["20121123", "W1"],
        "20121128Pflp178GCaMP5kN2Ramp_2_210421W2urx.log": ["20121128", "W2"],
        "20121128Pflp178GCaMP5kN2Ramp_2_210421W3urx.log": ["20121128", "W3"]
    }

    prot_type = "ramp"
    prot_switch = "210421"
    strain = "N2"
    neuron = "URX"
    marker = "Pflp178GCaMP5k"

    run_multiple_raw(block, spec_path, file_dict, 
                     prot_type, prot_switch, strain, neuron, marker)


def run_ramp_egl3_urx(block):
    spec_path = "/egl3/urx/ramp210421/"
    # dict reference: date, strain, genetic modification, stimulus protocol,
    file_dict = {
        "20120906Pflp178GCaMP5kegl3Ramp210421W3URX.log": ["20120906", "W3"],
        "20120906Pflp178GCaMP5kegl3Ramp210421W4URX.log": ["20120906", "W4"],
        "20120906Pflp178GCaMP5kegl3Ramp210421W7URX.log": ["20120906", "W7"],
        "20121017Pflp178GCaMP5kegl3Ramp210421W3urx.log": ["20121017", "W3"],
        "20121023Pflp178GCaMP5kegl3Ramp210421W2urx.log": ["20121023", "W2"],
        "20121023Pflp178GCaMP5kegl3Ramp210421W4urx.log": ["20121023", "W4"],
        "20121108Pflp178GCaMP5kegl3Ramp210421W3urx.log": ["20121108", "W3"],
        "20121108Pflp178GCaMP5kegl3Ramp210421W4urx.log": ["20121108", "W4"],
        "20121116Pflp178GCaMP5kegl3Ramp210421W2urx.log": ["20121116", "W2"],
        "20121116Pflp178GCaMP5kegl3Ramp210421W3urx.log": ["20121116", "W3"],
        "20121128Pflp178GCaMP5kegl3Ramp_2_210421W1urx.log": ["20121128", "W1"],
        "20121128Pflp178GCaMP5kegl3Ramp_2_210421W6urx.log": ["20121128", "W6"]
    }

    prot_type = "ramp"
    prot_switch = "210421"
    strain = "egl3"
    neuron = "URX"
    marker = "Pflp178GCaMP5k"

    run_multiple_raw(block, spec_path, file_dict, 
                     prot_type, prot_switch, strain, neuron, marker)


path_base_raw_files = "/home/msonntag/Chaos/DL/calcium_imaging/results"
out_file = "/home/msonntag/Chaos/DL/ca_imaging.nix"
nif = nixio.File.open(out_file, nixio.FileMode.Overwrite)
#run_single_raw(nif)

b = nif.create_block(name=f"Ca_imaging_data_shift_210421",
                     type_=f"Ca.raw.shift.210421")
run_shift_n2_urx(b)
run_shift_egl3_urx(b)
run_shift_n2_bag(b)
run_shift_egl3_bag(b)

b = nif.create_block(name=f"Ca_imaging_data_ramp_210421",
                     type_=f"Ca.raw.ramp.210421")
run_ramp_n2_urx(b)
run_ramp_egl3_urx(b)

nif.close()
