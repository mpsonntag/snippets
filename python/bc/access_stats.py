"""
Extract infos from docker json logfiles
"""
import argparse
import json


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


if __name__ == "__main__":
    main()
