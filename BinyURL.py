import requests
import http.server
from urllib.parse import parse_qs, unquote
import os

memory = {}

form = '''<!DOCTYPE html>
<title>Bookmark Server</title>
<form method="POST">
    <label>Long URI:
        <input name="longurl">
    </label>
    <br>
    <label>Short name:
        <input name="shorturl">
    </label>
    <br>
    <button type="submit">Save it!</button>
</form>
<p>URIs I know about:
<pre>
{}
</pre>
'''

def checkurl(url):
    try:
        if requests.get(str(url),timeout=2.0):
            return True
    except:
        return False

class Binyurl(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        name = unquote(self.path[1:])

        if name:
            if name in memory:
                self.send_response(303)
                self.send_header('Location', memory[name])
                self.end_headers()

            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain: charset=utf-8')
                self.end_headers()
                self.wfile.write('{0} is not in our shitty transient database'.format(name).encode())

        else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                known = "\n".join("{} : {}".format(key, memory[key])
                                  for key in sorted(memory.keys()))
                self.wfile.write(form.format(known).encode())

    def do_POST(self):
        length = int(self.headers.get('Content-length', 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)

        if "longurl" not in params or "shorturl" not in params:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain : charset=utf-8')
            self.end_headers()
            self.wfile.write('Missing form fields!'.encode())
            return

        longurl = params['longurl'][0]
        shorturl = params['shorturl'][0]

        if checkurl(longurl):
            memory[shorturl] = longurl
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain : charset=utf-8')
            self.end_headers()
            self.wfile.write("Invalid or nonexistent url! ({})".format(longurl).encode())

port = int(os.environ.get('PORT', 8000))
address = ('',port)
httpd = http.server.HTTPServer(address, Binyurl)
httpd.serve_forever()





