# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from datetime import datetime
import RPi.GPIO as GPIO

hostName = "localhost"
serverPort = 9009

GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)

def get_current_time_string():
	now = datetime.now().time()
	return f"The current time is: {now}"

def get_current_pressure_reading():
	return f"Someone is currently sitting at the desk = {GPIO.input(4)}"

class MyServer(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		with open('index.html', 'r') as webpage_file:
			self.wfile.write(bytes(eval('f' +repr(webpage_file.read())), "utf-8"))
		self.wfile.write(bytes(get_current_pressure_reading(), 'utf-8'))

if __name__ == "__main__":
	webServer = HTTPServer((hostName, serverPort), MyServer)
	print("Server started http://%s:%s" % (hostName, serverPort))

	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass
	webServer.server_close()
	GPIO.cleanup()
	print("Server stopped.")
