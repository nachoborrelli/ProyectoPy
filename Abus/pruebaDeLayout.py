import PySimpleGUI as sg
from SopaDeLetras import configuracion as config

dic_palabras = {}
dic_palabras['__verbos__'] = []  # dic de palabras clasificadas por tipo
dic_palabras['__adjetivos__'] = []
dic_palabras['__sustantivos__'] = []
print(config.configPalabras(dic_palabras))
