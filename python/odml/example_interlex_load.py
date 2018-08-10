"""odmlInterLex

odmlInterLex fetches all registered terms from scicrunch interlex
for a given search term

Usage: odmlilex SEARCHTERM

Arguments:
    SEARCHTERM       Term to get InterLex search terms.

Options:
    -h --help       show this screen.
    --version       show version.
"""

import sys

from docopt import docopt
from urllib import request


def main(args=None):

    print("bla")

    parser = docopt(__doc__, argv=args, version="0.1.0")

    searchterm = parser['SEARCHTERM']
    usrkey = "ZRt6argPOzoqCwk8ULK5N7agk731VsZy"

    requ = "https://scicrunch.org/api/1/ilx/search/term/%s?key=%s" % (searchterm, usrkey)

    print("Running '%s'" % requ)

    resp = request.urlopen(requ)

    print("Status response: '%s'; length: %s" % (resp.msg, resp.status))

    content = resp.read()

    print("Content:\n%s\n" % content)


if __name__ == "__main__":
    main(sys.argv[1:])
