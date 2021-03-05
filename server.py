from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import logging
import json

hostName = "localhost"
serverPort = 8080

class ColladaServer (BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers["Content-Length"]) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode("utf-8"))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode("utf-8"))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    webServer = HTTPServer((hostName, serverPort), ColladaServer)
    logging.info("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    logging.info("Server stopped.")
