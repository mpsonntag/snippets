import json

from datetime import date
from typing import Dict, Any


def citation_info(item: Dict[str, Any]) -> (str, str):
    cit_list = ""
    for auth in item["authors"]:
        first_name = f" {auth['firstName'][0]}." if "firstName" in auth.keys() and len(auth["firstName"]) > 0 else ""
        mid_name = ""
        if "middleName" in auth.keys() and auth["middleName"] and len(auth["middleName"]) > 0:
            mid_name = f" {auth['middleName'][0]}."
        citation = f"{auth['lastName']}{first_name}{mid_name}"
        cit_list = f"{cit_list}, {citation}" if len(cit_list) > 0 else citation
    doi_item = ""
    if "doi" in item.keys() and item["doi"] and len(item["doi"]) > 0:
        doi_item = f' doi: <a href="https://doi.org/{item["doi"]}">{item["doi"]}</a>'

    return cit_list, doi_item


fname = "/home/msonntag/Chaos/staging/posters2021/BC20data/abstracts.json"

with open(fname) as jfp:
    data = json.load(jfp)

for item in data:
    cit_list, doi_item = citation_info(item)

    year = date.today().year
    copy_item = f"Copyright: © ({year}) {cit_list}" if cit_list else ""
    cit_item = f"Citation: {cit_list} ({year}) {item['title']}. " \
               f"Bernstein Conference {year}.{doi_item}"

    print(f"{copy_item}\n{cit_item}")
