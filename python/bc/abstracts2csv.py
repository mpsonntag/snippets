# Convert the abstract output of the gca-client script to a CSV or TSV file

import argparse
import json


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

    for curr_abstract in data:
        print(curr_abstract["abstrTypes"])
        for currkey in curr_abstract:
            print(currkey)


if __name__ == "__main__":
    main()
