"""odmlFromDatacite

Convenience script to parse a datacite XML file or whole directories
containing datacite XML files and create odML files with the parsed
information.

Usage: odmlFromDatacite [-f FORMAT] [-o OUT] [-r] [-p] INPUT

Arguments:
    INPUT    Path and filename of the datacite XML file to be parsed.
             If used with the [-r] flag, INPUT should be a directory;
             all datacite XML files within this directory and any sub
             directories will be parsed to odML.

Options:
    -f FORMAT   odML output file format. Available formats are
                  'XML', 'JSON', 'YAML', 'RDF'. Default format is 'XML'.
    -o OUT      Output directory. Must exist if specified.
                  If not specified, output files will be written to the
                  current directory.
    -r          [Optional] Walk recursively through a repository.
                  and convert all datacite files found.
    -p          [Optional] Print the parsed document tree(s) to the command line.
                   Default is False.
    -h --help   Show this screen.
    --version   Show version number.
"""

import os
import pathlib
import re
import sys

from datetime import date
from xml.parsers.expat import errors as exp_err
from xml.parsers.expat import ExpatError

import xmltodict

from docopt import docopt
from odml import Document, Section, Property
from odml.fileio import save as save_odml
from odml.dtypes import DType
from odml.tools.parser_utils import SUPPORTED_PARSERS


VERSION = "0.1.0"


class ParserException(Exception):
    """
    Exception wrapper used by various odML parsers.
    """


class DataCiteItem:
    """
    Main class to bundle Datacite specific item data and the functions to convert
    them to the corresponding odML Section-Properties.
    section_name: odML section name of a Datacite Item.
    attribute_map: dict containing the mapping of Datacite XML attributes
                   to the corresponding odML names.
    func: function to handle the conversion from DataCite items to odML entities.
    container_name: odml name how a Datacite container Section should be called in odML.
    item_func: function to handle the conversion of Datacite items to odML entities that are
               additionally wrapped within a Datacite container item.
    """
    def __init__(self, sec_name, attribute_map, func, container_name=None, item_func=None):
        self.section_name = sec_name
        self.attribute_map = attribute_map
        self.func = func
        self.container_name = container_name
        self.item_func = item_func


def camel_to_snake(in_string):
    """
    Convert Camel-case strings to all lower snake case strings.
    """
    tmp = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', in_string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', tmp).lower()


def dict_from_xml(xml_file):
    """
    Parse the contents of an xml file into a python dictionary.

    :param xml_file: Location of the xml file to be parsed.
    :return: dictionary containing the contents of the xml file.
    """

    try:
        with open(xml_file, encoding="utf-8") as file:
            doc = xmltodict.parse(file.read())
    except ExpatError as exc:
        raise ParserException(f"{exp_err.messages[exc.code]}").with_traceback(exc.__traceback__)

    return doc


def handle_container(helper, node, root_sec):
    """
    Creates an odML section from a passed DataCiteItem and the corresponding Datacite XML Node.
    Since its assumed, that the passed Datacite XML node is a container, the function to
    handle sub-items is called to create odML entries from all container items.

    :param helper: DataCiteItem helper class containing the odml Section name and
                   odml conversion functions.
    :param node: Datacite Python dict node containing the container and child item data.
    :param root_sec: odml Section the created odml container section and all its children are
                     appended to.
    """
    if not node or helper.section_name not in node:
        return

    sec_cont_type = f"datacite/{camel_to_snake(helper.container_name)}"
    sub_sec_type = f"datacite/{camel_to_snake(helper.section_name)}"

    sec = Section(name=helper.container_name, type=sec_cont_type, parent=root_sec)

    handle_sub_container(helper, node, sec, sub_sec_type)


def handle_sub_container(helper, node, sec, sub_sec_type):
    """
    Creates odml Sections for all child items and odml Properties for all attributes.
    :param helper: DataCiteItem helper class containing the odml Section name and
                   odml conversion functions.
    :param node: Datacite XML node containing the container child item data.
    :param sec: odml Section all created Sections are appended to.
    :param sub_sec_type: string containing the odML sub-section type
    """
    # We might need to handle the case, when a container holds
    # only the content of one xml element and does not contain
    # the content and attributes of this xml element as a sole
    # list element but as many elements within an OrderedDict.
    if isinstance(node[helper.section_name], list):
        for (idx, title_node) in enumerate(node[helper.section_name]):
            sec_name = "%s_%d" % (helper.section_name, idx + 1)
            sub_sec = Section(name=sec_name, type=sub_sec_type, parent=sec)
            helper.item_func(helper, title_node, sub_sec)
    else:
        sub_sec_name = f"{helper.section_name}_1"
        sub_sec = Section(name=sub_sec_name, type=sub_sec_type, parent=sec)
        helper.item_func(helper, node[helper.section_name], sub_sec)


