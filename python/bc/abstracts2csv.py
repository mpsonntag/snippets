"""
Convert the GCA abstract json output of the GCA-client script to a TSV file
"""

import argparse
import json


ABSTRACT_KEYS = ["abstrTypes", "acknowledgements", "affiliations", "authors", "conference",
                 "conflictOfInterest", "doi", "favUsers", "figures", "isTalk", "mtime",
                 "reasonForTalk", "references", "sortId", "state", "stateLog", "text",
                 "title", "topic", "uuid"]
ABSTR_TYPES_KEYS = ["name", "prefix", "short", "uuid"]
AUTHOR_KEYS = ["affiliations", "firstName", "lastName", "mail", "middleName", "position", "uuid"]
AFFILIATION_KEYS = ["address", "country", "department", "section", "position", "uuid"]
REFERENCES_KEYS = ["doi", "link", "text", "uuid"]


def main():
    """
    Parse an abstract service json file and print the information to a CSV file.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", help="JSON file containing abstracts data")
    args = parser.parse_args()

    in_file = args.json_file
    with open(in_file, encoding="utf-8") as jfp:
        data = json.load(jfp)


if __name__ == "__main__":
    main()
