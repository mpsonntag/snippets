"""odmlFromDatacite

Convenience script to parse a datacite xml file
and create an odML xml file with the parsed information.

Usage: odmlFromDatacite FILENAME

Arguments:
    FILENAME    Path and filename of the datacite xml file to be parsed.

Options:
    -h --help   Show this screen.
    --version   Show version number.
"""

import os
import re
import sys
import xmltodict

from docopt import docopt
from xml.parsers.expat import ExpatError

import odml

from odml.dtypes import DType


VERSION = "0.1.0"


class ParserException(Exception):
    """
    Exception wrapper used by various odML parsers.
    """
    pass


class DataCiteItem(object):
    def __init__(self, sec_name, attribute_map, func, container_name=None, item_func=None):
        self.section_name = sec_name
        self.attribute_map = attribute_map
        self.func = func
        self.container_name = container_name
        self.item_func = item_func


def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def dict_from_xml(xml_file):
    """
    Parse the contents of an xml file into a python dictionary.

    :param xml_file: Location of the xml file to be parsed.
    :return: dictionary containing the contents of the xml file.
    """

    try:
        with open(xml_file) as file:
            doc = xmltodict.parse(file.read())
    except ExpatError as exc:
        raise ParserException("Could not parse file")

    return doc


def handle_container(helper, node, root_sec):
    if not node or helper.section_name not in node:
        return

    sec_cont_type = "datacite/%s" % camel_to_snake(helper.container_name)
    sub_sec_type = "datacite/%s" % camel_to_snake(helper.section_name)

    sec = odml.Section(name=helper.container_name,
                       type=sec_cont_type,
                       parent=root_sec)

    # We might need to handle the case, when a container holds
    # only the content of one xml element and does not contain
    # the content and attributes of this xml element as a sole
    # list element but as many elements within an OrderedDict.
    if isinstance(node[helper.section_name], list):
        for (idx, title_node) in enumerate(node[helper.section_name]):
            sec_name = "%s_%d" % (helper.section_name, idx + 1)
            sub_sec = odml.Section(name=sec_name,
                                   type=sub_sec_type,
                                   parent=sec)
            helper.item_func(helper, title_node, sub_sec)
    else:
        sub_sec = odml.Section(name="%s_1" % helper.section_name,
                               type=sub_sec_type,
                               parent=sec)
        helper.item_func(helper, node[helper.section_name], sub_sec)


def handle_sec(helper, node, root_sec):
    if not node:
        return

    sec_type = "datacite/%s" % camel_to_snake(helper.section_name)
    sec = odml.Section(name=helper.section_name,
                       type=sec_type,
                       parent=root_sec)

    handle_props(helper, node, sec)


def handle_props(helper, node, sec):
    if not node:
        return

    # Handle special case if a node is just the string content of an XML element.
    if isinstance(node, str):
        odml.Property(name=helper.section_name, values=node, parent=sec)
    else:
        for sub in node:
            if sub in helper.attribute_map:
                dtype = DType.string
                if isinstance(sub, str) and sub.endswith("URI"):
                    dtype = DType.url

                odml.Property(name=helper.attribute_map[sub], dtype=dtype,
                              values=node[sub], parent=sec)
            else:
                print("[Warning] Ignoring node '%s/%s'" % (sec.name, sub))


def handle_creators_item(helper, node, sec):
    sub_type_base = "datacite/creator"

    for sub in node:
        if sub == "creatorName":
            odml.Property(name=sub, values=node[sub]["#text"], parent=sec)
            if "@nameType" in node[sub]:
                odml.Property(name="nameType", values=node[sub]["@nameType"], parent=sec)

        elif sub in ["givenName", "familyName"]:
            odml.Property(name=sub, values=node[sub], parent=sec)
        elif sub == "nameIdentifier":
            # toDo handle multiple name identifier
            subsec = odml.Section(name=sub,
                                  type="%s/named_identifier" % sub_type_base,
                                  parent=sec)
            odml.Property(name=sub, values=node[sub]["#text"], parent=subsec)
            if "@schemeURI" in node[sub]:
                odml.Property(name="schemeURI", dtype=DType.url,
                              values=node[sub]["@schemeURI"], parent=subsec)
            if "@nameIdentifierScheme" in node[sub]:
                odml.Property(name="nameIdentifierScheme",
                              values=node[sub]["@nameIdentifierScheme"], parent=subsec)

        elif sub == "affiliation":
            # toDo handle multiple affiliations
            sec_aff = odml.Section(name=sub,
                                   type="%s/affiliation" % sub_type_base,
                                   parent=sec)
            odml.Property(name=sub, values=node[sub]["#text"], parent=sec_aff)
            if "@affiliationIdentifier" in node[sub]:
                odml.Property(name="affiliationIdentifier",
                              values=node[sub]["@affiliationIdentifier"],
                              parent=sec_aff)
            if "@affiliationIdentifierScheme" in node[sub]:
                odml.Property(name="affiliationIdentifierScheme",
                              values=node[sub]["@affiliationIdentifierScheme"],
                              parent=sec_aff)
            if "@schemeURI" in node[sub]:
                odml.Property(name="schemeURI", values=node[sub]["@schemeURI"],
                              dtype=DType.url, parent=sec_aff)
        else:
            print("[Warning] Ignoring unsupported attribute '%s'" % sub)