def handle_sec(helper, node, root_sec):
    """
    Creates an odML Section from a passed DataCiteItem and the corresponding Datacite XML Node.

    :param helper: DataCiteItem helper class containing the odml Section name and
                   odml conversion functions.
    :param node: Datacite Python dict node containing the item data.
    :param root_sec: odml Section the created odml Section is appended to.
    """
    if not node:
        return

    sec_type = f"datacite/{camel_to_snake(helper.section_name)}"
    sec = Section(name=helper.section_name, type=sec_type, parent=root_sec)

    handle_props(helper, node, sec)


def handle_props(helper, node, sec):
    """
    Creates an odML Property from a passed DataCiteItem and the corresponding Datacite XML Node.

    :param helper: DataCiteItem helper class containing the odml conversion mapping.
    :param node: Datacite Python dict node containing the item data.
    :param sec: odml Section the created odml Property is appended to.
    """
    if not node:
        return

    # Handle special case if a node is just the string content of an XML element.
    if isinstance(node, str):
        Property(name=helper.section_name, values=node, parent=sec)
    else:
        for sub in node:
            if sub in helper.attribute_map:
                dtype = DType.string
                if isinstance(sub, str) and sub.endswith("URI"):
                    dtype = DType.url

                Property(name=helper.attribute_map[sub], dtype=dtype,
                         values=node[sub], parent=sec)
            else:
                print(f"[Warning] Ignoring node '{sec.name}/{sub}'")


def handle_name_identifiers(sub, node, sub_type_base, sec):
    """
    Specifies all information needed to convert Datacite "NameIdentifier" data
    to odML and runs the conversion.

    :param sub: string containing the odML section name of this item.
    :param node: Datacite Python dict node containing the item data.
    :param sub_type_base: string containing the base name of the used odML Section type.
    :param sec: odML Section the created odML data will be appended to.
    """
    name_identifier_map = {
        "#text": "nameIdentifier",
        "@schemeURI": "schemeURI",
        "@nameIdentifierScheme": "nameIdentifierScheme"
    }
    name_identifier_helper = DataCiteItem(sec_name=sub,
                                          attribute_map=name_identifier_map,
                                          func=None,
                                          item_func=handle_props)
    sub_sec_type = f"{sub_type_base}/named_identifier"
    handle_sub_container(name_identifier_helper, node, sec, sub_sec_type)


def handle_affiliations(sub, node, sub_type_base, sec):
    """
    Specifies all information needed to convert Datacite "Affiliation" data
    to odML and runs the conversion.

    :param sub: string containing the odML section name of this item.
    :param node: Datacite Python dict node containing the item data.
    :param sub_type_base: string containing the base name of the used odML Section type.
    :param sec: odML Section the created odML data will be appended to.
    """
    affiliation_map = {
        "#text": "affiliation",
        "@affiliationIdentifier": "affiliationIdentifier",
        "@affiliationIdentifierScheme": "affiliationIdentifierScheme",
        "@schemeURI": "schemeURI"
    }
    affiliation_helper = DataCiteItem(sec_name=sub,
                                      attribute_map=affiliation_map,
                                      func=None,
                                      item_func=handle_props)
    sub_sec_type = f"{sub_type_base}/affiliation"
    handle_sub_container(affiliation_helper, node, sec, sub_sec_type)


def handle_creators_item(_, node, sec):
    """
    Specifies all information needed to convert Datacite "Creators" single item data
    to odML and runs the conversion.

    :param node: Datacite Python dict node containing the item data.
    :param sec: odML Section the created odML data will be appended to.
    """
    sub_type_base = "datacite/creator"

    for sub in node:
        if sub == "creatorName":
            creator_name_map = {
                "#text": "creatorName",
                "@nameType": "nameType"
            }
            creator_name_helper = DataCiteItem(sec_name=sub,
                                               attribute_map=creator_name_map,
                                               func=None)
            handle_props(creator_name_helper, node[sub], sec)
        elif sub in ["givenName", "familyName"]:
            if isinstance(node[sub], str):
                Property(name=sub, values=node[sub], parent=sec)
            elif "#text" in node[sub]:
                Property(name=sub, values=node[sub]["#text"], parent=sec)
            else:
                print(f"[Warning] Could not parse '{sub_type_base}/{sub}'")
        elif sub == "nameIdentifier":
            handle_name_identifiers(sub, node, sub_type_base, sec)
        elif sub == "affiliation":
            handle_affiliations(sub, node, sub_type_base, sec)
        else:
            print(f"[Warning] Ignoring unsupported attribute '{sub}'")


