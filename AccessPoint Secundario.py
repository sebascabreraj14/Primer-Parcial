# ESP32_SECUNDARIO_DHT11.py
import network
import socket
import time
import dht
from machine import Pin

# Configuración WiFi
SSID = "Sebas"
PASSWORD = "1234sebas"

# Nombre para intentar que aparezca en Fing (no garantizado en AP de MicroPython)
HOSTNAME = "SensorDHT11"

# Sensor DHT11 en GPIO14
sensor = dht.DHT11(Pin(14))

# Conectar a la red del ESP32 principal
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.config(dhcp_hostname=HOSTNAME)  # Intento de nombre
sta.connect(SSID, PASSWORD)

print(" Conectando al AP...")
while not sta.isconnected():
    time.sleep(1)
print(" Conectado al AP")
print("IP asignada:", sta.ifconfig()[0])
