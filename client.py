import requests
import random 
from time import sleep
from uuid import getnode as get_mac
from gpiozero import InputDevice

input_device=InputDevice(17)

url = 'http://54.227.187.8/upload_sensor_data'
myobj = {'client_id': random.randint(0,10000)}

def seat_currently_occupied():
    input_value=input_device.value
    return input_value == 1

mac = get_mac()
print(f"mac address is {mac}")
myobj['client_id'] = mac

while True:
    myobj['seat_occupied'] = seat_currently_occupied()
    try:
        x = requests.post(url, json = myobj)
        print("Upload worked!")
        print(x.text)
    except:
        print("Failed to upload... will try again soon")
        pass
    sleep(1)
