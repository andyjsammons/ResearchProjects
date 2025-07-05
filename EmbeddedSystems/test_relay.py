import RPi.GPIO as GPIO
print(GPIO.RPI_INFO)

import time

output_pin = 4  

GPIO.setmode(GPIO.BCM)
GPIO.setup(output_pin, GPIO.OUT)

try:
    while True:
        GPIO.output(output_pin, GPIO.HIGH) 
        time.sleep(1)                      
        GPIO.output(output_pin, GPIO.LOW)  
        time.sleep(1)                      

except KeyboardInterrupt:
    GPIO.cleanup()
print("Exiting")