def handle_contributors_item(_, node, sec):
    """
    Specifies all information needed to convert Datacite "Contributors" single item data
    to odML and runs the conversion.

    :param node: Datacite Python dict node containing the item data.
    :param sec: odML Section the created odML data will be appended to.
    """
    sub_type_base = "datacite/contributor"

    for sub in node:
        if sub in ["contributorName", "givenName", "familyName"]:
            if isinstance(node[sub], str):
                Property(name=sub, values=node[sub], parent=sec)
            elif "#text" in node[sub]:
                Property(name=sub, values=node[sub]["#text"], parent=sec)
            else:
                print(f"[Warning] Could not parse '{sub_type_base}/{sub}'")
        elif sub == "@contributorType":
            Property(name="contributorType", values=node[sub], parent=sec)
        elif sub == "nameIdentifier":
            handle_name_identifiers(sub, node, sub_type_base, sec)
        elif sub == "affiliation":
            handle_affiliations(sub, node, sub_type_base, sec)
        else:
            print(f"[Warning] Ignoring unsupported attribute '{sub}'")


def handle_geo_entry(helper_list, node, sec, sub_sec_name, sub_sec_type):
    """
    Specifies all information needed to convert Datacite "GeoEntry" data
    to odML and runs the conversion.
    """
    sub_sec = Section(name=sub_sec_name, type=sub_sec_type, parent=sec)

    for entry in node:
        if entry in helper_list:
            try:
                Property(name=entry, dtype=DType.float,
                         values=node[entry], parent=sub_sec)
            except ValueError:
                print(f"[Warning] Skipping invalid '{entry}' value '{node[entry]}'")


def handle_geo_locations(_, node, sec):
    """
    Specifies all information needed to convert Datacite "GeoLocations" single item data
    to odML and runs the conversion.

    :param node: Datacite Python dict node containing the item data.
    :param sec: odML Section the created odML data will be appended to.
    """
    sub_type_base = "datacite/geo_location"

    point_list = ["pointLongitude", "pointLatitude"]
    box_list = ["westBoundLongitude", "eastBoundLongitude",
                "southBoundLatitude", "northBoundLatitude"]

    for elem in node:
        if elem == "geoLocationPlace":
            Property(name=elem, values=node[elem], parent=sec)
        elif elem == "geoLocationPoint":
            sec_type = f"{sub_type_base}/{camel_to_snake(elem)}"
            handle_geo_entry(point_list, node[elem], sec, elem, sec_type)
        elif elem == "geoLocationBox":
            sec_type = f"{sub_type_base}/{camel_to_snake(elem)}"
            handle_geo_entry(box_list, node[elem], sec, elem, sec_type)
        elif elem == "geoLocationPolygon":
            sub_type = f"{sub_type_base}/{camel_to_snake(elem)}"
            sub_sec = Section(name=elem, type=sub_type, parent=sec)

            for (idx, point) in enumerate(node[elem]["polygonPoint"]):
                point_name = "polygonPoint_%d" % (idx + 1)
                sec_type = f"{sub_type_base}/{camel_to_snake('polygonPoint')}"
                handle_geo_entry(point_list, point, sub_sec, point_name, sec_type)


def handle_funding_references(_, node, sec):
    """
    Specifies all information needed to convert Datacite "FundingReferences" single item data
    to odML and runs the conversion.

    :param node: Datacite XML node containing the item data.
    :param sec: odML Section the created odML data will be appended to.
    """
    for sub in node:
        if sub in ["funderName", "awardTitle"]:
            Property(name=sub, values=node[sub], parent=sec)
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


def setup_supported_tags():
    """
    Creates DataCite item to odml name mappings for all supported Datacite items and
    provides them via a dictionary of specific DataCiteItem objects.
    This also provides the mappings whether a DataCite item needs to be handled as
    a single DataItem entry or as a Container item entry providing the functions required
    to parse the individual items of the container node content.
    """
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

    contributors_helper = DataCiteItem(sec_name="contributor",
                                       attribute_map=None,
                                       func=handle_container,
                                       container_name="contributors",
                                       item_func=handle_contributors_item)

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

    geo_locations_helper = DataCiteItem(sec_name="geoLocation",
                                        attribute_map=None,
                                        func=handle_container,
                                        container_name="geoLocations",
                                        item_func=handle_geo_locations)

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
        "contributors": contributors_helper,
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
        "geoLocations": geo_locations_helper,
        "fundingReferences": funding_references_helper
    }

    return supported_tags


