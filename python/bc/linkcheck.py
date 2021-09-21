"""
Check all provided links from a poster gallery json file
for non http.StatusOK codes.
"""
import argparse
import json
import urllib.error

from typing import Dict, List
from urllib.request import urlopen


def handle_link_item(item: Dict[str, str], item_key: str) -> str:
    """
    Checks whether the item content for a provided dict key is a url
    and returns the url or an empty string if the check fails.
    :param item: a dictionary item.
    :param item_key: dictionary item key; the corresponding dictionary value
                     is checked whether it is a url.
    :return: url string
    """
    url = ""
    if item_key in item.keys() and item[item_key] and item[item_key].startswith("http"):
        url = item[item_key]
    return url


def handle_url_check(url: str, info_line: str):
    """
    Checks a provided url for http.Status codes other than 200
    and redirects and prints the result to the command line.
    :param url: URL to be checked.
    :param info_line: Formatted line to identify the item the URL belongs to.
    """
    try:
        res = urlopen(url)
    except urllib.error.HTTPError as exc:
        print(f"Code {exc} | {info_line}")
        return

    if res.getcode() != 200:
        print(f"Code {res.getcode()} | {info_line}")

    if res.geturl() != url:
        print(f"Redirect {res.geturl()} | {info_line}")


def handle_poster(data: List[Dict[str, str]]):
    """
    Iterates over all provided poster items and checks the http.StatusOK for
    every valid url item.
    :param data: list containing poster dictionary items.
    """
    print("Checking poster item links ...")
    for item in data:
        abs_num = item['abstract_number']
        abs_id = item['id']
        if check_url := handle_link_item(item, "vimeo link"):
            info_line = f"Poster {abs_num}|{abs_id} vimeo link({check_url})"
            handle_url_check(check_url, info_line)
        if check_url := handle_link_item(item, "individual video link"):
            info_line = f"Poster {abs_num}|{abs_id} individual video link({check_url})"
            handle_url_check(check_url, info_line)


def handle_workshop(data: List[Dict[str, str]]):
    """
    Iterates over all provided poster items and checks the http.StatusOK for
    every valid url item.
    :param data: list containing workshop dictionary items.
    """
    print("Checking workshop item links ...")
    for item in data:
        item_num = item['workshop number']
        if check_url := handle_link_item(item, "info url"):
            info_line = f"Workshop {item_num} info url({check_url})"
            handle_url_check(check_url, info_line)
        if check_url := handle_link_item(item, "recording url"):
            info_line = f"Workshop {item_num} recording url({check_url})"
            handle_url_check(check_url, info_line)


def handle_exhibition(data: List[Dict[str, str]]):
    """
    Iterates over all provided exhibition items and checks the http.StatusOK for
    every valid url item.
    :param data: list containing exhibition dictionary items.
    """
    print("Checking exhibition item links ...")
    for item in data:
        item_num = item['company_name']
        if check_url := handle_link_item(item, "website"):
            info_line = f"Exhibition {item_num} | website({check_url})"
            handle_url_check(check_url, info_line)

        materials = list(filter(lambda cur: cur.startswith("material_"), item.keys()))
        for mat in materials:
            if check_url := handle_link_item(item, mat):
                info_line = f"Exhibition {item_num} | {mat}({check_url})"
                handle_url_check(check_url, info_line)


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

        handle_workshop(data)
        print("Done ...")
        return

    if exhibition:
        print("Handling exhibition data ...")
        if not content_check(data, "company_name", json_file, "EXHIBITION"):
            return

        handle_exhibition(data)
        print("Done ...")
        return

    print("Handling poster data ...")
    if not content_check(data, "abstract_number", json_file, "POSTERS"):
        return

    handle_poster(data)
    print("Done ...")


if __name__ == "__main__":
    main()
