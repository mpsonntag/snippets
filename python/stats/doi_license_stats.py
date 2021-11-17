"""
Get statistics on used license names from published G-Node
datasets. Requires a local copy of the DOImetadata repository.
"""
import argparse
import os
import re


def license_names_from_files(dir_path: str):
    print(f"Handling directory {os.path.abspath(dir_path)}")
    pattern = "rightsuri"
    for filename in os.listdir(dir_path):
        if not filename.endswith(".xml"):
            continue
        print(f"Handling file {filename}")
        filepath = os.path.join(os.path.abspath(dir_path), filename)
        with open(filepath, encoding="utf-8") as curr_file:
            for line in curr_file:
                if re.search(pattern, line.lower()):
                    # quick and dirty
                    print(line.split(">")[1].split("<")[0].strip())


def main():
    """
    Handle commandline arguments, call analysis procedures and handle statistics results.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dir_path", help="Path to the DOImetadata directory")
    args = parser.parse_args()

    license_names_from_files(args.dir_path)


if __name__ == "__main__":
    main()
