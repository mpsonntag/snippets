"""
Extract infos from docker json logfiles
"""
import argparse
import json

from typing import Dict, List


def parse_stats(logs: List[Dict[str, str]]) -> Dict[str, int]:
    """
    Parses the accessed URL from the docker log string, counts the
    distinct occurrences and returns the resulting dictionary.
    The log string is formatted as: "[logger] [date] [time] [request status]
    [request type] [address]".
    Dependent on "[request status]" the next items are for "Started": "for [IP address]"
    and for "Completed": "[http.StatusCode] [http.Status] in [request time]"
    :param logs: List of docker log dicts; its keys are "log", "stream", "time".
    :return: Dict containing distinct addresses and their occurrence.
    """
    counter_dict = {}
    for item in logs:
        curr = item["log"].split(" ")
        if not curr[5] in counter_dict.keys():
            counter_dict[curr[5]] = 1
        else:
            counter_dict[curr[5]] = counter_dict[curr[5]] + 1

    return counter_dict


def main():
    """
    Parse command line arguments and run the URL checks with the data provided.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", help="Docker logs JSON file")
    args = parser.parse_args()

    json_file = args.json_file
    with open(json_file, "r", encoding="utf-8") as jfp:
        data_string = jfp.read().replace('}\n{', '},\n{')
        data = json.loads(f"[{data_string}]")

    # Filter all logs that deal with accessing a BernsteinConference page
    fil_str = "BernsteinConference"
    fil_dat = list(filter(lambda log_entry: fil_str in log_entry["log"], data))

    # Filter all logs that contain "Completed" to remove "Started" duplicates
    fil_com_dat = list(filter(lambda log_entry: "Completed" in log_entry["log"], fil_dat))

    # Filter all categories
    curr = ".pdf"
    pdf_dat = list(filter(lambda log_entry: curr in log_entry["log"], fil_com_dat))
    # Filter loading the pdf view plugin entries
    curr = "/plugins"
    pdf_dat = list(filter(lambda log_entry: curr not in log_entry["log"], pdf_dat))
    # Filter for raw pdf access -> happens when the Poster landing page is opened
    # or when the poster is downloaded;
    # The download rate per poster could be approximated by subtracting src access from
    # raw access.
    pdf_raw_dat = list(filter(lambda log_entry: "raw" in log_entry["log"], pdf_dat))
    # Filter for pdf view on the page
    pdf_src_dat = list(filter(lambda log_entry: "src" in log_entry["log"], pdf_dat))
    curr = "BernsteinConference/Posters/wiki/Poster"
    pos_dat = list(filter(lambda log_entry: curr in log_entry["log"], fil_com_dat))
    curr = "BernsteinConference/InvitedTalks/wiki/Invited"
    inv_dat = list(filter(lambda log_entry: curr in log_entry["log"], fil_com_dat))
    curr = "BernsteinConference/ContributedTalks/wiki/Contributed"
    con_dat = list(filter(lambda log_entry: curr in log_entry["log"], fil_com_dat))
    curr = "BernsteinConference/Workshops/wiki/Workshop"
    wor_dat = list(filter(lambda log_entry: curr in log_entry["log"], fil_com_dat))
    curr = "BernsteinConference/Exhibition/wiki/Exhibition"
    exh_dat = list(filter(lambda log_entry: curr in log_entry["log"], fil_com_dat))

    print(f"Raw PDF: {len(parse_stats(pdf_raw_dat))}")
    print(f"View PDF: {len(parse_stats(pdf_src_dat))}")
    print(f"Poster: {len(parse_stats(pos_dat))}")
    print(f"Invited Talks: {len(parse_stats(inv_dat))}")
    print(f"Contributed Talks: {len(parse_stats(con_dat))}")
    print(f"Workshops: {len(parse_stats(wor_dat))}")
    print(f"Exhibition: {len(parse_stats(exh_dat))}")


if __name__ == "__main__":
    main()
