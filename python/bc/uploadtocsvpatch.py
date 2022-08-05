"""
Opens a CSV file, identifies the "id" column and uses it to create salted and hashed strings from
the corresponding values. A new column "upload_key" is added to the CSV data and a new
file is saved.
"""

import argparse


def main():
    """
    Handles the command line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", help="Tab delimited CSV file containing the abstract id data")
    parser.add_argument("code_salt", help="Salt string to create poster upload codes")
    args = parser.parse_args()


if __name__ == "__main__":
    main()
