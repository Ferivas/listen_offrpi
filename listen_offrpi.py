#!/usr/bin/env python
import RPi.GPIO as GPIO
import subprocess
import time

led_sta=18
pinoff=22
#starpi=27
GPIO.setmode(GPIO.BCM)
print("Listen for shutdown Rpi")
GPIO.setup(led_sta, GPIO.OUT)
#GPIO.setup(starpi, GPIO.OUT)
#GPIO.output(starpi, True)
GPIO.output(led_sta, False)
GPIO.setup(pinoff, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    GPIO.wait_for_edge(pinoff, GPIO.FALLING)
    print("Ver retardo")
    counter=0
    while GPIO.input(pinoff) == False:     
        counter += 1
        time.sleep(0.5)
        tmod=counter%2
        if tmod==0:
            GPIO.output(led_sta, False)
        else:
            GPIO.output(led_sta, True)
            
    if counter>6:
    #GPIO.output(starpi, False)
        GPIO.output(led_sta, True)
        subprocess.call(['shutdown', '-h', 'now'], shell=False)
    else:
        print("Retardo insuficiente")
        GPIO.output(led_sta, False)
