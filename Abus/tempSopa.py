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


def select_words (dic_palabras, cantverbos, cantadj, cantsust):
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
    for pal in palabras:
        if (len(pal) > max):
            palMax = pal
            max = len(pal)
    return max

def draw_grid(window,palMax,g,coordenadas):
    '''
        '''
    for row in range(len(palMax)):
        for col in range(len(palMax)):
            g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3),
                            (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black')
            #letra = random.choice(string.ascii_uppercase)       #Me guardo una letra random
            #g.DrawText('{}'.format(letra), (col * BOX_SIZE + 15, row * BOX_SIZE + 15), font='Courier 25')

            #coordenadas[(col,row)]=letra



def Pintar(coordenadas,borrados,g,punto):
    g.DrawRectangle((punto[0] * BOX_SIZE + 5, punto[1] * BOX_SIZE + 3),
                    (punto[0] * BOX_SIZE + BOX_SIZE + 5, punto[1] * BOX_SIZE + BOX_SIZE + 3), line_color='black',
                    fill_color='red')
    g.DrawText('{}'.format(coordenadas[punto]), (punto[0] * BOX_SIZE + 15, punto[1]* BOX_SIZE + 15),
               font='Courier 25')
    borrados[punto] = coordenadas[punto]
    del coordenadas[punto]


def Despintar(coordenadas,borrados,g,punto):
    g.DrawRectangle((punto[0] * BOX_SIZE + 5, punto[1] * BOX_SIZE + 3),
                    (punto[0]* BOX_SIZE + BOX_SIZE + 5, punto[1] * BOX_SIZE + BOX_SIZE + 3), line_color='black',
                    fill_color='white')
    g.DrawText('{}'.format(borrados[punto]), (punto[0]* BOX_SIZE + 15, punto[1] * BOX_SIZE + 15),
               font='Courier 25')
    coordenadas[punto] = borrados[punto]
    del borrados[punto]
#--------------------------------------- Layouts ---------------------------------------

layout = [
            [sg.Text('Sopa De Letras'), sg.Text('', key='_OUTPUT_')],
            [sg.Graph((700,600), (0,450), (450,0), key='_GRAPH_', change_submits=True, drag_submits=False,background_color='white')],
            [sg.Button('Show'), sg.Button('Exit')]
         ]

window = sg.Window('Window Title', ).Layout(layout).Finalize()

# ------------------------------------ Estructuras ------------------------------------
dic_palabras = {}
dic_palabras['__verbos__'] = []  # dic de palabras clasificadas por tipo
dic_palabras['__adjetivos__'] = []
dic_palabras['__sustantivos__'] = []

#--------------------------------------- Main ---------------------------------------


#bienvenida()                                                           #Cartel de bienvenida
config_values = configPalabras()                                        #Levantar configuracion
palabras = select_words(dic_palabras,config_values['__cantverbos__'],config_values['__cantadjetivos__'],config_values['__cantsustantivos__'])                                   #Seleccionar palabras a usar
palMax = longest_word(palabras)


g = window.FindElement('_GRAPH_')
BOX_SIZE = 25

coordenadas={}
draw_grid(window,palMax,g,coordenadas)
borrados={}
while True:             # Event Loop
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    mouse = values['_GRAPH_']
    if event == '_GRAPH_':
        if mouse == (None, None):
            continue            #Pass vs continue?
        x = mouse[0] // BOX_SIZE
        y = mouse[1] // BOX_SIZE
        #letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
        punto=(x,y)
        if(punto in coordenadas.keys()):
           Pintar(coordenadas,borrados,g,punto)
        else:
            Despintar(coordenadas,borrados,g,punto)