def handle_funding_references(_, node, sec):
    for sub in node:
        if sub in ["funderName", "awardTitle"]:
            odml.Property(name=sub, values=node[sub], parent=sec)
        elif sub == "awardNumber":
            award_number_map = {"#text": "awardNumber", "@awardURI": "awardURI"}
            award_number_helper = DataCiteItem(sec_name=sub,
                                               attribute_map=award_number_map,
                                               func=None)
            handle_props(award_number_helper, node[sub], sec)
        elif sub == "funderIdentifier":
            funder_identifier_map = {
                "#text": "funderIdentifier",
                "@funderIdentifierType": "funderIdentifierType",
                "@schemeURI": "schemeURI"}
            funder_identifier_helper = DataCiteItem(sec_name=sub,
                                                    attribute_map=funder_identifier_map,
                                                    func=None)
            handle_props(funder_identifier_helper, node[sub], sec)


def parse_datacite_dict(doc):
    """
    :param doc: python dict containing datacite conform data to
                be parsed.
    """
    if not doc or "resource" not in doc:
        raise ParserException("Could not find root")

    dcite_root = doc["resource"]
    if "identifier" not in dcite_root:
        raise ParserException("Could not find identifier (DOI) node")

#    supported_tags = ["contributors", "geoLocations"]

    identifier_map = {
        "#text": "identifier",
        "@identifierType": "identifierType"
    }
    identifier_helper = DataCiteItem(sec_name="identifier",
                                     attribute_map=identifier_map,
                                     func=handle_sec)

    creators_helper = DataCiteItem(sec_name="creator",
                                   attribute_map=None,
                                   func=handle_container,
                                   container_name="creators",
                                   item_func=handle_creators_item)

    title_map = {
        "#text": "title",
        "@titleType": "titleType"
    }
    title_helper = DataCiteItem(sec_name="title",
                                attribute_map=title_map,
                                func=handle_container,
                                container_name="titles",
                                item_func=handle_props)

    publisher_helper = DataCiteItem(sec_name="publisher",
                                    attribute_map={"#text": "publisher"},
                                    func=handle_props)

    publication_year_helper = DataCiteItem(sec_name="publicationYear",
                                           attribute_map={"#text": "publicationYear"},
                                           func=handle_props)

    subjects_map = {
        "#text": "subject",
        "@schemeURI": "schemeURI",
        "@subjectScheme": "subjectScheme",
        "@valueURI": "valueURI"
    }
    subjects_helper = DataCiteItem(sec_name="subject",
                                   attribute_map=subjects_map,
                                   func=handle_container,
                                   container_name="subjects",
                                   item_func=handle_props)

    dates_map = {
        "#text": "date",
        "@dateType": "dateType",
        "@dateInformation": "dateInformation"
    }
    dates_helper = DataCiteItem(sec_name="date",
                                attribute_map=dates_map,
                                func=handle_container,
                                container_name="dates",
                                item_func=handle_props)

    language_helper = DataCiteItem(sec_name="language",
                                   attribute_map={"#text": "language"},
                                   func=handle_props)

    res_type_map = {
        "#text": "resourceType",
        "@resourceTypeGeneral": "resourceTypeGeneral"
    }
    res_type_helper = DataCiteItem(sec_name="resourceType",
                                   attribute_map=res_type_map,
                                   func=handle_sec)

    alternate_identifiers_map = {
        "#text": "alternateIdentifier",
        "@alternateIdentifierType": "alternateIdentifierType"
    }
    alternate_identifiers_helper = DataCiteItem(sec_name="alternateIdentifier",
                                                attribute_map=alternate_identifiers_map,
                                                func=handle_container,
                                                container_name="alternateIdentifiers",
                                                item_func=handle_props)

    related_identifiers_map = {
        "#text": "relatedIdentifier",
        "@relatedIdentifierType": "relatedIdentifierType",
        "@relationType": "relationType",
        "@relatedMetadataScheme": "relatedMetadataScheme",
        "@schemeURI": "schemeURI",
        "@schemeType": "schemeType",
        "@resourceTypeGeneral": "resourceTypeGeneral"
    }
    related_identifiers_helper = DataCiteItem(sec_name="relatedIdentifier",
                                              attribute_map=related_identifiers_map,
                                              func=handle_container,
                                              container_name="relatedIdentifiers",
                                              item_func=handle_props)

    sizes_helper = DataCiteItem(sec_name="size",
                                attribute_map={"#text": "size"},
                                func=handle_container,
                                container_name="sizes",
                                item_func=handle_props)

    formats_helper = DataCiteItem(sec_name="format",
                                  attribute_map={"#text": "format"},
                                  func=handle_container,
                                  container_name="formats",
                                  item_func=handle_props)

    version_helper = DataCiteItem(sec_name="version",
                                  attribute_map={"#text": "version"},
                                  func=handle_props)

    rights_map = {
        "@schemeURI": "schemeURI",
        "@rightsIdentifierScheme": "rightsIdentifierScheme",
        "@rightsIdentifier": "rightsIdentifier",
        "@rightsURI": "rightsURI"
    }
    rights_helper = DataCiteItem(sec_name="rights",
                                 attribute_map=rights_map,
                                 func=handle_container,
                                 container_name="rightsList",
                                 item_func=handle_props)

    descriptions_map = {
        "#text": "description",
        "@descriptionType": "descriptionType"
    }
    descriptions_helper = DataCiteItem(sec_name="description",
                                       attribute_map=descriptions_map,
                                       func=handle_container,
                                       container_name="descriptions",
                                       item_func=handle_props)

    funding_references_helper = DataCiteItem(sec_name="fundingReference",
                                             attribute_map=None,
                                             func=handle_container,
                                             container_name="fundingReferences",
                                             item_func=handle_funding_references)

    supported_tags = {
        "identifier": identifier_helper,
        "creators": creators_helper,
        "titles": title_helper,
        "publisher": publisher_helper,
        "publicationYear": publication_year_helper,
        "subjects": subjects_helper,
        "dates": dates_helper,
        "language": language_helper,
        "resourceType": res_type_helper,
        "alternateIdentifiers": alternate_identifiers_helper,
        "relatedIdentifiers": related_identifiers_helper,
        "sizes": sizes_helper,
        "formats": formats_helper,
        "version": version_helper,
        "rightsList": rights_helper,
        "descriptions": descriptions_helper,
        "fundingReferences": funding_references_helper
    }

    odml_doc = odml.Document()
    odml_doc.repository = "https://terminologies.g-node.org/v1.1/terminologies.xml"

    root_sec = odml.Section(name="DataCite", type="data_reference", parent=odml_doc)

    for node_tag in dcite_root:
        if node_tag in supported_tags:
            helper = supported_tags[node_tag]
            helper.func(helper, dcite_root[node_tag], root_sec)
        else:
            print("[Warning] Ignoring unsupported root node '%s'" % node_tag)

    # ToDo remove DEBUG prints
    print(doc)
    print()
    print(odml_doc.pprint())
    print()
    print(odml_doc.sections[0].pprint())
    print()
    print(odml_doc.sections[0].properties)
    odml.save(odml_doc, '/home/msonntag/Chaos/DL/doi_odml.odml')


def main(args=None):
    parser = docopt(__doc__, argv=args, version=VERSION)

    cite_file = parser['FILENAME']
    if not os.path.isfile(cite_file):
        print("[Error] Could not access input file '%s'\n" % cite_file)
        exit(1)

    doc = None
    try:
        doc = dict_from_xml(cite_file)
    except ParserException as exc:
        print("[Error] '%s' in file '%s'" % (exc, cite_file))
        exit(1)

    try:
        parse_datacite_dict(doc)
    except ParserException as exc:
        print("[Error] Could not parse input file '%s'\n\t%s" % (cite_file, exc))
        exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
