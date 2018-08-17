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

import json
import sys

from docopt import docopt

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


def main(args=None):

    parser = docopt(__doc__, argv=args, version="0.1.0")

    searchterm = parser['SEARCHTERM']
    usrkey = "ZRt6argPOzoqCwk8ULK5N7agk731VsZy"
    requ = "https://scicrunch.org/api/1/ilx/search/term/%s?key=%s" % (searchterm, usrkey)

    print("Running interlex query '%s'" % requ)

    resp = urllib2.urlopen(requ)

    print("Status response: '%s'; length: %s" % (resp.msg, resp.getcode()))

    content = json.load(resp)

    print("Result:\n%s\n" % content)


if __name__ == "__main__":
    main(sys.argv[1:])
