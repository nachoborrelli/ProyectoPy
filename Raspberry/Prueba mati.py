#import Adafruit_DHT
from datetime import datetime
import time
import json
import os

# #=================================SENSOR======================================================
# class Temperatura:
#     def __init__(self, pin=17, sensor=Adafruit_DHT.DHT11):
#         # Usamos el DHT11 que es compatible con el DHT12
#         self._sensor = sensor
#         self._data_pin = pin
#     def datos_sensor(self):
#         humedad, temperatura = Adafruit_DHT.read_retry(self._sensor, self._data_pin)
#         return {'temperatura': temperatura, 'humedad': humedad}

def AgregarDatos(datos):
    dic = {}
    dic['Temperatura'] = datos[0]
    dic['Humedad'] = datos[1]
    dic['Fecha'] = str(datetime.fromtimestamp(time.time()))
    return dic

def datosSensor():
    return(20,60)
#temp = Temperatura()
oficinas = {}
oficinas['Oficina 1'] = []
oficinas ['Oficina 2'] = []
oficinas ['Oficina 3'] = []

while True:
    try:
        jsonfile = open('datos-oficinas.json', 'x')
    except FileExistsError:
        jsonfile = open('datos-oficinas.json', 'r+')
    time.sleep(2)
    for i in range(1,4):
        datos = datosSensor()
        print(type(datos))
        print(datos)
        oficinas['Oficina {}'.format(i)].append(AgregarDatos(datos))
    json.dump(oficinas, jsonfile)
    jsonfile.close()
    #jsonfile = open('datos-oficinas.json', 'r+')
    #oficinas = json.load(jsonfile)
    #jsonfile.write('\n')
