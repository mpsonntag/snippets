import argparse
import csv
import json
import os

from typing import Dict, List, Any


def convert_posters(lines: List[List[str]]) -> List[Dict[str, str]]:
    fieldnames = lines[0]
    content = lines[1:]

    data: List[Dict[str, str]] = list()
    for row in content:
        # stop at blank rows
        if not "".join(row):
            break

        record: Dict[str, str] = dict()
        for key, value in zip(fieldnames, row):
            key = key.lower()
            # don't copy emails
            if "email" in key:
                continue
            # lot of dirty workarounds and fixes
            if key == "abstract number old":
                continue
            if "abstract no" in key:
                key = "abstract_number"
            if key == "abstract_number":
                value = value.lstrip("0")  # remove leading 0s
            record[key] = value

        data.append(record)

    return data


def convert_workshops(lines: List[List[str]]) -> List[Dict[str, Any]]:
    fieldnames = lines[0]
    content = lines[1:]

    data: List[Dict[str, str]] = list()
    for row in content:
        # stop at blank rows
        if not "".join(row):
            break
        record: Dict[str, str] = dict()
        for key, value in zip(fieldnames, row):
            key = key.lower().strip()
            record[key] = value

        data.append(record)

    return data


def read(fname: str) -> List[Dict[str, str]]:
    # Data saved from online spreadsheets start with a Byte order mark (BOM) entry
    # which can screw up the first column header content if not properly escaped.
    with open(fname, encoding="utf-8-sig") as csvfile:
        reader = csv.reader(csvfile, dialect="excel-tab")
        lines = list(reader)

    if "posters" in fname:
        return convert_posters(lines)
    if "workshops" in fname:
        return convert_workshops(lines)
    if "exhibition" in fname:
        return convert_workshops(lines)

    print("Couldn't determine data source type (posters or workshops)")
    print("Trying posters")
    return convert_posters(lines)


def main():
    parser = argparse.ArgumentParser(description="Convert tsv to json")
    parser.add_argument("tsvfile", help=".tsv file with column headers")
    args = parser.parse_args()

    tsvfile = args.tsvfile
    jsonfile = os.path.splitext(tsvfile)[0] + ".json"

    data = read(tsvfile)

    print(f"Saving to {jsonfile}")
    # Make sure tsv file data is saved as utf-8 again
    with open(jsonfile, "w", encoding="utf-8") as jfp:
        json.dump(data, jfp, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
