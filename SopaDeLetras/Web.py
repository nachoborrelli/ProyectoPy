#-----------------------------------------------------------------------------------------#
# TRABAJO CONFORMADO Y REALIZADO POR ALBERCA AGUSTIN, BORRELLI JUAN IGNACIO, GEBER MATIAS #
#-----------------------------------------------------------------------------------------#

from pattern.web import Wiktionary
import pattern.text.es as patt
import PySimpleGUI as sg
import json
definiciones = {}
layoutDefinicion = [
                 [sg.Text('Ingrese una definicion para la palabra')],
                 [sg.InputText(key='__definicion__')],
                 [sg.Button('Verbo',key='__verbos__', enable_events=True),
                  sg.Button('Adjetivo',key='__adjetivos__', enable_events=True),
                  sg.Button('Sustantivo',key='__sustantivos__', enable_events=True)]
          ]
windowDefinicion = sg.Window('Definicion',layout=layoutDefinicion)

def PalabraWik(pal, dic, tipo):
    '''Va a buscar la palabra a Wiktionary y la clasifica en verbo, sustantivo o adjetivo segun
    la primer seccion por orden de relevancia, si la palabra no se encuentra en el diccionario de la pagina,
    se debera ingresar otra
    Luego si la palabra es encontrada devuelve verdadero y la agrega al diccionario segun su clasificacion '''

    w = Wiktionary(language='es')
    correcto=False
    pal.lower()
    try:
        palabra = list(w.search(pal).sections)
    except(AttributeError):
        sg.Popup('Palabra no encontrada en Wiktionary')
        tipo = 'null'
        return correcto,tipo

    else:
        if(pal in dic['__verbos__']) or (pal in dic['__sustantivos__']) or (pal in dic['__adjetivos__']):
            pass
        else:
            for x in range(len(palabra)):
                seccion=str(palabra[x])
                if('erb'in seccion) or ('ustantiv' in seccion) or ('djetiv' in seccion):
                    #print(seccion)
                    break
            if ('erb' in seccion):                #Verbo o Forma Verbal
                dic['__verbos__'].append(pal)
                tipo= '__verbos__'
                correcto=True
            elif('Sustantivo' in seccion):
                dic['__sustantivos__'].append(pal)
                tipo = '__sustantivos__'
                correcto=True
            elif('djetiv' in seccion):           #Adjetivo o Forma Adjetiva
                dic['__adjetivos__'].append(pal)
                tipo= '__adjetivos__'
                correcto=True
    return correcto, tipo

def PalabraPattern(pal):
    '''Busca la palabra en el pattern y la califica segun su tipo, si no es un verbo, sustantivo o adjetivo, se debera ingresar otra.
        TENER EN CUENTA  QUE SI LA PALABRA NO EXISTE EL MODULO PATTERN LO TOMA COMO SUSTANTIVO'''
    pal.lower()
    palabra = patt.parse(pal)
    correcto=False
    #print(palabra)
    if ('VB' in palabra):
        tipo = '__verbos__'
        correcto=True
    elif ('NN' in palabra):
        tipo = '__sustantivos__'
        correcto=True
    elif ('JJ' in palabra):
        tipo = '__adjetivos__'
        correcto=True
    else:
        tipo = ' '
    return correcto, tipo

def ProcesarPalabra(pal, dic, tipo):
    '''Toma la palabra de internet en Wiktionary, se fija su clasificacion y la compara con la clasificacion
        del modulo Pattern.es, si las 2 se encontraron en los dos sitios, pregunta si la clasificacion entre ambos sitios
        dio distinto, en caso afirmativo se agrega al reporte.
        Si no existe en Wiktionary, este devuelve falso y lo agrega al reporte indicando que no se encontro la palabra'''
    wik = PalabraWik(pal, dic, tipo)
    pat = PalabraPattern(pal)
    if wik[0] and pat[0]:
        if (wik[1] != pat[1]):
            #print(wik[1], pat[1], 'valores')
            try:
                archivo = open('Reporte.txt', 'a')
            except(FileNotFoundError):
                archivo = open('Reporte.txt', 'x')
            finally:
                archivo.write('La clasificacion de la palabra {} no coincide entre Wiktionary y Pattern. En wiktionary es: {}, y en Patter es: {}. '.format(
                        pal, wik[1], pat[1]))
                archivo.write('\n')
            archivo.close()
        return (True,wik[1])
    else:
        ok = False
        if wik[1] != pat[1]:
            try:
                archivo = open('Reporte.txt', 'a')
            except(FileNotFoundError):
                archivo = open('Reporte.txt', 'x')
            finally:
                archivo.write(' la palabra {} no se encuentra en Wiktionary . '.format(pal))
                event, values = windowDefinicion.Read()
                print(event,type(event),values)
                if (event is not 'None') and (event is not None):
                    AgregarJson(pal, values['__definicion__'])
                    archivo.write('\n')
                    ok = True
                    tipo = event
                    dic[tipo].append(pal)
                archivo.close()
                return (ok, tipo)
        return (ok, wik[1])

def Definicion(pal):
    '''Busca el articulo de la palabra en Wiktionary, selecciona la seccion con el tipo, se queda con las definiciones
    y devuelve todas las que encuentra'''
    definicion = ConsultarDefinicionJson(pal)
    if definicion:
      return definicion
    wi = Wiktionary(language='es')
    secciones = wi.search(pal).sections
    if len(secciones) > 3:
        seccion = secciones[2]
    else:
        seccion = secciones[3]
    etimologia = wi.MediaWikiSection.plaintext(seccion)

    for letra in range(len(etimologia)):
        if etimologia[letra] == '1':
            pos = letra
            break
    try:
        definicion = etimologia[pos:]
    except UnboundLocalError:
        definicion = etimologia
    return definicion

def AgregarJson(palabra, definicion):
    '''agrega una palabra con su definicion al json sin borrar los datos previos (actualiza)'''
    definiciones[palabra] = definicion
    try:
        jsonfile = open('Definiciones.json', 'x')
    except FileExistsError:
        with open('Definiciones.json', 'r') as jsonfile:
            antiguo = {}
            antiguo = json.load(jsonfile)
            definiciones.update(antiguo)
        jsonfile = open('Definiciones.json', 'w')
    finally:
        json.dump(definiciones, jsonfile)
        jsonfile.close()

def ConsultarDefinicionJson(palabra):
    '''devuelve la definicion de una palabra'''
    jsonfile = open('Definiciones.json', 'r')
    diccionario = json.load(jsonfile)
    if (palabra in diccionario.keys()):
        jsonfile.close()
        return diccionario[palabra]
    else:
        jsonfile.close()
        return False

#TRABAJO CONFORMADO Y REALIZADO POR ALBERCA AGUSTIN, BORRELLI JUAN IGNACIO, GEBER MATIAS


