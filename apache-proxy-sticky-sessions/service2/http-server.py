# maintenance page
# html server read parameters and path example
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class CustomRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # Access the captured path
        # print("Path:", path)

        # Access query parameters
        # query_params = parse_qs(parsed_url.query)
        # print("Query parameters:", query_params)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>Service #2</h1>')

if __name__ == '__main__':
    server_address = ('', 9092)
    httpd = HTTPServer(server_address, CustomRequestHandler)
    print('Server is running on http://localhost:9092')
    httpd.serve_forever()
