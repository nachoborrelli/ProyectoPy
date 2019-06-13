import sys
import PySimpleGUI as sg
import random
import string
from SopaDeLetras.configuracion import configPalabras

#--------------------------------------- Functions ---------------------------------------------------------------------

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


def longest_word(wordDic):
    max = -1
    palMax = ''
    for list in wordDic:
        for pal in wordDic[list]:
            if len(pal) > max:
               palMax = pal
               max = len(pal)

    return palMax



def draw_grid(window, orientacion, graph, coordenadas, wordDic):
    ''' Dibuja con letras random (POR AHORA) la matriz. A su vez, guarda en un diccionario auxiliar
    con las cordenadas como clave y su letra como valor.'''

    def crearLineas(lado1, lado2):
        for col in range(lado1):  # Creo la grilla
            for row in range(lado2):
                graph.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3),
                                    (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3),
                                    line_color='black')

    def rellenarConLetrasRandom(lado1, lado2):
        for col in range(lado1):  # Agrego letras random en las posiciones libres.
            for row in range(lado2):
                letra = random.choice(string.ascii_uppercase)  # Me guardo una letra random
                if (col, row) not in coordenadas:
                    graph.DrawText('{}'.format(letra), (col * BOX_SIZE + 15, row * BOX_SIZE + 15),
                                   font='Courier 25')  # Escribo la letra.
                    coordenadas[(col, row)] = letra  # Generacion del diccionario auxiliar.

    # calcular tamaño de la grilla
    palMax = len(longest_word(wordDic))
    if (palMax < 5):
        palMax += 6
    elif ((palMax >= 5) and (palMax <= 7)):
        palMax += 4
    else:
        palMax +=  2

    cant_palabras = len(wordDic['verbos']) + len(wordDic['sustantivos']) + len(wordDic['adjetivos'])

    if cant_palabras < 7:  #
        cant_palabras += 5  #
    else:  # Revisar al final    #####################################
        cant_palabras += 2

    if orientacion == 'Horizontal':  # recorrer por filas
        crearLineas(palMax, cant_palabras)
        for lista in wordDic:
            for palabra in wordDic[lista]:
                while True:
                    ok = True
                    x = random.randrange(0, palMax-1)
                    y = random.randrange(0, cant_palabras)
                    if (palMax - x) >= len(palabra):
                        for i in range(len(palabra)):
                            if (x + i, y) in coordenadas:
                                ok = False
                                break
                        if ok == True:
                            for j in range(len(palabra)):
                                coordenadas[x + j, y] = palabra[j]
                                graph.DrawText('{}'.format(palabra[j]), ((x + j) * BOX_SIZE + 15, y * BOX_SIZE + 15),
                                               font='Courier 25')  # Escribo la letra
                    break
        rellenarConLetrasRandom(palMax, cant_palabras)
    else:
        # orientacion == 'Vertical'                                                #recorrer por columnas
        crearLineas(cant_palabras, palMax)
        for lista in wordDic:
            for palabra in wordDic[lista]:
                while True:
                    ok = True
                    x = random.randrange(0, cant_palabras)  # Cant filas
                    y = random.randrange(0, palMax - 1)
                    if (palMax - y) >= len(palabra):
                        for i in range(len(palabra)):
                            if (x, y + i) in coordenadas:
                                ok = False
                                break
                        if ok == True:
                            for j in range(len(palabra)):
                                coordenadas[x, y + j] = palabra[j]
                                graph.DrawText('{}'.format(palabra[j]), (x * BOX_SIZE + 15,(y + j) * BOX_SIZE + 15),
                                               font='Courier 25')  # Escribo la letra
                    break
        rellenarConLetrasRandom(cant_palabras, palMax)


def Pintar(coordenadas, pintados, graph, punto):
    '''  Se ocupa de indicar como marcada una casilla pintandola en gris.
        '''
    graph.DrawRectangle((punto[0] * BOX_SIZE + 5, punto[1] * BOX_SIZE + 3),
                    (punto[0] * BOX_SIZE + BOX_SIZE + 5, punto[1] * BOX_SIZE + BOX_SIZE + 3), line_color='black',
                    fill_color='grey72')
    graph.DrawText('{}'.format(coordenadas[punto]), (punto[0] * BOX_SIZE + 15, punto[1]* BOX_SIZE + 15),
               font='Courier 25')
    pintados[punto] = coordenadas[punto]  #Mantengo una estructura con solo las casillas pintadas.
    del coordenadas[punto]                  #Y las saco de mi estructura auxiliar.


def Despintar(coordenadas, pintados, graph, punto):
    graph.DrawRectangle((punto[0] * BOX_SIZE + 5, punto[1] * BOX_SIZE + 3),
                    (punto[0] * BOX_SIZE + BOX_SIZE + 5, punto[1] * BOX_SIZE + BOX_SIZE + 3), line_color='black',
                    fill_color='white')
    graph.DrawText('{}'.format(pintados[punto]), (punto[0] * BOX_SIZE + 15, punto[1] * BOX_SIZE + 15),
               font='Courier 25')
    coordenadas[punto] = pintados[punto]   #Devuelvo la casilla de la estructura de pintados a mi auxiliar
    del pintados[punto]
# ------------------------------------ Estructuras ---------------------------------------------------------------------
dic_palabras = {}
dic_palabras['__verbos__'] = []  # dic de palabras clasificadas por tipo
dic_palabras['__adjetivos__'] = []
dic_palabras['__sustantivos__'] = []

# --------------------------------------- Config y bienvenida ----------------------------------------------------------
bienvenida()
config_values = configPalabras(dic_palabras)                                                  # Levantar configuracion

# --------------------------------------- Layouts ----------------------------------------------------------------------

layout = [
            [sg.Text('Sopa De Letras'), sg.Text('', key='_OUTPUT_')],
            [sg.Graph((800, 600), (0, 450), (450, 0), key='_GRAPH_', change_submits=True, drag_submits=False, background_color='white')],
            [sg.Button('Show'), sg.Button('Exit')]
         ]

window = sg.Window('Window Title', ).Layout(layout).Finalize()

# --------------------------------------- Main -------------------------------------------------------------------------

wordDic = select_words(dic_palabras, config_values['__cantverbos__'], config_values['__cantadjetivos__'], config_values['__cantsustantivos__'])                                   #Seleccionar palabras a usar

graph = window.FindElement('_GRAPH_')

BOX_SIZE = 25                                                                               # Tamaño de las casillas

coordenadas = {}
draw_grid(window, config_values['__orientacion__'], graph, coordenadas)
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
                    Pintar(coordenadas, pintados, graph, punto)
                except KeyError:
                    pass
            else:
                try:                                           #Same con este.
                    Despintar(coordenadas, pintados, graph, punto)
                except KeyError:
                    pass

