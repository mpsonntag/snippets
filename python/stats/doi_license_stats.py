"""
Get statistics on used license names from published G-Node
datasets. Requires a local copy of the DOImetadata repository.
"""
import argparse
import os
import re

from typing import Dict


def license_names_from_files(dir_path: str) -> Dict:
    """
    Parse license names from all xml files found at the provided
    directory path and return a dictionary containing the license
    names as keys and total occurrences as values.

    :param dir_path: directory containing DOI publication xml files

    :return: dictionary containing the license names as keys and total occurrences as values.
    """
    print(f"Handling directory {os.path.abspath(dir_path)}")
    lic_names = {}
    pattern = "rightsuri"
    for filename in os.listdir(dir_path):
        if not filename.endswith(".xml"):
            continue
        print(f"Handling file {filename}")
        filepath = os.path.join(os.path.abspath(dir_path), filename)
        with open(filepath, 'r', encoding="utf-8") as curr_file:
            for line in curr_file:
                if re.search(pattern, line.lower()):
                    # quick and dirty
                    curr_name = line.split(">")[1].split("<")[0].strip()
                    if curr_name not in lic_names:
                        lic_names[curr_name] = 0
                    lic_names[curr_name] = lic_names[curr_name] + 1
    return lic_names


def main():
    """
    Handle commandline arguments, call analysis procedures and handle statistics results.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dir_path", help="Path to the DOImetadata directory")
    args = parser.parse_args()

    lic_names = license_names_from_files(args.dir_path)
    print(lic_names)


if __name__ == "__main__":
    main()