def parse_datacite_dict(doc):
    """
    Creates an odML document and parses the passed dictionary containing DataCite entries
    to odML, appending the resulting data to the odML document.

    :param doc: Python dict containing DataCite conform data to be parsed.
    :returns: The resulting odML document.
    """
    if not doc or "resource" not in doc:
        raise ParserException("Could not find root")

    datacite_root = doc["resource"]
    if "identifier" not in datacite_root:
        raise ParserException("Could not find identifier (DOI) node")

    odml_doc = Document()
    odml_doc.repository = "https://terminologies.g-node.org/v1.1/terminologies.xml"
    odml_doc.date = date.today().isoformat()

    root_sec = Section(name="DataCite", type="data_reference", parent=odml_doc)

    supported_tags = setup_supported_tags()
    for node_tag in datacite_root:
        if node_tag in supported_tags:
            helper = supported_tags[node_tag]
            helper.func(helper, datacite_root[node_tag], root_sec)
        else:
            print(f"[Warning] Ignoring unsupported root node '{node_tag}'")

    return odml_doc


def handle_document(cite_in, out_root, backend="XML", print_doc=False):
    """
    Parses a DataCite XML file to odML and saves the odML file in the specified file format.

    :param cite_in: DataCite xml file to be opened.
    :param out_root: Directory to save the resulting odML file to.
    :param backend: odML file format; default is XML; YAML, JSON, RDF are supported.
    :param print_doc: Whether the odML document content should also be printed to the command line.
                      Default is False.
    """
    print(f"[INFO] Handling file '{cite_in}'")

    # Read document from input file
    doc = None
    try:
        doc = dict_from_xml(cite_in)
    except ParserException as exc:
        exc_message = f"[Error] Could not parse datacite file '{cite_in}'\n\t{exc}"
        raise ParserException(exc_message).with_traceback(exc.__traceback__)

    # Parse input to an odML document
    try:
        odml_doc = parse_datacite_dict(doc)
    except ParserException as exc:
        exc_message = f"[Error] Could not parse datacite file '{cite_in}'\n\t{exc}"
        raise ParserException(exc_message).with_traceback(exc.__traceback__)

    if print_doc:
        print()
        print(odml_doc.pprint(max_depth=5))

    out_name = os.path.splitext(os.path.basename(cite_in))[0]
    out_file = os.path.join(out_root, f"{out_name}.{backend.lower()}")

    # Do not overwrite existing files
    if os.path.isfile(out_file):
        out_file = os.path.join(out_root, f"{out_name}(copy).{backend.lower()}")

    save_odml(odml_doc, out_file, backend)


def main(args=None):
    """
    Parses the command line arguments and calls the corresponding functions.
    """
    parser = docopt(__doc__, argv=args, version=VERSION)

    recursive = parser["-r"]
    cite_in = parser["INPUT"]

    if not recursive and not os.path.isfile(cite_in):
        print(f"[Error] Could not access input file '{cite_in}'\n")
        return sys.exit(1)

    if recursive and not os.path.isdir(cite_in):
        print(f"[Error] Could not access input directory '{cite_in}'\n")
        return sys.exit(1)

    # Handle output file format
    backend = "XML"
    if parser["-f"]:
        backend = parser["-f"].upper()
        if backend not in SUPPORTED_PARSERS:
            print(f"[Error] Output format '{backend}' is not supported. \n")
            print(docopt(__doc__, "-h"))
            return sys.exit(1)

    # Handle output directory
    out_root = os.getcwd()
    if parser["-o"]:
        if not os.path.isdir(parser["-o"]):
            print(f"[Error] Could not find output directory '{parser['-o']}'")
            return sys.exit(1)

        out_root = parser["-o"]

    print_file = parser["-p"]

    # File conversion
    if recursive:
        xfiles = list(pathlib.Path(cite_in).rglob('*.xml'))
        for file in xfiles:
            try:
                handle_document(file, out_root, backend, print_file)
            except ParserException as exc:
                print(exc)
    else:
        try:
            handle_document(cite_in, out_root, backend, print_file)
        except ParserException as exc:
            print(exc)
            return sys.exit(1)

    return sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
