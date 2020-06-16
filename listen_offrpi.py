#!/usr/bin/env python
import RPi.GPIO as GPIO
import subprocess

led_sta=18
pinoff=22
starpi=27
GPIO.setmode(GPIO.BCM)
print("Listen for shutdown Rpi")
GPIO.setup(led_sta, GPIO.OUT)
GPIO.setup(starpi, GPIO.OUT)
GPIO.output(starpi, True)
GPIO.output(led_sta, False)
GPIO.setup(pinoff, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.wait_for_edge(pinoff, GPIO.FALLING)
print("SLEEP")
GPIO.output(starpi, False)
GPIO.output(led_sta, True)
subprocess.call(['shutdown', '-h', 'now'], shell=False)
