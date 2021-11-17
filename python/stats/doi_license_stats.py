"""
Get statistics on used license names from published G-Node
datasets. Requires a local copy of the DOImetadata repository.
"""
import argparse


def license_names_from_files(dir_path: str):
    print(dir_path)


def main():
    """
    Handle commandline arguments, call analysis procedures and handle statistics results.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dir_path", help="Path to the DOImetadata directory")
    args = parser.parse_args()

    license_names_from_files(args.dir_path)


if __name__ == "__main__":
    main()
