import json

fname = "/home/msonntag/Chaos/staging/posters2021/BC20data/abstracts.json"

with open(fname) as jfp:
    data = json.load(jfp)

for item in data:
    cit_list = ""
    for auth in item["authors"]:
        first_name = f" {auth['firstName'][0]}." if "firstName" in auth.keys() and len(auth["firstName"]) > 0 else ""
        mid_name = ""
        if "middleName" in auth.keys() and auth["middleName"] and len(auth["middleName"]) > 0:
            mid_name = f" {auth['middleName'][0]}."
        citation = f"{auth['lastName']}{first_name}{mid_name}"
        cit_list = f"{cit_list}, {citation}" if len(cit_list) > 0 else citation
