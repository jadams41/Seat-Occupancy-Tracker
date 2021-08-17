from gpiozero import InputDevice

input_device=InputDevice(17)

while True:
    input_value=input_device.value
    print(f'pin 17 reads: {}input_value}')
    sleep(1)
