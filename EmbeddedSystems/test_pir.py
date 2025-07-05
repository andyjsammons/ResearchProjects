import RPi.GPIO as GPIO
print(GPIO.RPI_INFO)

import time

# Port of PIR
pir_port = 27

# Setup GPIO mode to Broadcom
GPIO.setmode(GPIO.BCM)

# configure the pin as input pin
GPIO.setup(pir_port,  GPIO.IN)

try:
    while (True):
        # if the input is zero, nobody is there at the sensor
        if GPIO.input(pir_port) == 0:
            print("No motion detected")
        else:
            print("Motion detected")

        time.sleep(0.5)
        
except KeyboardInterrupt:
    GPIO.cleanup()
print("Exiting")