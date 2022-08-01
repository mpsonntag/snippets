"""
Convert the GCA abstract json output of the GCA-client script to a TSV file
"""

import argparse
import json


ABSTRACT_KEYS = ["abstrTypes", "acknowledgements", "affiliations", "authors", "conference",
                 "conflictOfInterest", "doi", "favUsers", "figures", "isTalk", "mtime",
                 "reasonForTalk", "references", "sortId", "state", "stateLog", "text",
                 "title", "topic", "uuid"]

# {'name': 'Contributed Talks', 'prefix': 2, 'short': 'C', 'uuid': '17eacc42-97e9-460f-b466-11c34ac2c02a'}
ABSTR_TYPES = ["name", "prefix", "short", "uuid"]


"""
abstrTypes: [{'name': 'Contributed Talks', 'prefix': 2, 'short': 'C', 'uuid': '17eacc42-97e9-460f-b466-11c34ac2c02a'}]
acknowledgements: None
affiliations: [{'address': 'Paris', 'country': 'France', 'department': "Department l'audition", 'position': 0, 'section': 'Institut Pateur', 'uuid': 'ad476166-1f35-4d5a-ab6a-4e21b44a2566'}]
authors: [{'affiliations': [0], 'firstName': 'Simone', 'lastName': 'Azeglio', 'mail': 'simone.azeglio@gmail.com', 'middleName': None, 'position': 0, 'uuid': '990e9cd9-c171-4f1f-8f4e-0e110bc1e6af'}]
conference: https://abstracts.g-node.org/api/conferences/bd602155-c3e0-439f-ac34-de8b49554a98
conflictOfInterest: None
doi: None
favUsers: https://abstracts.g-node.org/api/abstracts/fb3b7276-cb3f-40b4-a2fb-10e41ff11d2b/favusers
figures: []
isTalk: False
mtime: 2022-07-29T14:01:56.212Z
reasonForTalk: None
references: []
sortId: 0
state: Submitted
stateLog: https://abstracts.g-node.org/api/abstracts/fb3b7276-cb3f-40b4-a2fb-10e41ff11d2b/stateLog
text: lorem ipsum
title: Brains for Brains Award talk
topic: Other
uuid: fb3b7276-cb3f-40b4-a2fb-10e41ff11d2b
"""


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

    blab = data[0]
    for currkey in ABSTRACT_KEYS:
        print("%s: %s" % (currkey, blab[currkey]))

    """
    for curr_abstract in data:
        print(curr_abstract["abstrTypes"])
        for currkey in curr_abstract:
            print(currkey)
    """


if __name__ == "__main__":
    main()
