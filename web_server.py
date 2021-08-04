# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from datetime import datetime

hostName = "localhost"
serverPort = 9009

def get_current_time_string():
	now = datetime.now().time()	
	return f"The current time is: {now}"

class MyServer(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		with open('index.html', 'r') as webpage_file:
			self.wfile.write(bytes(webpage_file.read(), "utf-8"))

if __name__ == "__main__":
	webServer = HTTPServer((hostName, serverPort), MyServer)
	print("Server started http://%s:%s" % (hostName, serverPort))

	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass
	webServer.server_close()
	print("Server stopped.")
