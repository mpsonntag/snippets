"""
Script to explore the functionality of pycurl
"""
import argparse

from io import BytesIO

import pycurl
import certifi


def curl_response_body(get_url):
    """
    Executes curl using the provided URL and prints the response
    body to the command line.
    """
    c = pycurl.Curl()
    c.setopt(c.URL, get_url)
    c.setopt(c.CAINFO, certifi.where())
    # c.setopt(c.VERBOSE, True)

    buffer = BytesIO()
    c.setopt(c.WRITEFUNCTION, buffer.write)

    c.perform()

    print(f"Connection response {c.getinfo(pycurl.HTTP_CODE)}")
    c.close()

    print(buffer.getvalue().decode("UTF-8").strip())


def main():
    """
    Handle commandline arguments and run the appropriate routines.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Provide URL to perform a GET request with")
    args = parser.parse_args()

    get_url = args.url
    if not get_url:
        print("Please provide a valid URL")
        return
    print(f"Handling URL {get_url}")
    curl_response_body(get_url)


if __name__ == "__main__":
    main()
