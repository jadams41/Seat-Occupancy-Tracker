# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from datetime import datetime
import json
import random
import RPi.GPIO as GPIO

hostName = "localhost"
serverPort = 9009

GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN)

def get_current_time_string():
        now = datetime.now().time()
        return f"The current time is: {now}"

def seat_currently_occupied():
        current_value = GPIO.input(26)
        print(f"XXXX Current value is {current_value} XXXX")
        return current_value == 0
        # return random.randint(0,1) == 0

class MyServer(BaseHTTPRequestHandler):
        def do_GET(self):
                if self.path == '/':
                        print("Returning index.html")

                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        with open('index.html', 'r') as webpage_file:
                                self.wfile.write(bytes(webpage_file.read(), "utf-8"))
                                # self.wfile.write(bytes(get_current_pressure_reading(), 'utf-8'))

                elif self.path == '/get_current_occupancy':
                        print("Returning current occupancy readings")

                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()

                        current_value = [
                                {
                                        "seatName": "Seat #1",
                                        "current_occupied": seat_currently_occupied()
                                },
                                {
                                        "seatName": "Seat #2",
                                        # "current_occupied": True
                                },
                                {
                                        "seatName": "Seat #3",
                                        # "current_occupied": True
                                },
                                {
                                        "seatName": "Seat #4", # "current_occupied": True
                                }
                        ]
                        print(f"Returning current readings: {json.dumps(current_value)}")
                        self.wfile.write(bytes(f'{json.dumps(current_value)}', 'utf-8'))
                else:
                        print(f"Invalid path: {self.path}")
                        self.send_response(400)
        def do_POST(self):
                print("Someone posted to me!")
                if self.path == '/upload_sensor_data':
                        print("Received post")
                        print(self.data)

                print(self)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()


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
