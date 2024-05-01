# listen_offrpi
Apaga de forma segura el Raspberry Pi presionando un pulsante

## Configuracion de GPIO utilizados
El GPIO utilizado para conectar el pulsante, el GPIO utilizado para conectar un led para señalización y su polarización se determinan con un archivo de texto en formato json que se puede editar si se utilizan pines diferentes.
La polaridad se refiere a la forma en que se conecta el led a la salida del GPIO. Si se conecta a través de una resistencia a GND se considera polaridad 1, mientras que si el led se conecta por medio de una resisitencia a VCC se considera que la polaridas es 0.
Si no se encuentra el archivo de configuración (listen_offrpi.json) el programa configura las variables de la siguiente manera<br>

{"ledsta": 17, "pinoff": 27, "polaridad": 1}

## Actualización de subrutinas
En la última actualización del sistema operativo del Rpi no se pudo utilizar las rutinas para manejo de la interrupción de espera de estado del pin. Por esta razón se utiliza una variación que utiliza una librería que viene instalada por defecto y que esta documentada en

https://gpiozero.readthedocs.io/

La nueva rutina se codifica en shutdwnbypin.py y se activa con el servicio shutdwnbypin.service.

La subrutina esta basada en el trabajo encontrado en este repositorio

https://github.com/TonyLHansen/raspberry-pi-safe-off-switch



