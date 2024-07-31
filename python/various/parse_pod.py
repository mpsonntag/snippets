import argparse
import feedparser
import requests


def handle_feed_url(feed_url):
    req = requests.get(feed_url)
    if req.status_code != 200:
        print(f"EXIT: Got status code {req.status_code} for URL {feed_url}")
        return

    curr_feed = feedparser.parse(feed_url)

    num_episodes = len(curr_feed.entries)
    curr_loop = len(curr_feed.entries)
    print("")
    for en in curr_feed.entries:
        print(f"#{curr_loop}/{num_episodes}: {en.title}: {en.link}")
        curr_loop = curr_loop - 1
    print("")


def main():
    parser = argparse.ArgumentParser(description="Parse RSS feed XML")
    parser.add_argument("feed_url", help="RSS feed XML url")
    args = parser.parse_args()

    feed_url = args.feed_url
    handle_feed_url(feed_url)


if __name__ == "__main__":
    main()
