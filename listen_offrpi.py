'''
listen_offrpi.py
Permite apagar de manera segura el Raspberry presionando un pulsante conectado
entre un GPIO y el GND del Rpi(pinoff)
Si esta programa esta corriendo tambien se enciende un led conectado a un GPIO
del Rpi, (ledsta)
Es necesario mantener presionado el pulsante durante aproximadamente 3 segundos
para que se apague el Rpi. Mientras se tiene presionado el pulsante, el ledsta
titila
El GPIO utilizado para conectar el pulsante, el GPIO utilizado para conectar un
led para señalización y su polarización se determinan con un archivo de texto 
en formato json que se puede editar si se utilizan pines diferentes. 
La polaridad se refiere a la forma en que se conecta el led a la salida del GPIO.
Si se conecta a través de una resistencia a GND se considera polaridad 1, 
mientras que si el led se conecta por medio de una resistencia a VCC se considera
que la polaridas es 0. 
Si no se encuentra el archivo de configuración (listen_offrpi.json) el programa
configura las variables de la siguiente manera

{"ledsta": 17, "pinoff": 27, "polaridad": 1}

'''
#!/usr/bin/env python
import RPi.GPIO as GPIO
import subprocess
import time
import json



FILECONFIG="listen_offrpi.json"
print("Comprueba configuracion hw inicial")

confighw=False
try:
    with open(FILECONFIG, 'r') as fp:
        dataconfig = json.load(fp)
    confighw=True
except:
    print("Configuracion default")
    configdefault={'ledsta':17,
                   'pinoff':27,
                   'polaridad':1}
    with open(FILECONFIG, 'w') as fp:
        json.dump(configdefault, fp)


if not confighw:
    with open(FILECONFIG, 'r') as fp:
        dataconfig = json.load(fp)
    confighw=True
    
print(dataconfig)    


led_sta=dataconfig.get('ledsta')
pinoff=dataconfig.get('pinoff')
polled=dataconfig.get('polaridad')
#starpi=27
GPIO.setmode(GPIO.BCM)
print("Listen for shutdown Rpi")
GPIO.setup(led_sta, GPIO.OUT)
if polled==0:
    GPIO.output(led_sta, False)
else:
    GPIO.output(led_sta, True)
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
            if polled==0:
                GPIO.output(led_sta, False)
            else:
                GPIO.output(led_sta, True)
        else:
            if polled==0:
                GPIO.output(led_sta, True)
            else:
                GPIO.output(led_sta, False)
            
    if counter>6:
        if polled==0:
            GPIO.output(led_sta, False)
        else:
            GPIO.output(led_sta, True)

        subprocess.call(['shutdown', '-h', 'now'], shell=False)
    else:
        print("Retardo insuficiente")
        if polled==0:
            GPIO.output(led_sta, False)
        else:
            GPIO.output(led_sta, True)
