"""
Fetch remote files using curl; provide URLs including file extensions via text file.
"""
import argparse
import subprocess
import time

from os.path import splitext


def read_file_content(infile):
    """
    Opens provided input file and returns the content as
    a list of line entries with leading and trailing
    whitespaces removed.
    """
    content = []
    with open(infile, encoding="utf8") as openfile:
        while line := openfile.readline():
            content.append(line.strip())
    return content


def fetch_files(content, offset=0, file_name_base="", zero_padding=4):
    """
    Try to fetch the content file for each entry from a provided list using curl.
    The file extension is extracted from each URL.
    Files are serially numbered and the numbers are padded with zeroes to
    a provided number of digits (default is four).
    """
    for line in content:
        line = line.strip()
        offset += 1
        if not (offset % 10) % 5:
            time.sleep(7)
        else:
            time.sleep(offset % 5)

        _, curr_ext = splitext(line)
        pad_offset = str(offset).zfill(zero_padding)
        curr_file_name = f"{file_name_base}{pad_offset}{curr_ext}"

        print(f"Fetching '{curr_file_name}' from {line}")
        subprocess.run(["curl", line, "-o", curr_file_name], check=False,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    """
    Handle commandline arguments and call main download routine
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url_file", help="File containing URLs")
    parser.add_argument("-o", "--offset",
                        help="Offset of output file numbers (int)", type=int)
    parser.add_argument("-n", "--name_base",
                        help="Prepended base for all output file names")
    args = parser.parse_args()

    infile = args.url_file
    content = read_file_content(infile)
    if not content:
        print(f"Empty file {infile}")
        return

    offset = args.offset if args.offset else 0
    file_name_base = args.name_base if args.name_base else ""
    fetch_files(content, offset, file_name_base)


if __name__ == "__main__":
    main()
