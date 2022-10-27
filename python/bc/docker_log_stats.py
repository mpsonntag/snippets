"""
Extract infos from gogs docker json logfiles
"""
import argparse
import json

from typing import Dict, List


def ordered_print(data: Dict[str, int], trim_string: str = ""):
    """
    Sorts the dictionary content by key and prints the resulting dictionary.
    :param data: Dict containing distinct addresses and their occurrence.
    :param trim_string: String to remove from the first column string.
    """
    if not data:
        return
    print()
    print("Individual views ...")
    new_dat = dict(sorted(data.items(), key=lambda ipa: ipa[1]))
    for dat in new_dat:
        print(f"{dat.replace(trim_string, '')}\t{new_dat[dat]}")


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
    # dictionary with web addresses as key and number of occurrence as value
    counter_dict = {}
    for item in logs:
        # extract web address from log string
        curr = item["log"].split(" ")[5]
        if curr not in counter_dict:
            counter_dict[curr] = 1
        else:
            counter_dict[curr] = counter_dict[curr] + 1

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

    total_views = 0
    for _, address_views in parse_dat.items():
        total_views = total_views + address_views

    print(f"{print_msg}:{str(total_views).rjust(25-len(print_msg))} ({str(len(parse_dat))} distinct pages)")

    return parse_dat


def process_day_data(data: List[Dict[str, str]], details: bool = False):
    curr_list = []
    # account for the first run
    prev_date = data[0]["time"].split("T")[0]
    for val in data:
        curr_date = val["time"].split("T")[0]
        if curr_date != prev_date:
            print(f"\n---- Access on date {prev_date}")
            process_data(curr_list, details)

            curr_list = []
            prev_date = curr_date
        curr_list.append(val)


def process_data(data: List[Dict[str, str]], details: bool = False):
    """
    Process docker log data into different categories of interest and produce
    and print corresponding statistics.
    :param data: list containing docker log dictionaries.
    :param details: boolean value to switch whether to print details or not.
    Default is False.
    """
    pdf_dat = list(filter(lambda log_entry: ".pdf" in log_entry["log"], data))

    # Filter for raw pdf access -> happens when the Poster landing page is opened
    # or when the poster is downloaded;
    # The download rate per poster could be approximated by subtracting src access from
    print("-- Total page views and distinct pages accessed")
    # Filter for pdf view on the page
    src_dat = filter_print(pdf_dat, "src", "PDF via web view")
    # raw access.
    raw_dat = filter_print(pdf_dat, "raw", "PDF raw repo access")

    pos_dat = filter_print(data, "Posters/wiki/Poster")
    inv_dat = filter_print(data, "InvitedTalks/wiki/Invited")
    con_dat = filter_print(data, "ContributedTalks/wiki/Contributed")
    wor_dat = filter_print(data, "Workshops/wiki/Workshop")
    exh_dat = filter_print(data, "Exhibition/wiki/Exhibition")
    inf_dat = filter_print(data, "ConferenceInformation/wiki")

    if details:
        ordered_print(raw_dat, "/BernsteinConference/Posters/raw/master/")
        ordered_print(src_dat, "/BernsteinConference/Posters/src/master/")
        ordered_print(pos_dat, "/BernsteinConference/Posters/wiki/")
        ordered_print(inv_dat, "/BernsteinConference/InvitedTalks/wiki/")
        ordered_print(con_dat, "/BernsteinConference/ContributedTalks/wiki/")
        ordered_print(wor_dat, "/BernsteinConference/Workshops/wiki/")
        ordered_print(exh_dat, "/BernsteinConference/Exhibition/wiki/")
        ordered_print(inf_dat, "/BernsteinConference/ConferenceInformation/wiki/")


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


def print_ip_data(data: List[Dict[str, str]]):
    """
    Count all IP related actions and print results
    :param data: list containing docker log dictionaries.
    """
    # filter IP related data
    ip_data = list(filter(lambda log_entry: " for " in log_entry["log"], data))

    # strip spammy data
    curr = "GET /img"
    ip_data = list(filter(lambda log_entry: curr not in log_entry["log"], ip_data))
    curr = "GET /assets"
    ip_data = list(filter(lambda log_entry: curr not in log_entry["log"], ip_data))
    curr = "GET /js"
    ip_data = list(filter(lambda log_entry: curr not in log_entry["log"], ip_data))
    curr = "/user/login"
    ip_data = list(filter(lambda log_entry: curr not in log_entry["log"], ip_data))
    curr = "/BernsteinConference/Main/raw/master/img"
    ip_data = list(filter(lambda log_entry: curr not in log_entry["log"], ip_data))
    curr = "/BernsteinConference/posters/raw/master/banners"
    ip_data = list(filter(lambda log_entry: curr not in log_entry["log"], ip_data))

    counter_dict = {}
    for item in ip_data:
        curr = item["log"].split(" ")[7].strip()
        if curr not in counter_dict:
            counter_dict[curr] = 1
        else:
            counter_dict[curr] = counter_dict[curr] + 1

    print()
    print(f"IP access; {len(counter_dict)} total IP addresses ...")
    ordered_print(counter_dict)


def main():
    """
    Parse command line arguments and run the URL checks with the data provided.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--details", dest="details", action="store_true",
                        help="Print details for all categories")
    parser.add_argument("--ip", dest="handle_ip", action="store_true",
                        help="Print IP address statistics")
    parser.add_argument("--day", dest="handle_dates", action="store_true",
                        help="Split statistics on a day to day basis")
    parser.add_argument("json_file", help="Docker logs JSON file")
    args = parser.parse_args()

    details = args.details
    handle_ip = args.handle_ip
    handle_dates = args.handle_dates

    json_file = args.json_file
    with open(json_file, "r", encoding="utf-8") as jfp:
        data_string = jfp.read().replace('}\n{', '},\n{')
        data = json.loads(f"[{data_string}]")

    # Reduce raw dictionary and remove interfering log entries
    fil_dat = reduce_raw_dict(data)

    if handle_dates:
        process_day_data(fil_dat, details)
        return

    # Process reduced data and print statistics
    process_data(fil_dat, details)

    if handle_ip:
        print_ip_data(data)


if __name__ == "__main__":
    main()
