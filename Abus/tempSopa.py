import sys
import PySimpleGUI as sg
import random
import string
from Mati import Web
from SopaDeLetras.configuracion import configPalabras

# --------------------------------------- Global Variables -------------------------------------------------------------

BOX_SIZE = 25  # Tamaño de las casillas


# --------------------------------------- Functions ---------------------------------------------------------------------

def bienvenida():
    layout_bienvenido = [
        [sg.Image(filename='bienvenido_image.png')]

    ]

    bienvenido = sg.Window('Bienvenido!', layout=layout_bienvenido)
    event, values = bienvenido.Read(timeout=4000)


def select_words(dic_palabras, cantverbos, cantadj, cantsust):
    wordDic = {}
    wordDic['verbos'] = []  # dic de palabras clasificadas por tipo
    wordDic['adjetivos'] = []
    wordDic['sustantivos'] = []
    if (cantverbos != 0):
        tempList = dic_palabras['__verbos__'].copy()
        wordDic['verbos'] = random.sample(tempList, k=cantverbos)
    if (cantsust != 0):
        tempList = dic_palabras['__sustantivos__'].copy()
        wordDic['sustantivos'] = random.sample(tempList, k=cantsust)
    if (cantadj != 0):
        tempList = dic_palabras['__adjetivos__'].copy()
        wordDic['adjetivos'] = random.sample(tempList, k=cantadj)
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


def calc_palMaxSide():  #################
    palMax = len(longest_word(wordDic))
    if (palMax < 5):
        palMax += 6
    elif ((palMax >= 5) and (palMax <= 7)):
        palMax += 4
    else:
        palMax += 2

    return palMax


def calc_cantPalabrasSide(wordDic):

    cant_palabras = len(wordDic['verbos']) + len(wordDic['sustantivos']) + len(wordDic['adjetivos'])
    if cant_palabras < 7:  #
        cant_palabras += 5  #
    else:
        cant_palabras += 2
    return cant_palabras


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
    palMax = calc_palMaxSide()
    cant_palabras = calc_cantPalabrasSide(wordDic)

    if orientacion == 'Horizontal':  # recorrer por filas
        crearLineas(palMax, cant_palabras)
        for lista in wordDic:
            for palabra in wordDic[lista]:
                while True:
                    ok = True
                    x = random.randrange(0, palMax - 1)
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
                                graph.DrawText('{}'.format(palabra[j]), (x * BOX_SIZE + 15, (y + j) * BOX_SIZE + 15),
                                               font='Courier 25')  # Escribo la letra
                    break
        rellenarConLetrasRandom(cant_palabras, palMax)


def Pintar(coordenadas, pintados, graph, punto, color= 'grey72'):
    '''  Se ocupa de indicar como marcada una casilla pintandola en gris.
        '''
    graph.DrawRectangle((punto[0] * BOX_SIZE + 5, punto[1] * BOX_SIZE + 3),
                        (punto[0] * BOX_SIZE + BOX_SIZE + 5, punto[1] * BOX_SIZE + BOX_SIZE + 3), line_color='black',
                        fill_color=color)
    graph.DrawText('{}'.format(coordenadas[punto]), (punto[0] * BOX_SIZE + 15, punto[1] * BOX_SIZE + 15),
                   font='Courier 25')
    pintados[punto] = coordenadas[punto]  # Mantengo una estructura con solo las casillas pintadas.
    del coordenadas[punto]  # Y las saco de mi estructura auxiliar.


def Despintar(coordenadas, pintados, graph, punto):
    graph.DrawRectangle((punto[0] * BOX_SIZE + 5, punto[1] * BOX_SIZE + 3),
                        (punto[0] * BOX_SIZE + BOX_SIZE + 5, punto[1] * BOX_SIZE + BOX_SIZE + 3), line_color='black',
                        fill_color='white')
    graph.DrawText('{}'.format(pintados[punto]), (punto[0] * BOX_SIZE + 15, punto[1] * BOX_SIZE + 15),
                   font='Courier 25')
    coordenadas[punto] = pintados[punto]  # Devuelvo la casilla de la estructura de pintados a mi auxiliar
    del pintados[punto]

def FormarPalabra(pintados):  #Hasta donde se, el sorted funciona con las 2 orientaciones
    keys = sorted(pintados.keys())
    print (keys)
    pal = ''
    for key in keys:
        pal = pal + pintados[key]
    return pal

# ------------------------------------ Estructuras,Config y bienvenida ---------------------------------------------------------------------
# bienvenida()
config_values = {}
config_values['__verbColorChooser__'] = '#ee5357'
config_values['__adjColorChooser__'] = '#6df54b'
config_values['__sustColorChooser__'] = '#5b4ff2'
config_values['__cantadjetivos__'] = 3
config_values['__cantsustantivos__'] = 4
config_values['__cantverbos__'] = 4

config_values['__ayuda__'] = 'No'
config_values['__orientacion__'] = 'Horizontal' #'Vertical'
config_values['__letras__'] = 'Mayúsculas'      #'Minúsculas'

#si tiene ayuda:
config_values['__ayudalistaPalabras__'] = True
config_values['__ayudaDefinicion__'] = True






dic_palabras = {}
dic_palabras['__verbos__'] = ['cagar','comer', 'coger', 'respirar' , 'caminar']  # dic de palabras clasificadas por tipo
dic_palabras['__adjetivos__'] = ['lindo', 'rojo' , 'feo' , 'monótono' ,'extraordinario']
dic_palabras['__sustantivos__'] = ['dinosaurio', 'embotellamiento', 'termotanque' , 'llamas']

