import requests
import random 
from time import sleep
from uuid import getnode as get_mac

try:
    from gpiozero import InputDevice
    input_device=InputDevice(17)
    running_in_mock_mode = False
except:
    running_in_mock_mode = True
    pass

url = 'http://54.227.187.8/upload_sensor_data'
myobj = {'client_id': ''}

def seat_currently_occupied():
    if not running_in_mock_mode:
        input_value=input_device.value
    else:
        input_value=random.randint(0,1)
    return input_value == 1

mac = get_mac()
mac_str = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
print(f"mac address is {mac_str}")
myobj['client_id'] = f'Sensor: {mac_str}'

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
