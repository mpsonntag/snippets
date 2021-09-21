"""
Check all provided links from a poster gallery json file
for non http.StatusOK codes.
"""
import argparse
import json
import urllib.error

from typing import Dict, List
from urllib.request import Request, urlopen


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


def handle_url_check(url: str, info_line: str) -> str:
    """
    Checks a provided url for http.Status codes other than 200
    and redirects and returns the result as string.
    :param url: URL to be checked.
    :param info_line: Formatted line to identify the item the URL belongs to.
    :return: formatted str on error, empty str on success.
    """
    # Provide a user agent since some pages deny access when none is available.
    req = Request(url, headers={'User-Agent': 'PYTHON/3.9'})
    try:
        res = urlopen(req)
    except urllib.error.HTTPError as exc:
        return f"Code {exc} | {info_line}\n"

    if res.getcode() != 200:
        return f"Code {res.getcode()} | {info_line}\n"

    if res.geturl() != url:
        return f"Redirect {res.geturl()} | {info_line}\n"

    return ""


def handle_poster(data: List[Dict[str, str]]):
    """
    Iterates over all provided poster items and checks the http.StatusOK for
    every valid url item.
    :param data: list containing poster dictionary items.
    """
    print("Processing poster item links ...")
    fails = ""
    for idx, item in enumerate(data):
        abs_num = item['abstract_number']
        abs_id = item['id']
        info_rune = "•"

        for url_key in ["vimeo link", "individual video link"]:
            # check link availability
            if check_url := handle_link_item(item, url_key):
                info_line = f"Poster {abs_num}|{abs_id} {url_key}({check_url})"
                # check url and process resulting error messages
                if err := handle_url_check(check_url, info_line):
                    info_rune = "x"
                    fails += err

        if idx and not idx % 100:
            print(f" {idx}")
        print(info_rune, end="", flush=True)
    print(f"\n{fails}")


def handle_workshop(data: List[Dict[str, str]]):
    """
    Iterates over all provided poster items and checks the http.StatusOK for
    every valid url item.
    :param data: list containing workshop dictionary items.
    """
    print("Processing workshop item links ...")
    fails = ""
    for idx, item in enumerate(data):
        item_num = item['workshop number']
        info_rune = "•"

        for url_key in ["info url", "recording url"]:
            # check link availability
            if check_url := handle_link_item(item, url_key):
                info_line = f"Workshop {item_num} {url_key}({check_url})"
                # check url and process resulting error messages
                if err := handle_url_check(check_url, info_line):
                    info_rune = "x"
                    fails += err

        if idx and not idx % 100:
            print(f" {idx}")
        print(info_rune, end="", flush=True)
    print(f"\n{fails}")


def handle_exhibition(data: List[Dict[str, str]]):
    """
    Iterates over all provided exhibition items and checks the http.StatusOK for
    every valid url item.
    :param data: list containing exhibition dictionary items.
    """
    print("Processing exhibition item links ...")
    fails = ""
    for idx, item in enumerate(data):
        item_num = item['company_name']
        info_rune = "•"

        # exhibition has a number of 'material_' keys where urls can be referenced
        materials = list(filter(lambda cur: cur.startswith("material_"), item.keys()))
        materials.append("website")
        for url_key in materials:
            if check_url := handle_link_item(item, url_key):
                info_line = f"Exhibition {item_num} | {url_key}({check_url})"
                # check url and process resulting error messages
                if err := handle_url_check(check_url, info_line):
                    info_rune = "x"
                    fails += err

        if idx and not idx % 100:
            print(f" {idx}")
        print(info_rune, end="", flush=True)
    print(f"\n{fails}")


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
