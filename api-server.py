from http.server import BaseHTTPRequestHandler, HTTPServer
import base64

# Hardcoded username and password
USERNAME = 'srdja'
PASSWORD = 'test'


class BasicAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        auth_header = self.headers.get('Authorization')
        if auth_header is None or not auth_header.startswith('Basic '):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Login Required"')
            self.end_headers()
            self.wfile.write(b'Unauthorized')
            return

        auth_decoded = base64.b64decode(auth_header[len('Basic '):]).decode(
            'utf-8')
        username, password = auth_decoded.split(':', 1)

        if username == USERNAME and password == PASSWORD:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"message": "Authorized"}')
        else:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Login Required"')
            self.end_headers()
            self.wfile.write(b'Unauthorized')


def run(server_class=HTTPServer, handler_class=BasicAuthHandler, port=8888):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()

