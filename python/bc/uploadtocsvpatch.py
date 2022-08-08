"""
Opens a CSV file, identifies the "id" column and uses it to create salted and hashed strings from
the corresponding values. A new column "upload_key" is added to the CSV data and a new
file is saved.
"""

import argparse
import hashlib as hl
import pandas as pd


def create_upload_key(uuid, salt):
    key = hl.pbkdf2_hmac("sha1", uuid.encode(), salt.encode(), 100000)
    return key.hex()[:10]


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
    code_salt = args.code_salt
    csv_sep = args.s
    csv_data = pd.read_csv(csv_file, header=0, sep=csv_sep)

    new_col = []
    for curr in csv_data.loc[:, "id"]:
        if pd.notna(curr):
            new_key = create_upload_key(curr, code_salt)
            new_col.append(new_key)
        else:
            new_col.append(curr)

    id_index = csv_data.columns.get_loc("id")
    csv_data.insert(id_index+1, "upload_keys", new_col)

    out_file_name = "%s_out.csv" % csv_file
    csv_data.to_csv(out_file_name, index=False, sep=csv_sep)

    print("\nWARNING: still using 'upload_keys' as csv column name")


if __name__ == "__main__":
    main()
