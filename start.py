from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
from sentalizer.start import get_sentiment as analyze 


class HttpServerImpl(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(json.dumps({'version': '1.0.0', 'name': 'Sentiment analyzer server'}).encode(encoding='utf_8'))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        content_len = int(self.headers.get('Content-Length'))
        post_body = json.loads(self.rfile.read(content_len))
        language = 'en'
        if 'lang' in post_body:
            language = post_body['lang']
        
        if 'extended' not in post_body:
            result = analyze(post_body['text'], language, False)
        else:
            result = analyze(post_body['text'], language, post_body['extended'])

        self.wfile.write(json.dumps(result).encode(encoding='utf_8'))


def __run(server_class=HTTPServer, handler_class=HttpServerImpl, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting http server on {addr}:{port}")
    httpd.serve_forever()

def initilize():
    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="0.0.0.0",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    __run(addr=args.listen, port=args.port)

#python server.py -p 80 -l 0.0.0.0
if __name__ == "__main__":
    import argparse
    initilize()
