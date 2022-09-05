"""
Opens a CSV file, identifies the "id" column containing GCA abstract server UUIDs and
uses it to create salted and hashed strings from the corresponding values.
A new column "upload_key" is added to the CSV data and a new file is saved.
"""

import argparse
import hashlib as hl
import os
import pandas as pd


def create_upload_key(uuid, salt):
    key = hl.pbkdf2_hmac("sha1", uuid.encode(), salt.encode(), 100000)
    return key.hex()[:10]


def load_salt(saltfile):
    with open(saltfile) as sfp:
        line = sfp.readline()

    return line.strip()


def main():
    """
    Handles the command line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    salthelp = ("File with salt string. Only first line will be used and it "
                "will be stripped of leading and trailing whitespace "
                "characters.")
    parser.add_argument("csv_file", help="CSV file containing the GCA abstract server UUIDs")
    parser.add_argument("code_salt", help=salthelp)
    parser.add_argument("-s", default="\t",
                        help="CSV file column separator; default is tab")
    args = parser.parse_args()

    csv_file = args.csv_file
    code_salt = args.code_salt
    csv_sep = args.s
    csv_data = pd.read_csv(csv_file, header=0, sep=csv_sep, encoding="UTF-8")

    new_col = []
    for curr in csv_data.loc[:, "id"]:
        if pd.notna(curr):
            new_key = create_upload_key(curr, load_salt(code_salt))
            new_col.append(new_key)
        else:
            new_col.append(curr)

    id_index = csv_data.columns.get_loc("id")
    csv_data.insert(id_index + 1, "upload_keys", new_col)

    out_name = os.path.splitext(os.path.basename(csv_file))[0]
    out_file_name = f"{out_name}_key.csv"
    csv_data.to_csv(out_file_name, index=False, sep=csv_sep, encoding="UTF-8")

    print("\nWARNING: still using 'upload_keys' as csv column name\n")


if __name__ == "__main__":
    main()
