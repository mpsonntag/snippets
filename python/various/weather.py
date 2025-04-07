"""
Fetch and process weather information.
"""

import argparse
import urllib.request as ureq

from lxml import etree
from lxml.html import fromstring as import_string


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


def parse_page_content(content):
    """
    Extract information from HTML string content and return as functional HTML page string
    """
    search_string = '//div[@class="section-left"]'

    content_tree = import_string(content)
    result_node = content_tree.xpath(search_string)

    result_root = etree.Element("html")
    result_root.append(result_node[0])
    result = etree.tostring(result_root)

    return result


def save_content(file_name, content):
    """
    Save string content to specified file
    """
    with open(file_name, "w", encoding="UTF-8") as fn:
        fn.write(str(content.decode("utf-8")))


def main():
    """
    Handle commandline arguments and run main processing routines
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url_str", help="URL to fetch parsable information")
    parser.add_argument("-o", "--out_file",
                        help="Name and location of the output file")
    args = parser.parse_args()
    url_str = args.url_str

    content = fetch_url_content(url_str)
    if not content:
        print("Could not fetch content from URL")
        return

    result = parse_page_content(content)

    file_name = args.out_file
    if file_name:
        print(f"Saving file {file_name}")
        save_content(file_name, result)


if __name__ == "__main__":
    main()
