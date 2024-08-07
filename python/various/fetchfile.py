"""
Fetch remote files using curl; provide URLs including file extensions via text file.
"""
import argparse
import subprocess
import time

from os.path import splitext


def fetch_files(infile):
    """
    Open provided input file and try to fetch the content for each
    entry via curl. The file extension is extracted from each URL.
    Files are serially numbered and the numbers are padded with zeroes to
    four digits.
    """
    offset = 0
    file_name_base = "11_"

    with open(infile, encoding="utf8") as openfile:
        while line := openfile.readline():
            line = line.strip()
            offset += 1
            if not (offset % 10) % 5:
                time.sleep(7)
            else:
                time.sleep(offset % 5)
            _, curr_ext = splitext(line)
            curr_file_name = f"{file_name_base}{offset:04}{curr_ext}"
            print(f"Fetching {curr_file_name}: {line}")
            subprocess.run(["curl", line, "-o", curr_file_name], check=False)


def main():
    """
    Handle commandline arguments and call main download routine
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url_file", help="File containing URLs")
    args = parser.parse_args()

    #infile = "linklist.md"
    infile = args.url_file
    fetch_files(infile)


if __name__ == "__main__":
    main()
