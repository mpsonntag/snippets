"""
Parse raw calcium imaging files acquired using different stimulus
protocols into a NIX file. The raw csv files require the following
columns:
'curr_frame', 'time_elapsed', 'obj_subtracted', 'subtracted_value',
'obj_value', 'obj_size', 'background_value', 'xold', 'yold'
"""
import argparse

import matplotlib.pyplot as plt
import pandas as pd

import nixio

DEFAULT_SINGLE_RAW_FILE = "20120705Pflp178GCaMP5kshift210421W8BAG.log"
DEFAULT_RAW_FILES = "/home/msonntag/Chaos/DL/calcium_imaging/results"
DEFAULT_OUT_FILE = "/home/msonntag/Chaos/DL/ca_imaging.nix"

HEAD_COL = ['curr_frame', 'time_elapsed', 'obj_subtracted', 'subtracted_value',
            'obj_value', 'obj_size', 'background_value', 'xold', 'yold']

# Open points:
# - walk across multiple files and different protocols
# - second version with only one DataArray but 3 dims -> time as sampled, data as second and
#       set with labels as third
# - add data arrays for stimulus protocols and use them as tags / multitags on all matching data
#       for later filtering
# - add metadata for each worm -> think about how this can be structured


def add_data(nib, nig, basic_name, basic_type, ca_data):
    """
    Save raw calcium imaging data in a NIX block and group them
    via NIX groups.
    :param nib: NIX block to save the data in.
    :param nig: NIX group to group the data in.
    :param basic_name: base of all created NIX data array names.
    :param basic_type: base of all created NIX data array types.
    :param ca_data: dict containing the calcium data parsed from raw imaging files.
    """
    # time elapsed data
    nida = nib.create_data_array(name=f"{basic_name}-time",
                                 array_type=f"{basic_type}.time_elapsed",
                                 data=ca_data["time_elapsed"])
    nida.label = "time elapsed"
    nida.unit = "ms"
    nida.append_sampled_dimension(1, label="frame", offset=1)

    nig.data_arrays.append(nida)

    # object subtracted value data
    nida = nib.create_data_array(name=f"{basic_name}-obj-sub",
                                 array_type=f"{basic_type}.object_subtracted",
                                 data=ca_data["obj_subtracted"])
    nida.label = " F object value minus background value"
    nida.append_sampled_dimension(1, label="frame", offset=1)

    nig.data_arrays.append(nida)

    # subtracted value
    nida = nib.create_data_array(name=f"{basic_name}-sub-val",
                                 array_type=f"{basic_type}.subtracted_value",
                                 data=ca_data["subtracted_value"])
    nida.label = "F value subtracted"
    nida.append_sampled_dimension(1, label="frame", offset=1)

    nig.data_arrays.append(nida)

    # object value
    nida = nib.create_data_array(name=f"{basic_name}-obj-val",
                                 array_type=f"{basic_type}.object_value",
                                 data=ca_data["obj_value"])
    nida.label = "F object value absolute"
    nida.append_sampled_dimension(1, label="frame", offset=1)

    nig.data_arrays.append(nida)

    # object size
    nida = nib.create_data_array(name=f"{basic_name}-obj-size",
                                 array_type=f"{basic_type}.object_size",
                                 data=ca_data["obj_size"])
    nida.label = "object size"
    nida.unit = "pixel"
    nida.append_sampled_dimension(1, label="frame", offset=1)

    nig.data_arrays.append(nida)

    # background value
    nida = nib.create_data_array(name=f"{basic_name}-bgd-val",
                                 array_type=f"{basic_type}.background_value",
                                 data=ca_data["background_value"])
    nida.label = "F background value average"
    nida.append_sampled_dimension(1, label="frame", offset=1)

    nig.data_arrays.append(nida)

    # previous ROI x position
    nida = nib.create_data_array(name=f"{basic_name}-roi-old-x",
                                 array_type=f"{basic_type}.ROI_old_x",
                                 data=ca_data["xold"])
    nida.label = "previous ROI x position"
    nida.append_sampled_dimension(1, label="frame", offset=1)

    nig.data_arrays.append(nida)

    # previous ROI y position
    nida = nib.create_data_array(name=f"{basic_name}-roi-old-y",
                                 array_type=f"{basic_type}.ROI_old_y",
                                 data=ca_data["yold"])
    nida.label = "previous ROI y position"
    nida.append_sampled_dimension(1, label="frame", offset=1)

    nig.data_arrays.append(nida)


