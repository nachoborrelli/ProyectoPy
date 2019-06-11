import sys
import PySimpleGUI as sg
import random
import string

#--------------------------------------- Functions ---------------------------------------

def bienvenida():

    layout_bienvenido = [
                            [sg.Image(filename='bienvenido_image.png')]

                         ]


    bienvenido = sg.Window('Bienvenido!', layout=layout_bienvenido)
    event,  values = bienvenido.Read(timeout=4000)

def draw_grid(window,palMax,g,coordenadas):

    for row in range(len(palMax)):
        for col in range(len(palMax)):
            g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3),
                            (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black')
            # g.DrawText('{}'.format(row * 6 + col + 1), (col * BOX_SIZE + 10, row * BOX_SIZE + 8))
            letra=random.choice(string.ascii_uppercase)
            g.DrawText('{}'.format(letra), (col * BOX_SIZE + 15, row * BOX_SIZE + 15),
                       font='Courier 25')
            coordenadas[(col,row)]=letra
    return coordenadas
#--------------------------------------- Layouts ---------------------------------------

layout = [
            [sg.Text('Sopa De Letras'), sg.Text('', key='_OUTPUT_')],
            [sg.Graph((700,600), (0,450), (450,0), key='_GRAPH_', change_submits=True, drag_submits=False,background_color='white')],
            [sg.Button('Show'), sg.Button('Exit')]
         ]

window = sg.Window('Window Title', ).Layout(layout).Finalize()


#--------------------------------------- Main ---------------------------------------


#bienvenida()
#draw_grid(window)
g = window.FindElement('_GRAPH_')
BOX_SIZE = 25
palabras=['milanesa','telefono','galletitas','computadora','sdkjfisdfjdsf']
max=-1
for pal in palabras:
    if (len(pal)>max):
        palMax=pal
        max=len(pal)
print(palMax)
coordenadas={}
coordenadas=draw_grid(window,palMax,g,coordenadas)
borrados={}
while True:             # Event Loop
    event, values = window.Read()
    print(event, values)
    if event is None or event == 'Exit':
        break
    mouse = values['_GRAPH_']
    if event == '_GRAPH_':
        if mouse == (None, None):
            continue            #Pass vs continue?
        box_x = mouse[0] // BOX_SIZE
        box_y = mouse[1] // BOX_SIZE
        letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
        print(box_x, box_y)
        punto=(box_x,box_y)
        if(punto in coordenadas.keys()):
            g.DrawRectangle((box_x * BOX_SIZE + 5, box_y * BOX_SIZE + 3),
                            (box_x * BOX_SIZE + BOX_SIZE + 5, box_y * BOX_SIZE + BOX_SIZE + 3), line_color='black',
                            fill_color='red')
            g.DrawText('{}'.format(coordenadas[punto]), (box_x * BOX_SIZE + 15, box_y * BOX_SIZE + 15),
                       font='Courier 25')
            borrados[punto]=coordenadas[punto]
            del coordenadas[punto]
        else:
            g.DrawRectangle((box_x * BOX_SIZE + 5, box_y * BOX_SIZE + 3),
                            (box_x * BOX_SIZE + BOX_SIZE + 5, box_y * BOX_SIZE + BOX_SIZE + 3), line_color='black',fill_color='white')
            g.DrawText('{}'.format(borrados[punto]), (box_x * BOX_SIZE + 15, box_y * BOX_SIZE + 15),
                       font='Courier 25')
            coordenadas[punto]=borrados[punto]
            del borrados[punto]