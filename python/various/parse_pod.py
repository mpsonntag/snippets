import argparse
import json

from os.path import splitext

import feedparser
import requests

from dateutil import parser as datparser


REQ_TIMEOUT=10


def check_feed_url(feed_url):
    # crude URL scheme check
    if ":" in feed_url and "//" in feed_url:
        return True
    return False


def check_feed_available(feed_url):
    req = requests.get(feed_url, timeout=REQ_TIMEOUT)
    if req.status_code != 200:
        print(f"Got status code {req.status_code} for URL {feed_url}")
        return False
    return True


def fetch_feed(feed_url):
    curr_feed = feedparser.parse(feed_url)
    print(f"\n{curr_feed.feed.title} -{curr_feed.version}- ({curr_feed.feed.link})")
    return curr_feed


def handle_feed_url(curr_feed):
    num_episodes = len(curr_feed.entries)
    curr_loop = len(curr_feed.entries)
    print("")
    for idx, en in enumerate(curr_feed.entries):
        stat_code = requests.get(en.link, timeout=REQ_TIMEOUT).status_code
        is_avail = "OK" if stat_code == 200 else f"NOT AVAILABLE {stat_code}"
        pub_date = f"{datparser.parse(en.published):%Y-%m-%d %H:%M}"
        print(f"{idx} {is_avail}: #{curr_loop}/{num_episodes} ({pub_date}): {en.title}: {en.link}")
        curr_loop = curr_loop - 1
    print("")


def check_link(curr_feed, entry_idx):
    list_len = len(curr_feed.entries)

    if entry_idx >= list_len:
        print(f"Provided index {entry_idx} larger than available list 0-{list_len-1}")
        return

    requested_entry = curr_feed.entries[entry_idx]

    audio_link_list = list(filter(lambda d: {"href", "rel"} <= d.keys() and
                                            d["rel"] == "enclosure", requested_entry.links))
    if len(audio_link_list) < 1:
        print(f"\nCould not find audio link in requested entry\n\t{requested_entry}")
        return

    if len(audio_link_list) > 1:
        print("WARNING: More than one enclosure references found. Using first one.")
    audio_link = audio_link_list[0].href
    stat_code = requests.get(audio_link, timeout=REQ_TIMEOUT).status_code
    if stat_code != 200:
        print(f"DL link not available: {stat_code}; {audio_link}")
        return

    _, use_ext = splitext(audio_link.split("?")[0])
    if not use_ext:
        use_ext = ".mp3"
        print((f"WARNING: Could not identify file extension from audio link; using MP3 as default "
               f"{audio_link}"))

    use_date = f"{datparser.parse(requested_entry.published):%Y%m%d}"
    use_title = requested_entry.title
    use_file_name = f"{use_date}_{use_title}{use_ext}"
    print(f"Using file name {use_file_name}")


def dump_feed_content(curr_feed):
    print(json.dumps(curr_feed, indent=2))


def dump_feed_entry(curr_feed, entry_idx):
    list_len = len(curr_feed.entries)

    if entry_idx >= list_len:
        print(f"Provided index {entry_idx} larger than available list 0-{list_len-1}")
        return

    blab = curr_feed.entries[entry_idx]
    print(json.dumps(blab, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Parse RSS feed XML")
    parser.add_argument("feed_url", help="RSS feed XML url")
    parser.add_argument("-r", "--raw", help="Dump feed content",
                        action=argparse.BooleanOptionalAction)
    parser.add_argument("-i", "--index", help="Item index", type=int)
    parser.add_argument("-s", "--single_index",
                        help="Item index to dump single entry", type=int)
    args = parser.parse_args()

    feed_url = args.feed_url
    if not check_feed_url(feed_url):
        print(f"Please verify feed URL '{feed_url}'")
        return

    if not check_feed_available(feed_url):
        print(f"Please verify feed URL '{feed_url}'")
        return

    curr_feed = fetch_feed(feed_url)
    handle_raw = args.raw
    if handle_raw:
        dump_feed_content(curr_feed)
        return

    handle_index = args.index
    if handle_index:
        check_link(curr_feed, handle_index)
        return

    handle_single_dump = args.single_index
    if handle_single_dump:
        dump_feed_entry(curr_feed, handle_single_dump)
        return

    handle_feed_url(curr_feed)


if __name__ == "__main__":
    main()
