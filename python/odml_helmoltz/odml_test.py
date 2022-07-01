import odml

from IPython import embed


def store_geo_param(name):
    # providing a section type enables filtering large odml file
    # with multiple similar occurrences.
    section_type = "Crown-length-parameters"
    section = odml.Section(name, section_type)
    section.create_property("data_range", [0, 999999])
    section.create_property("data_type", "float")
    section.create_property("data_dimension", [3, 3])
    _ = section.create_property("data", ["(0.4; 0.4; 0.4)",
                                         "(0.4; 0.4; 0.4)",
                                         "(0.4; 0.4; 0.4)"], dtype="3-tuple")

    return section


def validate(section):
    embed()
    must = {"data_dimension": [3, 3]}
    exists = ["data_range"]
    for mke, mkv in must.items():
        if not section.properties[mke].values == mkv:
            raise ValueError(f"Property {mke} does not match requirement {mkv}")
    for eel in exists:
        if eel not in section.properties:
            raise ValueError(f"Required property {eel} does not exist!")

    return True


if __name__ == "__main__":
    # section names have to be unique on their section level
    sec = store_geo_param(name="NPar.geo.clfh")
    doc = odml.Document()
    doc.append(sec)
    odml.save(doc, "test.xml")

    validate(sec)
