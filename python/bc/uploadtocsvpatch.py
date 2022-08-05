"""
Opens a CSV file, identifies the "id" column and uses it to create salted and hashed strings from
the corresponding values. A new column "upload_key" is added to the CSV data and a new
file is saved.
"""

import argparse
import pandas as pd


def main():
    """
    Handles the command line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", help="CSV file containing the abstract id data")
    parser.add_argument("code_salt", help="Salt string to create poster upload codes")
    parser.add_argument("-s", default="\t",
                        help="CSV file column separator; default is tab")
    args = parser.parse_args()

    csv_file = args.csv_file
    csv_sep = args.s
    csv_data = pd.read_csv(csv_file, header=0, sep=csv_sep)

    print(csv_data.loc[:, "id"])


if __name__ == "__main__":
    main()