def plot_single_raw(nif):
    """
    Parse a single calcium imaging csv file, save the details to a NIX file
    and plot the object substracted data.
    :param nif: open NIX file object
    """
    ca_data = pd.read_csv(DEFAULT_SINGLE_RAW_FILE, header=None, names=HEAD_COL)

    # Main block holding CA experiment data
    nib = nif.create_block(name="ca_imaging_data", type_="CA-primary-data")
    basic_name = "CA-data.20120705.W8"
    # Group data by experiment data arrays
    nig = nib.create_group(name=basic_name, type_="CA-primary-data")

    add_data(nib, nig, basic_name, "CA", ca_data)

    # make an example plot
    nib = nif.blocks[0]
    nida = nib.data_arrays["CA-data.20120705.W8-obj-sub"]
    x_axis = nida.dimensions[0]
    x_data = x_axis.axis(nida.data.shape[0])
    y_data = nida.data[:]

    plt.plot(x_data, y_data, label=nida.name)
    plt.xlabel(x_axis.label)
    plt.ylabel(nida.label)
    plt.legend()
    plt.show()


def parse_protocol_from_path(spec_path, protocol_info):
    """
    Parses a specific CA imaging protocol information from a given path.
    :param spec_path: path containing the protocol information. e.g. "/egl3/urx/ramp210421/"
    :param protocol_info: information to be retrieved. Valid entries are
    "strain", "neuron", "prot_type", "o2conc".
    :return: string with the requested information or an empty string if the information
    could not be parsed.
    """
    prot_items = spec_path.strip("/").split("/")
    ret_val = ""
    if protocol_info == "strain":
        ret_val = prot_items[0]
    elif protocol_info == "neuron":
        ret_val = prot_items[1].upper()
    elif protocol_info == "prot_type":
        if "ramp" in prot_items[2].lower():
            ret_val = "ramp"
        elif "shift" in prot_items[2].lower():
            ret_val = "shift"
    elif protocol_info == "o2conc":
        ret_val = prot_items[2].lower().replace("shift", "").replace("ramp", "")

    return ret_val


def run_multiple_raw(block, spec_path, file_dict):
    """
    Reads raw calcium imaging data for all files in a provided file dict,
    stores the loaded data in a provided NIX block and groups all data in
    a newly created NIX group.
    :param block: NIX block to save data in.
    :param spec_path: path containing the protocol information. e.g. "/egl3/urx/ramp210421/"
    :param file_dict: dictionary mapping raw file names to date and subjects.
    """
    prot_type = parse_protocol_from_path(spec_path, "prot_type")
    prot_switch = parse_protocol_from_path(spec_path, "o2conc")
    strain = parse_protocol_from_path(spec_path, "strain")
    neuron = parse_protocol_from_path(spec_path, "neuron")

    nig = block.create_group(name=f"Ca.{strain}.{neuron}", type_=f"Ca.{strain}.{neuron}")
    for fname in file_dict:
        ffname = f"{DEFAULT_RAW_FILES}{spec_path}{fname}"
        curr_data = pd.read_csv(ffname, header=None, names=HEAD_COL)
        print(file_dict[fname])

        # since all data arrays live on the same block, the individual names
        # have to be very distinct to avoid duplicate name issues
        basic_name = f"Ca.{prot_type}.{prot_switch}.{strain}.{neuron}.{file_dict[fname][0]}." \
                     f"{file_dict[fname][1]}"
        basic_type = f"Ca.{prot_type}.{prot_switch}.{strain}.{neuron}"

        # Group data by experiment data arrays
        add_data(block, nig, basic_name, basic_type, curr_data)


def run_shift_n2_urx(block):
    """
    Parse and save raw N2 URX shift calcium imaging data to a NIX block.
    Location and filenames of the raw files are provided by this function.
    :param block: NIX block to store the data in.
    """
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

    spec_path = "/N2/urx/shift210421/"
    run_multiple_raw(block, spec_path, file_dict)


