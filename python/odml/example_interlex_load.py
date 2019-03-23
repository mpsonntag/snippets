"""odmlInterLex

odmlInterLex fetches all registered terms from scicrunch interlex
for a given search term

Usage: odmlilex SEARCHTYPE SEARCHTERM

Arguments:
    SEARCHTYPE      SciCrunch search type. Currently the following search options are supported:
                    1 ... Interlex term search (default)
                    2 ... Scigraph vocabulary term
                    3 ... Scigraph vocabulary search
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

try:
    from http import HTTPStatus as httplib
except ImportError:
    import httplib


SCICRUNCH_USERKEY = "ZRt6argPOzoqCwk8ULK5N7agk731VsZy"
SCICRUNCH_URI = "https://scicrunch.org/api/1"


def search_interlex(search_term):
    requ = "%s/ilx/search/term/%s?key=%s" % (SCICRUNCH_URI, search_term, SCICRUNCH_USERKEY)

    print("Running interlex query '%s'" % requ)

    resp = urllib2.urlopen(requ)

    if resp.getcode() != httplib.OK:
        print("Could not resolve query, exit with '%s/%s'" % (resp.msg, resp.getcode()))
        exit(-1)

    content = json.load(resp)

    print("Result: Hits:'%s', '%s'" % (len(content), content))

    data = None
    try:
        data = content["data"]
    except KeyError:
        print("Received invalid response '%s'" % content)
        exit(-1)

    if not data["id"]:
        print("Search returned no result")
        exit(0)

    print("InterlexID: '%s'" % data["ilx"])
    print("Label: '%s'" % data["label"])
    print("Type: '%s'" % data["type"])
    print("definition: '%s'" % data["definition"])
    print("Number of available ids: '%s'" % len(data["existing_ids"]))

    for res in data["existing_ids"]:
        print("Current item: '%s'" % res)


def search_vocabulary(search_term):
    requ = "%s/scigraph/vocabulary/search/%s?limit=1&searchSynonyms=true&key=%s" % (SCICRUNCH_URI, search_term, SCICRUNCH_USERKEY)

    print("Running interlex query '%s'" % requ)

    resp = urllib2.urlopen(requ)

    if resp.getcode() != httplib.OK:
        print("Could not resolve query, exit with '%s/%s'" % (resp.msg, resp.getcode()))
        exit(-1)

    content = json.load(resp)

    print("Result: Hits:'%s', '%s'" % (len(content), content))


def main(args=None):
    # Find more details at
    # https://github.com/SciCrunch/NIF-Ontology
    # https://scicrunch.org/browse/api-docs/index.html?url=https://scicrunch.org/swagger-docs/swagger.json

    parser = docopt(__doc__, argv=args, version="0.1.1")

    search_type = parser['SEARCHTYPE']
    search_term = parser['SEARCHTERM']

    if search_type == "1":
        search_interlex(search_term)

    elif search_type == "2":
        search_vocabulary(search_term)

    elif search_type == "3":
        pass
    else:
        print("WARNING: Unsupported search type, defaulting to InterLex search.")
        search_interlex(search_term)


if __name__ == "__main__":
    main(sys.argv[1:])
