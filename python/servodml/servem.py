import http.server as hs
import socketserver


def run(directory=None, port=8000):
    handler = hs.SimpleHTTPRequestHandler
    server_address = ('', port)

    with socketserver.TCPServer(server_address, handler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    run()
