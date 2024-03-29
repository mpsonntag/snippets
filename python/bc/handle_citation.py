"""
Parse DOI information from entries in a json file and print all formatted DOI
citations to the command line.
"""
import argparse
import json

from datetime import date
from typing import Dict, Any


def citation_info(item: Dict[str, Any]) -> (str, str):
    """
    Parse citation information from a dict item and return a formatted list
    entry and doi item
    :param item: Dictionary containing author and DOI information.
    :return: tuple containing a citation list item string and a DOI item string
    """
    cit_list = ""
    for auth in item["authors"]:
        first_name = ""
        if "firstName" in auth.keys() and len(auth["firstName"]) > 0:
            first_name = f" {auth['firstName'][0]}."
        mid_name = ""
        if "middleName" in auth.keys() and auth["middleName"] and len(auth["middleName"]) > 0:
            mid_name = f" {auth['middleName'][0]}."
        citation = f"{auth['lastName']}{first_name}{mid_name}"
        cit_list = f"{cit_list}, {citation}" if len(cit_list) > 0 else citation
    doi_item = ""
    if "doi" in item.keys() and item["doi"] and len(item["doi"]) > 0:
        doi_item = f' doi: <a href="https://doi.org/{item["doi"]}">{item["doi"]}</a>'

    return cit_list, doi_item


def main():
    """
    Parse DOI information from entries in a json file and print all formatted DOI
    citations to the command line.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", help="JSON file containing abstracts data")
    args = parser.parse_args()

    in_file = args.json_file
    with open(in_file, encoding="utf-8") as jfp:
        data = json.load(jfp)

    for item in data:
        cit_list, doi_item = citation_info(item)

        year = date.today().year
        copy_item = f"Copyright: © ({year}) {cit_list}" if cit_list else ""
        cit_item = f"Citation: {cit_list} ({year}) {item['title']}. " \
                   f"Bernstein Conference {year}.{doi_item}"

        print(f"{copy_item}\n{cit_item}")


if __name__ == "__main__":
    main()
