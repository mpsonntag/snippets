"""
UFZ Leipzig odml concept script

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

> To summarize:
> 1. we want to be able to store n dimensional values
> 2. currently d-type describes the data type or the dimension (if
> 2-tuple or 3-tuple is used), in the latter case float is assumed. For
> the example we would need dimension besides dtype, to store both
> attributes.
> 3. we need the attribute range

Full metadata to be stored in odml: "net_dict" found at
https://github.com/nest/nest-simulator/blob/master/pynest/examples/Potjans_2014/network_params.py
"""

import odml
import odml.validation as oval

from odml.tools.parser_utils import ParserException


def store_geo_param(name):
    # providing a section type enables filtering large odml file
    # with multiple similar occurrences.
    section_type = "Crown-length-parameters"
    section = odml.Section(name, section_type)
    section.create_property("data_range", [0, 999999])
    section.create_property("data_typeOfArray", "float")
    section.create_property("data_dimension", [3, 3])
    _ = section.create_property("data", ["(0.4; 0.4; 0.4)",
                                         "(0.4; 0.4; 0.4)",
                                         "(0.4; 0.4; 0.4)"], dtype="3-tuple")

    return section


def validate_sec_crown_length_handler(obj):
    validation_id = oval.IssueID.custom_validation
    # validation is specific to sections of type "crown-length"
    if not obj.type == "Crown-length-parameters":
        return

    # ensure that the section contains the 'data_type' property
    if "data_typeOfArray" not in obj.properties:
        msg = "data_typeOfArray property is missing"
        yield oval.ValidationError(obj, msg, oval.LABEL_ERROR, validation_id)
    # ensure that the section contains the 'data_dimension' property
    if "data_dimension" not in obj.properties:
        msg = "data_dimension property is missing"
        yield oval.ValidationError(obj, msg, oval.LABEL_ERROR, validation_id)
    # warn if the section does not contain the 'data_range' property
    if "data_range" not in obj.properties:
        msg = "data_range property is missing"
        yield oval.ValidationError(obj, msg, oval.LABEL_WARNING, validation_id)


if __name__ == "__main__":
    # section names have to be unique on their section level
    doc = odml.Document()
    sec = store_geo_param(name="NPar.geo.clfh")
    doc.append(sec)

    # save the document to file
    odml.save(doc, "crown_length.xml")

    # register a custom validation handler ensuring, that "crown_length" sections are
    # only saved if they have been properly added.
    oval.Validation.register_handler("section", validate_sec_crown_length_handler)

    # add a crown_length section that does not contain all required properties
    invalid_sec = doc.create_section(name="NPar.geo.clfh_invalid",
                                     type="Crown-length-parameters")

    # the document can now no longer be saved since the latest crown length section
    # contains validation errors
    try:
        odml.save(doc, "crown_length.xml")
    except ParserException as exc:
        print(exc)

    # adding the required properties to the invalid section
    invalid_sec.create_property("data_dimension", [3, 3])
    invalid_sec.create_property("data_typeOfArray", "float")

    # saving now works again, but a warning is reported on file save, since the
    # "data_range" property is still missing
    odml.save(doc, "crown_length.xml")