coordenadas = {}
pintados = {}
#config_values = configPalabras(dic_palabras)  # Levantar configuracion
wordDic = select_words(dic_palabras, config_values['__cantverbos__'],  # Seleccionar palabras a usar
                       config_values['__cantadjetivos__'],
                       config_values['__cantsustantivos__']
                       )

# --------------------------------------- Layouts ----------------------------------------------------------------------

layoutHorizontal = [
    [sg.Text('Sopa De Letras'), sg.Text('', key='_OUTPUT_')],
    [sg.Graph((500, 500),                                                       #canvas_size
              (0, BOX_SIZE * calc_cantPalabrasSide(wordDic) + 3),               #graph_bottom_left
              (BOX_SIZE * calc_palMaxSide() + 5, 0), key='_GRAPH_',             #graph_top_right
              change_submits=True, drag_submits=False, background_color='white')],
    [sg.Button('Adjetivo', button_color=('black', config_values['__adjColorChooser__']),font=('none' , 10, 'bold'), size=(9, 2)),
     # Los colores deberian llegar por parametro.
     sg.Button('Verbo', button_color=('black', config_values['__verbColorChooser__']),font=('none' , 10, 'bold'), size=(9, 2)),
     sg.Button('Sustantivo', button_color=('black', config_values['__sustColorChooser__']),font=('none' , 10, 'bold'), size=(9, 2)),
     sg.Button('Ayuda', key='__helpButton__', button_color=('black', '#ff8100'),font=('none' , 10, 'bold'), size=(9, 2))],
    [sg.Button('Terminar', button_color=('black', 'grey55')), sg.Button('Salir', button_color=('black', 'grey55'))]
    # Salir no tendria q estar...
]

layoutVertical = [
    [sg.Text('Sopa De Letras'), sg.Text('', key='_OUTPUT_')],
    [sg.Graph((500, 500),                                                           #canvas_size
              (0, BOX_SIZE * calc_palMaxSide() + 3),                                #graph_bottom_left
              (BOX_SIZE * calc_cantPalabrasSide(wordDic) + 5, 0), key='_GRAPH_',    #graph_top_right
              change_submits=True, drag_submits=False, background_color='white')],
    [sg.Button('Adjetivo', button_color=('black', config_values['__adjColorChooser__']), size=(9, 2)),
     # Los colores deberian llegar por parametro.
     sg.Button('Verbo', button_color=('black', config_values['__verbColorChooser__']), size=(9, 2)),
     sg.Button('Sustantivo', button_color=('black', config_values['__sustColorChooser__']), size=(9, 2))],
    [sg.Button('Terminar', button_color=('black', 'grey55')), sg.Button('Salir', button_color=('black', 'grey55'))]
    # Salir no tendria q estar...
]

helpLayout = [  [sg.Text('Definicion de una palabra al azar')],
                [sg.Multiline('',key = '__helpText__',size=(50,20))],
                [sg.Quit('Cerrar')]
            ]


if (config_values['__orientacion__'] == 'Horizontal'):
    sopa_window = sg.Window('Window Title').Layout(layoutHorizontal).Finalize()
else:
    sopa_window = sg.Window('Window Title').Layout(layoutVertical).Finalize()

if config_values['__ayudaDefinicion__'] == False:
    sopa_window.FindElement('__helpButton__').Update(visible=False)

graph = sopa_window.FindElement('_GRAPH_')

help_window = sg.Window('Ayudin' ,layout=helpLayout, no_titlebar=True )

# --------------------------------------- Main -------------------------------------------------------------------------



draw_grid(sopa_window, config_values['__orientacion__'], graph, coordenadas,wordDic)

while True:  # Event Loop
    event, values = sopa_window.Read()
    print(event)
    if event is None or event == 'Terminar' or event == 'Salir':
        break
    elif event == '_GRAPH_':
        mouse = values['_GRAPH_']
        if mouse == (None, None):
            pass  # Pass vs continue?
        else:
            x = mouse[0] // BOX_SIZE
            y = mouse[1] // BOX_SIZE
            punto = (x, y)
            if punto in coordenadas.keys():
                try:  # Esto no va, hay que ajustar el tamaño de la window.
                    Pintar(coordenadas, pintados, graph, punto)
                except KeyError:
                    pass
            else:
                try:  # Same con este.
                    Despintar(coordenadas, pintados, graph, punto)
                except KeyError:
                    pass
    elif event == 'Adjetivo' or event == 'Sustantivo' or event == 'Verbo':
            print('entra')
            clave = '__' + event + 's' + '__'
            clave = clave.lower()
            pal = FormarPalabra(pintados)
            print (pal)
            if pal in dic_palabras[clave]:
                if clave == '__adjetivos__':
                    color = config_values['__adjColorChooser__']
                elif clave == '__sustantivos__':
                    color = config_values['__sustColorChooser__']
                else:
                    color = config_values['__verbColorChooser__']
                pintadosClone = pintados.copy()   #Puede ser keys creo
                print(pintadosClone)
                for punto in pintadosClone:
                    Despintar(coordenadas,pintados,graph,punto)
                for punto in pintadosClone:
                    Pintar(coordenadas, pintadosClone, graph, punto, color)
            else:
                pintadosClone = pintados.copy()   # si no haces copias: RuntimeError: dictionary changed size during iteration (??)
                for punto in pintadosClone:
                    Despintar(coordenadas, pintados, graph, punto)
            pal=''
    elif event == '__helpButton__':
        help_window.FindElement('__helpText__').Update(Web.Definicion(random.choice(random.choice(list(wordDic.values())))))    #elegir random word y tirar la definicion
        helpevent, helpvalues= help_window.Read()