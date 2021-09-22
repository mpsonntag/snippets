"""
Extract infos from docker json logfiles
"""
import argparse
import json


def main():
    """
    Parse command line arguments and run the URL checks with the data provided.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", help="Docker logs JSON file")
    args = parser.parse_args()

    json_file = args.json_file
    with open(json_file, "r", encoding="utf-8") as jfp:
        data_string = jfp.read().replace('}\n{', '},\n{')
        data = json.loads(f"[{data_string}]")

    print(len(data))


if __name__ == "__main__":
    main()
