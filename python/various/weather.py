"""
Fetch and process weather information.
"""

import argparse


def main():
    """
    Handle commandline arguments and run main processing routines
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url_str", help="URL to fetch parsable information")

    args = parser.parse_args()
    url_str = args.url_str
    print(url_str)


if __name__ == "__main__":
    main()
