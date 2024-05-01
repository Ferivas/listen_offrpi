# -*- coding: utf-8 -*-
"""
Created on Wed May  1 14:57:59 2024

listen_offrpi.py
Permite apagar de manera segura el Raspberry presionando un pulsante conectado
entre un GPIO y el GND del Rpi(pinoff)
Si esta programa esta corriendo tambien se enciende un led conectado a un GPIO
del Rpi, (ledsta)
Es necesario mantener presionado el pulsante durante aproximadamente 6 segundos
para que se apague el Rpi (este valor se puede cambiar en el archivo de 
inicializacion json. Mientras se tiene presionado el pulsante, el ledsta
titila
El GPIO utilizado para conectar el pulsante, el GPIO utilizado para conectar un
led para señalización y su polarización se determinan con un archivo de texto 
en formato json que se puede editar si se utilizan pines diferentes. 
La polaridad se refiere a la forma en que se conecta el led a la salida del GPIO.
Si se conecta a través de una resistencia a GND se considera polaridad 0, 
mientras que si el led se conecta por medio de una resistencia a VCC se considera
que la polaridas es 1. 
Si no se encuentra el archivo de configuración (listen_offrpi.json) el programa
configura las variables de la siguiente manera

{"ledsta": 17, "pinoff": 3, "polaridad": 0, "offtime":6}

@author: Fernando
"""

from gpiozero import Button, LEDBoard
from signal import pause
import warnings, os

import json

FILECONFIG="shutdwnbypin.json"
print("Comprueba configuracion hw inicial")

confighw=False
try:
    with open(FILECONFIG, 'r') as fp:
        dataconfig = json.load(fp)
    confighw=True
except:
    print("Configuracion default")
    configdefault={'ledsta':17,
                   'pinoff':3,
                   'polaridad':0,
                   'offtime':6}
    with open(FILECONFIG, 'w') as fp:
        json.dump(configdefault, fp)


if not confighw:
    with open(FILECONFIG, 'r') as fp:
        dataconfig = json.load(fp)
    confighw=True
    
print(dataconfig) 


offGPIO = dataconfig.get('pinoff')
offtime = dataconfig.get('offtime')
polled=dataconfig.get('polaridad')

mintime = 1       # notice switch after mintime seconds
actledGPIO = dataconfig.get('ledsta')   # activity LED

def shutdown(b):
    # find how long the button has been held
    p = b.pressed_time
    # blink rate will increase the longer we hold
    # the button down. E.g., at 2 seconds, use 1/4 second rate.
    leds.blink(on_time=0.5/p, off_time=0.5/p)
    if p > offtime:
        if polled==0:
            leds.off()
        else:
            leds.on()
        os.system("sudo poweroff")

def when_pressed():
    # start blinking with 1/2 second rate
    leds.blink(on_time=0.5, off_time=0.5)

def when_released():
    # be sure to turn the LEDs off if we release early
    if polled==0:
        leds.on()
    else:
        leds.off()

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    leds = LEDBoard(actledGPIO)

if polled==0:
    leds.on()
else:
    leds.off()    
  
btn = Button(offGPIO, hold_time=mintime, hold_repeat=True)
btn.when_held = shutdown
btn.when_pressed = when_pressed
btn.when_released = when_released
pause()