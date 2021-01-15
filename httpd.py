#file httpd.py

import threading
import _thread
import sys
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server
if sys.version_info >=  (2, 7):
    import json as json
else:
    import simplejson as json


class TinyWebServer():
    def __init__(self, app):
        self.app = app

    def simple_app(self, environ, start_response):
        status = '200 OK'
        if environ['REQUEST_METHOD'] == 'POST':
            # request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            # request_body = environ['wsgi.input'].read(request_body_size)
            # d = parse_qs(request_body)  # turns the qs to a dict
            # return 'From POST: %s' % ''.join('%s: %s' % (k, v) for k, v in d.iteritems())
            return ["POSTHI"]
        else:  # GET
            # d = parse_qs(environ['QUERY_STRING'])  # turns the qs to a dict
            # #return 'From GET: %s' % ''.join('%s: %s' % (k, v) for k, v in d.iteritems())
            # try:
            #     track_id = str(d['track'])
            #     url = self.app.api.get_playable_url(track_id[2:-2])
            #     response = json.dumps([{"track": track_id, "url": url}], indent=4, separators=(',', ': '))
            #     return response
            response = json.dumps([{"track": "hi!"}])
            headers = [('Content-Type', 'application/json'), ('Content-Length', str(len(response)))]
            start_response(status, headers)
            return [bytes(response, 'utf-8')]


    def create(self, ip_addr, port):
        self.httpd = make_server(ip_addr, port, self.simple_app)

    def start(self):
        """
        start the web server on a new _thread
        """
        self._webserver_died = threading.Event()
        self._webserver__thread = threading.Thread(
                target=self._run_webserver__thread)
        self._webserver__thread.start()

    def _run_webserver__thread(self):
        self.httpd.serve_forever()
        self._webserver_died.set()

    def stop(self):
        if not self._webserver__thread:
            return

        _thread.start_new_thread(self.httpd.shutdown, () )
        #self.httpd.server_close()

        # wait for _thread to die for a bit, then give up raising an exception.
        #if not self._webserver_died.wait(5):
            #raise ValueError("couldn't kill webserver")
        print ("Shutting down internal webserver")
