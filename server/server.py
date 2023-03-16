import http.server
import socketserver

PORT = 8080


class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = 'srealityEstates.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


Handler = HttpRequestHandler

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print("Http Server Serving at port", PORT)
    httpd.serve_forever()
