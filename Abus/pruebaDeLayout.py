import PySimpleGUI as sg
config_values = {}
config_values['__verbColorChooser__'] = '#f17850'
config_values['__adjColorChooser__'] = '#2d06c4'
config_values['__sustColorChooser__'] = '#3707f5'
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


layoutVertical = [
    [sg.Text('Sopa De Letras'), sg.Text('', key='_OUTPUT_')],
    [sg.Graph((500, 500),                                                           # canvas_size
              (0, 25 * 17 + 3),                                #graph_bottom_left
              (25 * 16 + 5, 0), key='_GRAPH_',    #graph_top_right
              change_submits=True, drag_submits=False, background_color='white')],
    [sg.Button('Adjetivo', button_color=('black', config_values['__adjColorChooser__']), size=(9, 2)),
     # Los colores deberian llegar por parametro.
     sg.Button('Verbo', button_color=('black', config_values['__verbColorChooser__']), size=(9, 2)),
     sg.Button('Sustantivo', button_color=('black', config_values['__sustColorChooser__']), size=(9, 2))],
    [sg.Button('Terminar', button_color=('black', 'grey55')), sg.Button('Salir', button_color=('black', 'grey55'))]

]

sopa_window = sg.Window('Window Title').Layout(layoutVertical).Finalize()