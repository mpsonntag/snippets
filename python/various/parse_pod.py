import argparse
import feedparser
import json
import requests

from dateutil import parser as datparser


def handle_feed_url(feed_url):
    req = requests.get(feed_url)
    if req.status_code != 200:
        print(f"EXIT: Got status code {req.status_code} for URL {feed_url}")
        return

    curr_feed = feedparser.parse(feed_url)

    num_episodes = len(curr_feed.entries)
    curr_loop = len(curr_feed.entries)
    print("")
    for idx, en in enumerate(curr_feed.entries):
        stat_code = requests.get(en.link).status_code
        is_avail = f"OK" if stat_code == 200 else f"NOT AVAILABLE {stat_code}"
        pub_date = '{:%Y-%m-%d %H:%M}'.format(datparser.parse(en.published))
        print(f"{idx} {is_avail}: #{curr_loop}/{num_episodes} ({pub_date}): {en.title}: {en.link}")
        curr_loop = curr_loop - 1
    print("")


def check_link(feed_url, link_idx):
    req = requests.get(feed_url)
    if req.status_code != 200:
        print(f"EXIT: Got status code {req.status_code} for URL {feed_url}")
        return

    curr_feed = feedparser.parse(feed_url)
    list_len = len(curr_feed.entries)

    if link_idx >= list_len:
        print(f"Provided index {link_idx} larger than available list 0-{list_len-1}")
        return

    requested_entry = curr_feed.entries[link_idx]
    stat_code = requests.get(requested_entry.link).status_code
    if stat_code != 200:
        print(f"DL link not available: {stat_code}; {requested_entry.link}")
        return

    fn = requested_entry.title
    flink = requested_entry.link
    print(f"Using file name {fn}: {flink}")


def dump_feed_content(feed_url):
    req = requests.get(feed_url)
    if req.status_code != 200:
        print(f"EXIT: Got status code {req.status_code} for URL {feed_url}")
        return

    curr_feed = feedparser.parse(feed_url)
    print(json.dumps(curr_feed, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Parse RSS feed XML")
    parser.add_argument("feed_url", help="RSS feed XML url")
    parser.add_argument("-r", "--raw", help="Dump feed content",
                        action=argparse.BooleanOptionalAction)
    parser.add_argument("-i", "--index", help="Item index", type=int)
    args = parser.parse_args()

    feed_url = args.feed_url

    handle_raw = args.raw
    if handle_raw:
        dump_feed_content(feed_url)
        return

    handle_index = args.index
    if handle_index:
        check_link(feed_url, handle_index)
        return

    handle_feed_url(feed_url)


if __name__ == "__main__":
    main()
