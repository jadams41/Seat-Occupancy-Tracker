import RPi.GPIO as GPIO
import time

print("Doing some basic setup of our GPIO pins")
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)

print("Will be attempting to read pressure sensor continuously")
prev_input = 0
try:
    while True:
        # take a reading
        input = GPIO.input(4)
        print(f"input = {input}")
        if ((not prev_input) and input):
            print("Under pressure")
        #update previous input
        prev_input = input
        #slight pause
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping the program")
    pass
finally:
    GPIO.cleanup()
