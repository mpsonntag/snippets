"""
Facilitates download of content files via provided podcast feed URL.
"""
import argparse
import json

from os.path import splitext

import feedparser
import requests

from dateutil import parser as date_parser


REQ_TIMEOUT=10


def is_url(feed_url):
    """
    Crude check whether a provided string is formatted like a URL.
    :param feed_url: String providing a URL.
    """
    if ":" in feed_url and "//" in feed_url:
        return True
    return False


def is_url_available(feed_url):
    """
    Check whether a provided URL string is accessible and
    returns status code 200 (OK).
    :param feed_url: String providing a URL.
    """
    req = requests.get(feed_url, timeout=REQ_TIMEOUT)
    if req.status_code != 200:
        print(f"Got status code {req.status_code} for URL {feed_url}")
        return False
    return True


def fetch_feed(feed_url):
    """
    Fetch XML file from a provided feed URL and parse the resulting data
    into a feedparser dict.
    :param feed_url: String providing a URL.
    :return: A FeedParserDict.
    """
    curr_feed = feedparser.parse(feed_url)
    print(f"\n{curr_feed.feed.title} -{curr_feed.version}- ({curr_feed.feed.link})")
    return curr_feed


def handle_feed_url(curr_feed):
    """
    Print information about content files available via the provided
    FeedParserDict to the command line.
    Further checks whether the provided link to download the content file
    is available and returns the status code 200 (OK).
    :param curr_feed: A FeedParserDict.
    """
    num_episodes = len(curr_feed.entries)
    curr_loop = len(curr_feed.entries)
    print("")
    for idx, en in enumerate(curr_feed.entries):
        stat_code = requests.get(en.link, timeout=REQ_TIMEOUT).status_code
        is_avail = "OK" if stat_code == 200 else f"n/a {stat_code}"
        pub_date = f"{date_parser.parse(en.published):%Y-%m-%d %H:%M}"
        print(f"{idx} {is_avail}: #{curr_loop}/{num_episodes} ({pub_date}): {en.title}: {en.link}")
        curr_loop = curr_loop - 1
    print("")


def extract_content_url(curr_feed, entry_idx):
    """
    Extract and return a URL for a specific item in a provided FeedParserDict.
    :param curr_feed: A FeedParserDict.
    :param entry_idx: index of the requested item in the provided FeedParserDict.
    :return: String with the URL of interest.
    """
    list_len = len(curr_feed.entries)

    if entry_idx >= list_len:
        print(f"Provided index {entry_idx} larger than available list 0-{list_len-1}")
        return ""

    requested_entry = curr_feed.entries[entry_idx]

    audio_link_list = list(filter(lambda d: {"href", "rel"} <= d.keys() and
                                            d["rel"] == "enclosure", requested_entry.links))
    if len(audio_link_list) < 1:
        print(f"\nNo available audio file URL for requested entry\n\t{requested_entry}")
        return ""

    if len(audio_link_list) > 1:
        print("WARNING: More than one enclosure references found. Using first one.")
    audio_link = audio_link_list[0].href
    return audio_link


def handle_output_name(audio_link, requested_entry):
    """
    Parse construct and return an output filename from a provided URL
    and FeedParseDict item.
    :param audio_link: String containing the URL to an audio file.
    :param requested_entry: Single FeedParseDict item.
    :return: String containing a file name in the format [YYYYMMDD]_[title].[ext]
    """
    _, use_ext = splitext(audio_link.split("?")[0])
    if not use_ext:
        use_ext = ".mp3"
        print((f"WARNING: Could not identify file extension from audio file URL. "
               f"Using MP3 as fallback ({audio_link})"))

    use_date = f"{date_parser.parse(requested_entry.published):%Y%m%d}"
    use_title = requested_entry.title
    use_file_name = f"{use_date}_{use_title}{use_ext}"
    return use_file_name


def handle_item(curr_feed, entry_idx):
    """
    Check whether a file is available for a specific entry in a
    provided ParserFeedDict.
    :param curr_feed: A FeedParserDict.
    :param entry_idx: index of the requested item in the provided FeedParserDict.
    """
    audio_link = extract_content_url(curr_feed, entry_idx)
    if not audio_link or not is_url(audio_link):
        return
    stat_code = requests.get(audio_link, timeout=REQ_TIMEOUT).status_code
    if stat_code != 200:
        print(f"Audio file URL not available: {stat_code} ({audio_link})")
        return

    file_name = handle_output_name(audio_link, curr_feed.entries[entry_idx])
    print(f"Using file name {file_name}")


def dump_feed_content(curr_feed):
    """
    Dump the content of the provided FeedParserDict as json to the command line.
    :param curr_feed: A FeedParserDict.
    """
    print(json.dumps(curr_feed, indent=2))


def dump_feed_entry(curr_feed, entry_idx):
    """
    Dump the content of a specified entry in the provided FeedParserDict
    as json to the command line.
    :param curr_feed: A FeedParserDict.
    :param entry_idx: index of the requested item in the provided FeedParserDict.
    """
    list_len = len(curr_feed.entries)

    if entry_idx >= list_len:
        print(f"Provided index {entry_idx} larger than available list 0-{list_len-1}")
        return

    curr = curr_feed.entries[entry_idx]
    print(json.dumps(curr, indent=2))


def main():
    """
    Parse command line arguments and run the appropriate functions. Checks
    whether the mandatory feed address is a URL and is accessible.
    """
    parser = argparse.ArgumentParser(description="Parse RSS feed XML")
    parser.add_argument("feed_url", help="RSS feed XML url")
    parser.add_argument("-r", "--raw", help="Dump feed content",
                        action=argparse.BooleanOptionalAction)
    parser.add_argument("-i", "--index", help="Item index", type=int)
    parser.add_argument("-s", "--single_index",
                        help="Item index to dump single entry", type=int)
    args = parser.parse_args()

    feed_url = args.feed_url
    if not is_url(feed_url) or not is_url_available(feed_url):
        print(f"Please verify feed URL '{feed_url}'")
        return

    curr_feed = fetch_feed(feed_url)
    handle_raw = args.raw
    if handle_raw:
        dump_feed_content(curr_feed)
        return

    handle_index = args.index
    if handle_index:
        handle_item(curr_feed, handle_index)
        return

    handle_single_dump = args.single_index
    if handle_single_dump:
        dump_feed_entry(curr_feed, handle_single_dump)
        return

    handle_feed_url(curr_feed)


if __name__ == "__main__":
    main()
