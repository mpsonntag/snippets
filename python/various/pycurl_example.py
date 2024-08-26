"""
Explore the functionality of pycurl
"""
import argparse

import pycurl


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Provide URL to perform a GET request with")
    args = parser.parse_args()

    get_url = args.url
    if not get_url:
        print("Please provide a valid URL")
        return
    print(f"Handling URL {get_url}")


if __name__ == "__main__":
    main()
