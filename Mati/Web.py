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
        try:
            palabra = list(w.search(pal).sections)
        except(AttributeError):
            sg.Popup('Ingrese otra palabra')
        else:
            print(palabra)
            seccion2 = str(palabra[3])
            seccion1 = str(palabra[2])
            if ('Verbo' in seccion2) or ('Verbo' in seccion1):
                dic['__verbos__'].append(pal)
                tipo= '__verbos__'
                correcto=True
            elif('Sustantivo' in seccion2) or ('Sustantivo' in seccion1):
                dic['__sustantivos__'].append(pal)
                tipo = '__sustantivos__'
                correcto=True
            elif('Adjetivo' in seccion2) or ('Adjetivo' in seccion1):
                dic['__adjetivos__'].append(pal)
                tipo= '__adjetivos__'
                correcto=True
            elif('adjetiva' in seccion2) or ('adjetiva' in seccion1):        #Se puede unir con el de arriba_?
                dic['__adjetivos__'].append(pal)
                tipo = '__adjetivos__'
                correcto=True
        return (correcto, tipo)

    def PalabraPattern(pal):
        '''Busca la palabra en el pattern y la califica segun su tipo, si no es un verbo, sustantivo o adjetivo, se debera ingresar otra.
            TENER EN CUENTA  QUE SI LA PALABRA NO EXISTE EL MODULO PATTERN LO TOMA COMO SUSTANTIVO'''
        palabra = patt.parse(pal)
        correcto=False
        print(palabra)
        if ('VB' in palabra):
            correcto=True
        elif ('NN' in palabra):
            correcto=True
        elif ('JJ' in palabra):
            correcto=True
        else:
            print('Ingrese otra Palabra')
        return correcto
    val= PalabraWik(pal, dic, tipo)
    if val[0] and PalabraPattern(pal):
        return (True,val[1])
    else:
        return (False,val[1])

    # def Definicion(pal):
    #     '''Busca el articulo de la palabra en Wiktionary, selecciona la seccion con el tipo
    #     y la devuelve toda como texto plano'''
    #     wi = Wiktionary(language='es')
    #     secciones = wi.search(pal).sections
    #     seccion = secciones[3]
    #     definicion = wi.MediaWikiSection.plaintext(seccion)  # ERROR NO PUEDO ACCEDER A UNA POSICION DE UN TEXTO PLANO
    #     print(secciones)
    #     print(definicion)
    #     return definicion
    PalabraWik((pal, dic, tipo))
