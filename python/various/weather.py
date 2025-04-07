"""
Fetch and process weather information.
"""

import argparse
import urllib.request as ureq


def fetch_url_content(url_str):
    """
    Fetch and return content from a URL as string
    """
    content = ""
    response = ureq.urlopen(url_str)
    code = response.getcode()
    if code == 200:
        print(f"Response status: {code}")
        content = response.read()
    else:
        print(f"Response status: {code}")

    return content


def main():
    """
    Handle commandline arguments and run main processing routines
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url_str", help="URL to fetch parsable information")

    args = parser.parse_args()
    url_str = args.url_str

    content = fetch_url_content(url_str)


if __name__ == "__main__":
    main()