def run_shift_egl3_urx(block):
    """
    Parse and save raw egl3 URX shift calcium imaging data to a NIX block.
    Location and filenames of the raw files are provided by this function.
    :param block: NIX block to store the data in.
    """
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

    spec_path = "/egl3/urx/shift210421/"
    run_multiple_raw(block, spec_path, file_dict)


def run_shift_n2_bag(block):
    """
    Parse and save raw N2 BAG shift calcium imaging data to a NIX block.
    Location and filenames of the raw files are provided by this function.
    :param block: NIX block to store the data in.
    """
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

    spec_path = "/N2/bag/shift210421/"
    run_multiple_raw(block, spec_path, file_dict)


def run_shift_egl3_bag(block):
    """
    Parse and save raw egl3 BAG shift calcium imaging data to a NIX block.
    Location and filenames of the raw files are provided by this function.
    :param block: NIX block to store the data in.
    """
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
        # "20121205Pflp178GCaMP5kegl3shift_210421W3_2SECLATEbag_add20frm_at_beg.log":
        # ["20121205", "W3"], # duplicate name issue with next log
        "20121205Pflp178GCaMP5kegl3shift_210421W3_2SECLATEbag.log": ["20121205", "W3"],
        "20121205Pflp178GCaMP5kegl3shift_210421W5bag.log": ["20121205", "W5"],
        "20121205Pflp178GCaMP5kegl3shift_210421W7bag.log": ["20121205", "W7"],
        "20121205Pflp178GCaMP5kegl3shift_210421W8bag.log": ["20121205", "W8"]
    }

    spec_path = "/egl3/bag/shift210421/"
    run_multiple_raw(block, spec_path, file_dict)


def run_ramp_n2_urx(block):
    """
    Parse and save raw N2 URX ramp calcium imaging data to a NIX block.
    Location and filenames of the raw files are provided by this function.
    :param block: NIX block to store the data in.
    """
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

    spec_path = "/N2/urx/ramp210421/"
    run_multiple_raw(block, spec_path, file_dict)


def run_ramp_egl3_urx(block):
    """
    Parse and save raw egl3 URX ramp calcium imaging data to a NIX block.
    Location and filenames of the raw files are provided by this function.
    :param block: NIX block to store the data in.
    """
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

    spec_path = "/egl3/urx/ramp210421/"
    run_multiple_raw(block, spec_path, file_dict)


def run_ramp_n2_bag(block):
    """
    Parse and save raw N2 BAG ramp calcium imaging data to a NIX block.
    Location and filenames of the raw files are provided by this function.
    :param block: NIX block to store the data in.
    """
    # dict reference: date, strain, genetic modification, stimulus protocol,
    file_dict = {
        "20120703Pflp178GCaMP5kRamp210421W2BAG.log": ["20120703", "W2"],
        "20120703Pflp178GCaMP5kRamp210421W5BAG.log": ["20120703", "W5"],
        "20120703Pflp178GCaMP5kRamp210421W6BAG.log": ["20120703", "W6"],
        "20120705Pflp178GCaMP5kRamp210421W1BAG.log": ["20120705", "W1"],
        "20120705Pflp178GCaMP5kRamp210421W2upperBAG.log": ["20120705", "W2"],
        "20120705Pflp178GCaMP5kRamp210421W3BAG.log": ["20120705", "W3"],
        "20120705Pflp178GCaMP5kRamp210421W5BAGu.log": ["20120705", "W5"],
        "20120726Pflp178GCaMP5kRamp210421W2BAG.log": ["20120726", "W2"],
        "20120807Pflp178GCaMP5kRamp210421W10BAG.log": ["20120807", "W10"],
        "20120807Pflp178GCaMP5kRamp210421W12BAG.log": ["20120807", "W12"],
        "20120807Pflp178GCaMP5kRamp210421W5BAGu.log": ["20120807", "W5"],
        "20120807Pflp178GCaMP5kRamp210421W8BAG.log": ["20120807", "W8"],
        "20120823Pflp178GCaMP5kRamp210421W6BAG.log": ["20120823", "W6"],
        "20121116Pflp178GCaMP5kN2Ramp210421W1bag.log": ["20121116", "W1"],
        "20121116Pflp178GCaMP5kN2Ramp210421W2bag.log": ["20121116", "W2"],
        "20121116Pflp178GCaMP5kN2Ramp210421W3bag.log": ["20121116", "W3"],
        "20121128Pflp178GCaMP5kN2Ramp_2_210421W1bag.log": ["20121128", "W1"]
    }

    spec_path = "/N2/bag/ramp210421/"
    run_multiple_raw(block, spec_path, file_dict)


