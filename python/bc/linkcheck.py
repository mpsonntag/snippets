"""
Check all provided links from a poster gallery json file
for non http.StatusOK codes.
"""
import argparse
import json

from typing import Dict, List


def handle_poster(data: List[Dict[str, str]]):
    """
    Iterate over all provided poster items and check the http.StatusOK for
    every full and derivative link item.
    :param data: list containing poster dictionary items.
    """


def content_check(data: List[Dict[str, str]], check: str,
                  json_file: str, msg: str) -> bool:
    """
    Checks whether a dictionary contains a column specific to expected data and returns
    a corresponding boolean value. This avoids writing files of an invalid gallery type.
    :param data: list containing poster dictionary items.
    :param check: name of the column that is supposed to be found in the dictionary items.
    :param json_file: name of the file containing the data
    :param msg: String displayed in command line print.
    :return: True if the column was found in the data, False otherwise.
    """
    if not data or check not in data[0].keys():
        print(f"'{json_file}' does not seem to be a valid {msg} file ...")
        print("Aborting ...")
        return False
    return True


def main():
    """
    Parse command line arguments and run the URL checks with the data provided.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workshops", dest="workshops", action="store_true",
                        help="Create workshop pages instead of posters")
    parser.add_argument("--exhibition", dest="exhibition", action="store_true",
                        help="Create exhibition pages instead of posters")
    parser.add_argument("jsonfile", help="JSON file with the poster data")
    args = parser.parse_args()

    workshops = args.workshops
    exhibition = args.exhibition

    json_file = args.jsonfile
    with open(json_file) as jfp:
        data = json.load(jfp)

    if workshops:
        print("Handling workshops data ...")
        if not content_check(data, "workshop number", json_file, "WORKSHOP"):
            return

        return

    if exhibition:
        print("Handling exhibition data ...")
        if not content_check(data, "company_name", json_file, "EXHIBITION"):
            return

        return

    print("Handling poster data ...")
    if not content_check(data, "abstract_number", json_file, "POSTERS"):
        return

    handle_poster(data)


if __name__ == "__main__":
    main()
