import PySimpleGUI as sg
from Mati import Web
import random

def configPalabras(dic_palabras):
    #------------------------------------ Funciones ------------------------------------
    def borrar_valor(valor,dic_palabras):

        '''borra un valor del diccionario de palabras'''
        valido=''
        if valor in dic_palabras['__verbos__']:
            dic_palabras['__verbos__'].remove(valor)
            valido='__verbos__'
        elif valor in dic_palabras['__adjetivos__']:
            dic_palabras['__adjetivos__'].remove(valor)
            valido='__adjetivos__'
        elif valor in dic_palabras['__sustantivos__']:
            dic_palabras['__sustantivos__'].remove(valor)
            valido='__sustantivos__'

        return valido


    # ------------------------------------ Layout & Design ------------------------------------

    sg.ChangeLookAndFeel('Purple')

    columna_verbos = [
        [sg.Frame('Verbos', [
        [sg.Listbox(dic_palabras['__verbos__'], key='__verbos__', size=(25, 5))],
        [sg.Text('Cantidad:'), sg.Spin([i for i in range(0, 6)], initial_value=0, size=(3, 3),key='__cantverbos__'),
        sg.ColorChooserButton('Elegir color', key='__verbColorChooser__', )]
                           ])]
    ]
    columna_adj = [
        [sg.Frame('Adjetivos', [
        [sg.Listbox( dic_palabras['__adjetivos__'], key='__adjetivos__', size=(25, 5))],
        [sg.Text('Cantidad:'), sg.Spin([i for i in range(0,  6)], initial_value=0, size=(3, 3), key='__cantadjetivos__'),
        sg.ColorChooserButton('Elegir color', key='__adjColorChooser__' )]
                            ])]
    ]
    columna_sust = [
        [sg.Frame('Sustantivos', [
        [sg.Listbox(dic_palabras['__sustantivos__'], key='__sustantivos__', size=(25, 5))],
        [sg.Text('Cantidad:'), sg.Spin([i for i in range(0,  6)], initial_value=0, size=(3, 3),key='__cantsustantivos__'),
        sg.ColorChooserButton('Elegir color', key='__sustColorChooser__', )]
                            ])]
    ]

    Config = [
        [sg.Text(' ' * 43), sg.Text('Ingrese de a una las palabras a utilizar (sin espacios en blanco)', font=('Helvetica', 11))],
        [sg.Text(' ' * 40), sg.Input(do_not_clear=False,key='__input__'),
         sg.Submit('Agregar',key='__addbutton__'), sg.Button('Eliminar',key='__deletebutton__')],
        [sg.Text('_' * 113)],
        [sg.Text('Palabras ingresadas', font=('Helvetica', 13))],
        [sg.Column(columna_verbos), sg.Column(columna_adj), sg.Column(columna_sust)],
        [sg.Text('_' * 113)],
        [sg.Text('Ayuda'), sg.InputOptionMenu(('Si' , 'No'),key='__ayuda__'),
         sg.Text('Orientacion'), sg.InputOptionMenu(('Horizontal', 'Vertical'),key='__orientacion__'),
         sg.Text('Letras'), sg.InputOptionMenu(('Mayúsculas','Minúsculas'),key='__letras__'),
         sg.Text('Tipografia'), sg.InputCombo(values=('Courier', 'Helvetica', 'Times', 'Arial', 'Comic', 'Verdana'), size =(15, 1), key='__tipografia__'),
         sg.Text(' ' *5),
         sg.Ok('Aceptar', button_color=('white', '#475841'))]

    ]

    layout_selectAyuda = [
        [sg.Text('Seleccione las ayudas a usar')],
        [sg.Checkbox('Definicion de palabra', key='__ayudaDefinicion__', default=True),
         sg.Checkbox('Lista de Palabras', key='__ayudalistaPalabras__', default=True)],
        [sg.Submit()],
    ]


    # ------------------------------------ Window Loop ------------------------------------

    ventana_IngVen = sg.Window('Configuracion', layout=Config)
    window_selectAyuda = sg.Window('Ayudas', layout=layout_selectAyuda)

    while True:
        event, values = ventana_IngVen.Read()
        tipo = ''
        if event == None:
            break
        elif event == '__addbutton__':
            valores = Web.ProcesarPalabra(values['__input__'].lower(), dic_palabras, tipo)
            print(valores[0])
            if valores[0] == False:
                #valores = Web.ProcesarPalabra(values['__input__'], dic_palabras, tipo)
                pass
            else:
                ventana_IngVen.FindElement(valores[1]).Update(dic_palabras[valores[1]])       #pos 0 = boolean si se pudo o no #pos 1 el tipo de palabra
            ventana_IngVen.Refresh()

        elif event == '__deletebutton__':
            tipo_borrado = borrar_valor(values['__input__'], dic_palabras)
            if tipo_borrado != '':                              #Chequear que la palabra a eliminar sea valida
                ventana_IngVen.FindElement(tipo_borrado).Update(dic_palabras[tipo_borrado])
            else:
                sg.PopupError('Palabra no existente',title='')

        elif event == 'Aceptar':
            if values['__cantverbos__']=='0' and values['__cantadjetivos__'] =='0'and values['__cantsustantivos__'] =='0':
                continuar = sg.PopupYesNo('Se eligieron 0 verbos, 0 adjetivos y 0 sustantivos. \n'
                                'Esto finalizará el juego y perderá todos los datos ingresados.\n'
                                'Desea continuar?',
                                title='Peligro',font=('Helvetica',9,'bold'),button_color=('#000000','#ff1919'))
                if continuar == 'Yes':
                    break
                else:
                    pass
            else:
                break
        print(event)

    if values['__ayuda__'] == 'Si':                                                         #en caso de que se seleccione ayuda,
        event_ayuda, values_ayuda = window_selectAyuda.Read()
        if event_ayuda is 'Submit':
            values['__ayudalistaPalabras__'] = values_ayuda['__ayudalistaPalabras__']
            values['__ayudaDefinicion__'] = values_ayuda['__ayudaDefinicion__']

    if values['__verbColorChooser__'] == '':                                                #Generar colores al azar si no son ingresados
        values['__verbColorChooser__'] = '#' + "%06x" % random.randint(0, 0xFFFFFF)
    if values['__adjColorChooser__'] == '':
        values['__adjColorChooser__'] = '#' + "%06x" % random.randint(0, 0xFFFFFF)
    if values['__sustColorChooser__'] == '':
        values['__sustColorChooser__'] = '#' + "%06x" % random.randint(0, 0xFFFFFF)

    valoresInservibles = ['__input__','__verbos__','__adjetivos__','__sustantivos__']       #elimino los valores devueltos por el layout que no me sirven
    for dato in valoresInservibles:
        if dato in values.keys():
            del values[dato]

    #convertir valores string a numericos para facilitar el procesamiento luego
    values['__cantsustantivos__'] = int(values['__cantsustantivos__'])
    values['__cantverbos__'] = int(values['__cantverbos__'])
    values['__cantadjetivos__'] = int(values['__cantadjetivos__'])
    print(values)
    return values