def run_ramp_egl3_bag(block):
    """
    Parse and save raw egl3 BAG ramp calcium imaging data to a NIX block.
    Location and filenames of the raw files are provided by this function.
    :param block: NIX block to store the data in.
    """
    # dict reference: date, strain, genetic modification, stimulus protocol,
    file_dict = {
        "20120904Pflp178GCaMP5kegl3Ramp210421W12BAG.log": ["20120904", "W12"],
        "20120906Pflp178GCaMP5kegl3Ramp210421W3BAG.log": ["20120906", "W3"],
        "20120906Pflp178GCaMP5kegl3Ramp210421W4BAG.log": ["20120906", "W4"],
        "20120906Pflp178GCaMP5kegl3Ramp210421W5BAG.log": ["20120906", "W5"],
        "20121023Pflp178GCaMP5kegl3Ramp210421W1bag.log": ["20121023", "W1"],
        "20121023Pflp178GCaMP5kegl3Ramp210421W3bag.log": ["20121023", "W3"],
        "20121023Pflp178GCaMP5kegl3Ramp210421W5bag.log": ["20121023", "W5"],
        "20121108Pflp178GCaMP5kegl3Ramp210421W1bag.log": ["20121108", "W1"],
        "20121108Pflp178GCaMP5kegl3Ramp210421W4bag.log": ["20121108", "W4"],
        "20121116Pflp178GCaMP5kegl3Ramp210421W1bag.log": ["20121116", "W1"],
        "20121116Pflp178GCaMP5kegl3Ramp210421W3bag.log": ["20121116", "W3"],
        "20121116Pflp178GCaMP5kegl3Ramp210421W4bag.log": ["20121116", "W4"],
        "20121123Pflp178GCaMP5kegl3Ramp210421W2bag.log": ["20121123", "W2"],
        "20121128Pflp178GCaMP5kegl3Ramp_2_210421W1bag.log": ["20121128", "W1"],
        "20121128Pflp178GCaMP5kegl3Ramp_2_210421W2bag.log": ["20121128", "W2"],
        "20121128Pflp178GCaMP5kegl3Ramp_2_210421W4bag.log": ["20121128", "W4"],
        "20121128Pflp178GCaMP5kegl3Ramp_2_210421W5bag.log": ["20121128", "W5"]
    }

    spec_path = "/egl3/bag/ramp210421/"
    run_multiple_raw(block, spec_path, file_dict)


def handle_raw_directory(nif):
    """
    Parses CA imaging data from a directory structure to a provided nix file.
    :param nif: nix file
    """
    block_shift = nif.create_block(name="Ca_imaging_data_shift_210421",
                                   type_="Ca.raw.shift.210421")
    run_shift_n2_urx(block_shift)
    run_shift_egl3_urx(block_shift)
    run_shift_n2_bag(block_shift)
    run_shift_egl3_bag(block_shift)

    block_ramp = nif.create_block(name="Ca_imaging_data_ramp_210421",
                                  type_="Ca.raw.ramp.210421")
    run_ramp_n2_urx(block_ramp)
    run_ramp_egl3_urx(block_ramp)
    run_ramp_n2_bag(block_ramp)
    run_ramp_egl3_bag(block_ramp)


def handle_file(plot_single_file):
    """
    Creates a NIX file and adds calcium imaging data from raw csv files to it.
    """
    with nixio.File.open(DEFAULT_OUT_FILE, nixio.FileMode.Overwrite) as nix_file:
        if plot_single_file:
            plot_single_raw(nix_file)
        else:
            handle_raw_directory(nix_file)


def run():
    """
    Script entry point
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot-file", dest="single", action="store_true",
                        help="Parse single file only")
    args = parser.parse_args()

    plot_raw = args.single
    handle_file(plot_raw)


if __name__ == "__main__":
    run()
