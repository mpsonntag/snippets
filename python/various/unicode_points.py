"""
test script to range through unicode code points
"""
import unicodedata as udat


def run():
    # unicode code points are provided as hexadecimal in the unicode consortium
    # code charts (Unicode version 15.0; www.unicode.org)

    # rough Ogham hexadecimal code point range
    hex_start = 0x1680
    hex_end = 0x1700
    print("Print Ogham alphabet from unicode code hex points")
    # hexadecimal range and print of code points
    for i in range(hex_start, hex_end):
        print(f"{hex(i)}: {chr(i)} ({udat.category(chr(i))})")


if __name__ == "__main__":
    run()
