"""
Check all provided links from a poster gallery json file
for non http.StatusOK codes.
"""
import argparse
import json

from typing import Dict, List


def handle_poster(data: List[Dict[str, str]]):
    print(data)


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
        return

    if exhibition:
        print("Handling exhibition data ...")
        return

    print("Handling poster data ...")
    handle_poster(data)


if __name__ == "__main__":
    main()
