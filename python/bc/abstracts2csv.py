"""
Convert the GCA abstract json output of the GCA-client script to a TSV file
"""

import argparse
import hashlib as hl
import json


ABSTRACT_KEYS = ["abstrTypes", "acknowledgements", "affiliations", "authors", "conference",
                 "conflictOfInterest", "doi", "favUsers", "figures", "isTalk", "mtime",
                 "reasonForTalk", "references", "sortId", "state", "stateLog", "text",
                 "title", "topic", "uuid"]
ABSTR_TYPES_KEYS = ["name", "prefix", "short", "uuid"]
AUTHOR_KEYS = ["affiliations", "firstName", "lastName", "mail", "middleName", "position", "uuid"]
AFFILIATION_KEYS = ["address", "country", "department", "section", "position", "uuid"]
REFERENCES_KEYS = ["doi", "link", "text", "uuid"]


def format_authors(first, middle, last):
    aun = last
    if middle and middle != "":
        aun = f"{middle} {last}"
    if first and first != "":
        aun = f"{first} {aun}"
    return aun


def handle_authors(authors_json, item_separator):
    authors = ""
    emails = ""
    for curr_auth in authors_json:
        if authors != "":
            authors += f"{item_separator} "
        if emails != "":
            emails += f"{item_separator} "

        authors += format_authors(curr_auth['firstName'],
                                  curr_auth['middleName'],
                                  curr_auth['lastName'])
        emails += f"{curr_auth['mail']}"

    return authors, emails


def handle_abstract_types(abs_types, abs_uuid):
    use_abs_type = {"name": "", "prefix": "", "short": "", "uuid": ""}
    if len(abs_types) > 0:
        if len(abs_types) > 1:
            print(f"WARNING: more than one abstract type found for abstract {abs_uuid}; "
                  f"using the first")
        use_abs_type = abs_types[0]

    return use_abs_type


def string_cleanup(content):
    if content:
        content = content.replace("\t", "").replace("\n", "")
    return content


def reduce_data(data, item_separator, code_salt):
    redu_data = []
    for abstract in data:
        authors, mails = handle_authors(abstract["authors"], item_separator)

        text = string_cleanup(abstract["text"])
        ack = string_cleanup(abstract["acknowledgements"])

        abs_type = handle_abstract_types(abstract["abstrTypes"], abstract["uuid"])

        upload_key = create_upload_key(abstract["uuid"], code_salt)

        redu_data.append({"sortId": abstract["sortId"],
                          "authors": authors,
                          "mail": mails,
                          "title": abstract["title"],
                          "topic": abstract["topic"],
                          "state": abstract["state"],
                          "uuid": abstract["uuid"],
                          "upload_key": upload_key,
                          "abstract_type": abs_type["name"],
                          "prefix": abs_type["prefix"],
                          "short": abs_type["short"],
                          "isTalk": abstract["isTalk"],
                          "reasonForTalk": abstract["reasonForTalk"],
                          "acknowledgements": ack,
                          "text": text})
    return redu_data


def convert(json_data, csv_separator, use_columns):
    tsv = ""
    for abstract in json_data:
        if not use_columns:
            # export all columns
            for _, abs_val in abstract.items():
                tsv += f"{abs_val}{csv_separator}"
        else:
            # export only specified columns
            for abs_key in use_columns:
                if abs_key not in abstract:
                    print(f"WARNING: could not find key {abs_key} in abstract")
                else:
                    tsv += f"{abstract[abs_key]}{csv_separator}"
        tsv += "\n"

    return tsv


def create_upload_key(uuid, salt):
    key = hl.pbkdf2_hmac("sha1", uuid.encode(), salt.encode(), 100000)
    return key.hex()[:10]


def main():
    """
    Parse an abstract service json file and print the information to a CSV file.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", help="JSON file containing abstracts data")
    parser.add_argument("code_salt", help="Salt string to create poster upload codes")
    parser.add_argument("out_file", help="Output CSV file")
    args = parser.parse_args()

    item_reduce_separator = ","
    csv_separator = "\t"
    code_salt = args.code_salt

    in_file = args.json_file
    with open(in_file, encoding="utf-8") as jfp:
        data = json.load(jfp)

    print("Parsing data ...")
    reduced = reduce_data(data, item_reduce_separator, code_salt)
    print("Converting to CSV data ...")
    csv_data = convert(reduced, csv_separator, [])

    out_file = args.out_file
    if not out_file:
        print("Using default output file ...")
        out_file = "out.csv"
    print(f"Saving CSV file {out_file}")
    with open(out_file, "w", encoding="utf-8") as tfp:
        tfp.write(csv_data)


if __name__ == "__main__":
    main()
