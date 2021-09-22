"""
Extract infos from gogs docker json logfiles
"""
import argparse
import json

from typing import Dict, List


def order_print(data: Dict[str, int]):
    """
    Sorts the dictionary content by key and prints the resulting dictionary.
    :param data: Dict containing distinct addresses and their occurrence.
    """
    print()
    print("Individual views ...")
    for dat in sorted(data):
        print(f"{dat}\t{data[dat]}")


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
        if not curr[5] in counter_dict:
            counter_dict[curr[5]] = 1
        else:
            counter_dict[curr[5]] = counter_dict[curr[5]] + 1

    return counter_dict


def filter_print(data: List[Dict[str, str]], fil_str: str,
                 print_msg: str = "") -> Dict[str, int]:
    """
    Reduces a dictionary to items that contain the passed filter string, calls the
    parse_stats func with the resulting dict and prints the length of the results.
    :param data: list containing docker log dictionaries.
    :param fil_str: string that has to be found in the "log" entry string.
    :param print_msg: Prefix before printing the number of results.
    :return: Dict containing distinct addresses and their occurrence.
    """
    if not print_msg:
        print_msg = fil_str.split("/")[0]

    fil_dat = list(filter(lambda log_entry: fil_str in log_entry["log"], data))
    parse_dat = parse_stats(fil_dat)

    print(f"{print_msg}:{str(len(parse_dat)).rjust(25-len(print_msg))}")

    return parse_dat


def process_data(data: List[Dict[str, str]]):
    """
    Process docker log data into different categories of interest and produce
    and print corresponding statistics.
    :param data: list containing docker log dictionaries.
    """
    pdf_dat = list(filter(lambda log_entry: ".pdf" in log_entry["log"], data))

    # Filter for raw pdf access -> happens when the Poster landing page is opened
    # or when the poster is downloaded;
    # The download rate per poster could be approximated by subtracting src access from
    # raw access.
    raw_dat = filter_print(pdf_dat, "raw", "Raw PDF")
    # Filter for pdf view on the page
    src_dat = filter_print(pdf_dat, "src", "View PDF")

    pos_dat = filter_print(data, "Posters/wiki/Poster")
    inv_dat = filter_print(data, "InvitedTalks/wiki/Invited")
    con_dat = filter_print(data, "ContributedTalks/wiki/Contributed")
    wor_dat = filter_print(data, "Workshops/wiki/Workshop")
    exh_dat = filter_print(data, "Exhibition/wiki/Exhibition")

    order_print(raw_dat)
    order_print(src_dat)
    order_print(pos_dat)
    order_print(inv_dat)
    order_print(con_dat)
    order_print(wor_dat)
    order_print(exh_dat)


def reduce_raw_dict(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Initial data cleanup.  Filter all logs that deal with accessing a
    "BernsteinConference" page and that contain "Completed" to remove
    "Started" duplicates. Further remove "/plugins" to filter loading
    the PDF viewer load logs.
    :param data: list containing docker log dictionaries.
    :return: list containing docker log dictionaries.
    """
    fil_str = "BernsteinConference"
    fil_dat = list(filter(lambda log_entry: fil_str in log_entry["log"], data))
    fil_dat = list(filter(lambda log_entry: "Completed" in log_entry["log"], fil_dat))
    fil_dat = list(filter(lambda log_entry: "/plugins" not in log_entry["log"], fil_dat))

    return fil_dat


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

    # Reduce raw dictionary and remove interfering log entries
    fil_dat = reduce_raw_dict(data)
    # Process reduced data and print statistics
    process_data(fil_dat)


if __name__ == "__main__":
    main()
