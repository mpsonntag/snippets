"""
Script to explore the beautiful soup functionality
"""
import argparse


def main():
    """
    Handle commandline arguments and run the appropriate routines.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Provide URL of interest")
    args = parser.parse_args()

    get_url = args.url
    if not get_url:
        print("Please provide a valid URL")
        return
    print(f"Handling URL {get_url}")


if __name__ == "__main__":
    main()
