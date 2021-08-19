# Python 3 server example
import json
import random
import socket
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 9009

current_seats = {
        'Dummy Seat #1': "Dummy value",
        'Dummy Seat #2': "Dummy value"
}

def process_received_data(data):
        print(f"Recieved data!: {data}")
        if not data['client_id'] or not data['seat_occupied']:
                print("Data was invalid... ignoring")

        current_seats[data['client_id']] = data['seat_occupied']

class MyServer(BaseHTTPRequestHandler):
        def do_GET(self):
                if self.path == '/':
                        print("Returning index.html")

                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        with open('index.html', 'r') as webpage_file:
                                self.wfile.write(bytes(webpage_file.read(), "utf-8"))

                elif self.path == '/get_current_occupancy':
                        print("Returning current occupancy readings")

                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()

                        current_value = []

                        for key in current_seats:
                                current_value.append({
                                        'seatName': key,
                                        'current_occupied':current_seats[key]
                                })

                        print(f"Returning current readings: {json.dumps(current_value)}")
                        self.wfile.write(bytes(f'{json.dumps(current_value)}', 'utf-8'))
                else:
                        print(f"Invalid path: {self.path}")
                        self.send_response(400)
        def do_POST(self):
                print("Someone posted to me!")
                if self.path == '/upload_sensor_data':
                        print("Received post")

                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length)
                        received_data = json.loads(post_data)
                        process_received_data(received_data)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

if __name__ == "__main__":
        webServer = HTTPServer((hostName, serverPort), MyServer)

        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        print("Server started http://%s:%s" % (hostName, serverPort))
        print(f'Things are running on hostname={hostname}, local_ip={local_ip}')
        try:
                local_ip2=([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])[0]
                print(f"IP Address is: {local_ip2}")
        except:
                pass

        try:
                webServer.serve_forever()
        except KeyboardInterrupt:
                pass
        webServer.server_close()
        print("Server stopped.")
