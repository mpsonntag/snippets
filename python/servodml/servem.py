"""serveOdml

serverLocalOdml sets up a minimal webserver and serves
and renders local odml files.

Usage: serveOdml [-d DIRECTORY] [-p PORT]

Options:
    -d DIRECTORY    Directory from which files will be served
                    Default is the directory from which the server is started.
    -p PORT         Port the server will use.
                    Default is port 8000.
    -h --help       Show this screen.
    --version       Show version.
"""

import http.server as hs
import socketserver
import sys

from docopt import docopt


def run(directory=None, port=8000):
    handler = hs.SimpleHTTPRequestHandler
    # files with odML extensions should be interpreted as XML
    handler.extensions_map.update({'.odml': 'application/xml'})
    server_address = ('', port)

    with socketserver.TCPServer(server_address, handler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    parser = docopt(__doc__, argv=sys.argv[1:], version="0.1.0")

    server_port = int(parser['-p']) if parser['-p'] else 8000
    serve_directory = parser['-d'] if parser['-d'] else None

    run(serve_directory, server_port)
