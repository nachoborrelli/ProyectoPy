import sys
import PySimpleGUI as sg
import random
import string

"""
    Demo application to show how to draw rectangles and letters on a Graph Element
    This demo mocks up a crossword puzzle board
    It will place a letter where you click on the puzzle
"""


BOX_SIZE = 25
palabras=['milanesa','telefono','galletitas','computadora','sdkjfisdfjdsf']
max=-1
for pal in palabras:
    if (len(pal)>max):
        palMax=pal
        max=len(pal)
print(palMax)
#borrzr

layout = [
            [sg.Text('Crossword Puzzle Using PySimpleGUI'), sg.Text('', key='_OUTPUT_')],
            [sg.Graph((700,600), (0,450), (450,0), key='_GRAPH_', change_submits=True, drag_submits=False)],
            [sg.Button('Show'), sg.Button('Exit')]
         ]

window = sg.Window('Window Title', ).Layout(layout).Finalize()

g = window.FindElement('_GRAPH_')

for row in range(len(palMax)):
    for col in range(len(palMax)):
        g.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black')
        #g.DrawText('{}'.format(row * 6 + col + 1), (col * BOX_SIZE + 10, row * BOX_SIZE + 8))
        g.DrawText('{}'.format(random.choice(string.ascii_uppercase)), (col * BOX_SIZE + 15, row * BOX_SIZE + 15),font='Courier 25')

while True:             # Event Loop
    event, values = window.Read()
    print(event, values)
    if event is None or event == 'Exit':
        break
    mouse = values['_GRAPH_']
