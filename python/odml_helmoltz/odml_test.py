import odml

"""
array    N_Par.Geo_CLFH_31
    \\u -
    \\r 0:999999
    \\d Parameters of Crown length factor-Height-function of a single tree (group-specific)
    typeOfArray    float
    dimension    3    3
data
    0.4    0.4    0.4
    0.0    0.0    0.0
    0.0    0.0    0.0
end
"""


def store_geo_param(name):
    section = odml.Section(name, "NPar.geo.clfh")
    section.create_property("data_range", [0, 999999])
    section.create_property("data_type", "float")
    section.create_property("data_dimension", [3, 3])
    p = section.create_property("data", ["(0.4; 0.4; 0.4)", "(0.4; 0.4; 0.4)", "(0.4; 0.4; 0.4)"], dtype="3-tuple")

    return section


def validate(section):
    from IPython import embed
    embed()
    must = {"data_dimension": [3, 3]}
    exists = ["data_range"]
    for m in must:
        if not section.properties[m].values == must[m]:
            raise ValueError(f"Property {m} does not match requirement {must[m]}")
    for e in exists:
        if e not in section.properties:
            raise ValueError(f"Required property {e} does not exist!")
    return True


if __name__ == "__main__":
    sec = store_geo_param("test")
    doc = odml.Document()
    doc.append(sec)
    odml.save(doc, "test.xml")

    validate(sec)
