#file httpd.py

import threading
import _thread
import sys
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server
import time
if sys.version_info >=  (2, 7):
    import json as json
else:
    import simplejson as json
import http.server
import socketserver


def chunk_generator_test():
    for i in range(10):
        time.sleep(.1)
        yield "this is chunk: %s\r\n"%i

class UKAudioStreamHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def do_HEAD(self):
        self.send_response(200)
    def do_GET(self):
        self.send_response(200)
        self.send_header('Transfer-Encoding', 'chunked')
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        def write_chunk(chunk):
            tosend = '%X\r\n%s\r\n'%(len(chunk), chunk)
            self.wfile.write(tosend)
        for chunk in chunk_generator_test():
            if not chunk:
                continue
            write_chunk(chunk)
        self.wfile.write('0\r\n\r\n')


class UKAudioStreamServer():
    def __init__(self, app):
        self.app = app

    def create(self, ip_addr, port):
        self.server = http.server.HTTPServer((ip_addr, port), UKAudioStreamHandler)

    def start(self):
        self._webserver_died = threading.Event()
        self._webserver__thread = threading.Thread(target=self._run_webserver__thread)
        self._webserver__thread.start()

    def _run_webserver__thread(self):
        self.server.serve_forever()
        self._webserver_died.set()

    def stop(self):
        if not self._webserver__thread:
            return

        _thread.start_new_thread(self.server.shutdown, () )

        # wait for _thread to die for a bit, then give up raising an exception.
        #if not self._webserver_died.wait(5):
            #raise ValueError("couldn't kill webserver")
        print ("Shutting down internal webserver")
