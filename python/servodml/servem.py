"""serveOdml

serverLocalOdml sets up a minimal webserver and serves
and renders local odml files.

Usage: serveOdml [-d DIRECTORY] [-p PORT]

Options:
    -p PORT         Port the server will use.
                    Default is port 8000.
    -h --help       Show this screen.
    --version       Show version.
"""

import http.server as hs
import socketserver
import sys

from docopt import docopt

PORT = 8000


def run(port=PORT):
    handler = hs.SimpleHTTPRequestHandler
    # files with odML extensions should be interpreted as XML
    handler.extensions_map.update({'.odml': 'application/xml'})

    server_address = ('', port)

    with socketserver.TCPServer(server_address, handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Received Keyboard interrupt, shutting down")
            httpd.server_close()


def parse_args(args):
    parser = docopt(__doc__, argv=args, version="0.1.0")
    server_port = int(parser['-p']) if parser['-p'] else PORT
    run(server_port)


if __name__ == "__main__":
    if sys.argv[1:]:
        parse_args(sys.argv[1:])
    else:
        run()
