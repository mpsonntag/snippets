"""
Script to explore the functionality of pycurl
"""
import argparse

from io import BytesIO

import pycurl
import certifi


class CurlHandler:
    """Context Manager object to properly open and close a curl object"""
    def __init__(self, handle_url, use_https=True, verbose=False):
        print("Running init")
        self.curl = pycurl.Curl()
        self.curl.setopt(self.curl.URL, handle_url)
        if use_https:
            self.curl.setopt(self.curl.CAINFO, certifi.where())
        if verbose:
            self.curl.setopt(self.curl.VERBOSE, True)

    def __enter__(self):
        print("Running enter")
        return self.curl

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Running exit")
        self.curl.close()


def shrink_newline(text):
    """
    All multiple consecutive '\n' in a provided text are reduced
    to a single newline.
    :param text: String containing the text of interest.
    :return: String containing the provided text with all consecutive
    '\n' characters reduced to a single newline occurrence.
    """
    san, prev = "", ""
    for rune in text:
        if rune != "\n":
            san += rune
        elif rune == "\n" and rune != prev:
            san += rune
        prev = rune
    return san


def curl_response_body(get_url):
    """
    Executes curl using the provided URL and prints the response
    body to the command line.
    """
    with CurlHandler(get_url) as c:
        buffer = BytesIO()
        c.setopt(c.WRITEFUNCTION, buffer.write)

        c.perform()
        print(f"Connection response {c.getinfo(pycurl.HTTP_CODE)}")

    body = buffer.getvalue().decode("UTF-8").strip()
    body = shrink_newline(body)
    print(body)


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
