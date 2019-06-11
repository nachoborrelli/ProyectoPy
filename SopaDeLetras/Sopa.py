import sys
import PySimpleGUI as sg
import random
import string
from SopaDeLetras.configuracion import configPalabras

#--------------------------------------- Functions ---------------------------------------

def bienvenida():

    layout_bienvenido = [
                            [sg.Image(filename='bienvenido_image.png')]

                         ]

    bienvenido = sg.Window('Bienvenido!', layout=layout_bienvenido)
    event,  values = bienvenido.Read(timeout=4000)


def select_words(dic_palabras, cantverbos, cantadj, cantsust):
    wordDic = []
    tempList = dic_palabras['__verbos__'].copy()
    wordDic['verbos'] = random.choices(tempList, k=cantverbos)
    tempList = dic_palabras['__sustantivos__'].copy()
    wordDic['sustantivos'] = random.choices(tempList, k=cantsust)
    tempList = dic_palabras['__adjetivos__'].copy()
    wordDic['adjetivos'] = random.choices(tempList, k=cantadj)
    return wordDic


def longest_word(dic_palabras):
    max = -1
    palMax = ''
    for pal in palabras:
        if len(pal) > max:
            palMax = pal
            max = len(pal)
    return palMax


def draw_grid(window, palMax, g, coordenadas):
    ''' Dibuja con letras random (POR AHORA) la matriz. A su vez, guarda en un diccionario auxiliar
    con las cordenadas como clave y su letra como valor.
        '''
    for row in range(len(palMax)):
        for col in range(len(palMax)):
            g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3),
                            (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black')  #Creo la grilla
            letra = random.choice(string.ascii_uppercase)       #Me guardo una letra random
            g.DrawText('{}'.format(letra), (col * BOX_SIZE + 15, row * BOX_SIZE + 15), font='Courier 25')  #Escribo la letra.
            coordenadas[(col, row)] = letra         #Generacion del diccionario auxiliar.


def Pintar(coordenadas, pintados, g, punto):
    '''  Se ocupa de indicar como marcada una casilla pintandola en gris.
        '''
    g.DrawRectangle((punto[0] * BOX_SIZE + 5, punto[1] * BOX_SIZE + 3),
                    (punto[0] * BOX_SIZE + BOX_SIZE + 5, punto[1] * BOX_SIZE + BOX_SIZE + 3), line_color='black',
                    fill_color='grey72')
    g.DrawText('{}'.format(coordenadas[punto]), (punto[0] * BOX_SIZE + 15, punto[1]* BOX_SIZE + 15),
               font='Courier 25')
    pintados[punto] = coordenadas[punto]  #Mantengo una estructura con solo las casillas pintadas.
    del coordenadas[punto]                  #Y las saco de mi estructura auxiliar.


def Despintar(coordenadas, pintados, g, punto):
    g.DrawRectangle((punto[0] * BOX_SIZE + 5, punto[1] * BOX_SIZE + 3),
                    (punto[0] * BOX_SIZE + BOX_SIZE + 5, punto[1] * BOX_SIZE + BOX_SIZE + 3), line_color='black',
                    fill_color='white')
    g.DrawText('{}'.format(pintados[punto]), (punto[0] * BOX_SIZE + 15, punto[1] * BOX_SIZE + 15),
               font='Courier 25')
    coordenadas[punto] = pintados[punto]   #Devuelvo la casilla de la estructura de pintados a mi auxiliar
    del pintados[punto]

#--------------------------------------- Layouts ---------------------------------------

layout = [
            [sg.Text('Sopa De Letras'), sg.Text('', key='_OUTPUT_')],
            [sg.Graph((700, 600), (0, 330), (330, 0), key='_GRAPH_', change_submits=True, drag_submits=False, background_color='white')],
            [sg.Button('Show'), sg.Button('Exit')]
         ]

window = sg.Window('Window Title', ).Layout(layout).Finalize()

# ------------------------------------ Estructuras ------------------------------------
dic_palabras = {}
dic_palabras['__verbos__'] = []  # dic de palabras clasificadas por tipo
dic_palabras['__adjetivos__'] = []
dic_palabras['__sustantivos__'] = []

#--------------------------------------- Main ---------------------------------------


bienvenida()
config_values = configPalabras(dic_palabras)                  #Levantar configuracion
palabras = select_words(dic_palabras, config_values['__cantverbos__'], config_values['__cantadjetivos__'], config_values['__cantsustantivos__'])                                   #Seleccionar palabras a usar
palMax = longest_word(palabras)


g = window.FindElement('_GRAPH_')
BOX_SIZE = 25      # Tamaño de las casillas

coordenadas = {}
draw_grid(window, palMax, g, coordenadas)
pintados = {}


while True:             # Event Loop
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    mouse = values['_GRAPH_']
    if event == '_GRAPH_':
        if mouse == (None, None):
            pass            #Pass vs continue?
        else:
            x = mouse[0] // BOX_SIZE
            y = mouse[1] // BOX_SIZE
            punto = (x, y)
            if punto in coordenadas.keys():
                try:                                           #Esto no va, hay que ajustar el tamaño de la window.
                    Pintar(coordenadas, pintados, g, punto)
                except KeyError:
                    pass
            else:
                try:                                           #Same con este.
                    Despintar(coordenadas, pintados, g, punto)
                except KeyError:
                    pass

