from pattern.web import Wiktionary
import pattern.text.es as patt
import PySimpleGUI as sg
def ProcesarPalabra(pal, dic, tipo):
    #pal = str(input())
    def PalabraWik(pal, dic, tipo):
        '''Va a buscar la palabra a Wiktionary y la califica en verbo, sustantivo o adjetivo segun
        la primer seccion por orden de relevancia, si la palabra no se encuentra en el diccionario de la pagina,
        se debera ingresar otra'''
        w = Wiktionary(language='es')
        correcto=False
        pal.lower()
        try:
            palabra = list(w.search(pal).sections)
        except(AttributeError):
            sg.Popup('Ingrese otra palabra')
        else:
            print(palabra)
            seccion2 = str(palabra[3])
            seccion1 = str(palabra[2])
            if ('Verb' in seccion2) or ('Verb' in seccion1):                  #Verbo o Forma Verbal
                dic['__verbos__'].append(pal)
                tipo= '__verbos__'
                correcto=True
            elif('Sustantivo' in seccion2) or ('Sustantivo' in seccion1):
                dic['__sustantivos__'].append(pal)
                tipo = '__sustantivos__'
                correcto=True
            elif('Adjetiv' in seccion2) or ('Adjetiv' in seccion1):           #Adjetivo o Forma Adjetiva
                dic['__adjetivos__'].append(pal)
                tipo= '__adjetivos__'
                correcto=True
        return (correcto, tipo)

    def PalabraPattern(pal):
        '''Busca la palabra en el pattern y la califica segun su tipo, si no es un verbo, sustantivo o adjetivo, se debera ingresar otra.
            TENER EN CUENTA  QUE SI LA PALABRA NO EXISTE EL MODULO PATTERN LO TOMA COMO SUSTANTIVO'''
        pal.lower()
        palabra = patt.parse(pal)
        correcto=False
        print(palabra)
        if ('VB' in palabra):
            tipo = '__verbos__'
            correcto=True
        elif ('NN' in palabra):
            tipo = '__sustantivos__'
            correcto=True
        elif ('JJ' in palabra):
            tipo = '_adjetivos__'
            correcto=True
        else:
            tipo = ' '
            print('Ingrese otra Palabra')
        return correcto,tipo


    wik = PalabraWik(pal, dic, tipo)
    pat = PalabraPattern(pal)
    if wik[0] and pat[0]:
        if (wik[1] != pat[1]):
            try:
                archivo = open('Reporte.txt', 'a')
            except(FileNotFoundError):
                archivo = open('Reporte.txt','x')
                archivo.write('La clasificacion de la palabra {} no coincide entre Wiktionary y Pattern. En wiktionary es: {}, y en Patter es: {}. '.format(
                        pal, wik[1], pat[1]))
                #archivo.write('/n')
            else:
                archivo.write('La clasificacion de la palabra {} no coincide entre Wiktionary y Pattern. En wiktionary es: {}, y en Patter es: {}. '.format(
                        pal, wik[1], pat[1]))
                archivo.write('/n')
            archivo.close()
        return (True,wik[1])
    else:
        if (wik[1] != pat[1]):
            try:
                archivo = open('Reporte.txt', 'a')
            except(FileNotFoundError):
                archivo = open('Reporte.txt','x')
                archivo.write('La clasificacion de la palabra {} no coincide entre Wiktionary y Pattern. En wiktionary es: {}, y en Patter es: {}. '.format(
                        pal, wik[1], pat[1]))
                archivo.write('/n')
            else:
                archivo.write('La clasificacion de la palabra {} no coincide entre Wiktionary y Pattern. En wiktionary es: {}, y en Patter es: {}. '.format(
                        pal, wik[1], pat[1]))
                archivo.write('/n')
            archivo.close()
        return (False,wik[1])

def Definicion(pal):
    '''Busca el articulo de la palabra en Wiktionary, selecciona la seccion con el tipo
    y la devuelve toda como texto plano'''
    wi = Wiktionary(language='es')
    secciones = wi.search(pal).sections
    seccion = secciones[3]
    etimologia = wi.MediaWikiSection.plaintext(seccion)  # ERROR NO PUEDO ACCEDER A UNA POSICION DE UN TEXTO PLANO

    for letra in range(len(etimologia)):
        if etimologia[letra] == '1':
            pos=letra
            break
    try:
        definicion = etimologia[pos:]
    except UnboundLocalError:
        definicion = etimologia

    return definicion

