import PySimpleGUI as sg
from Mati import Web as modulo

def configPalabras():
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

    #------------------------------------ Estructuras ------------------------------------
    dic_palabras = {}
    dic_palabras['__verbos__'] = []                                         #dic de palabras clasificadas por tipo
    dic_palabras['__adjetivos__'] = []
    dic_palabras['__sustantivos__'] = []
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
        [sg.Text('Ayuda'), sg.InputOptionMenu(('No', 'Si'),key='__ayuda__'),
         sg.Text('Orientacion'), sg.InputOptionMenu(('Horizontal', 'Vertical'),key='__orientacion__'),
         sg.Text('Letras'), sg.InputOptionMenu(('Mayúsculas','Minúsculas'),key='__letras__'),
         sg.Text('Tipografia'), sg.InputCombo(values=('Courier', 'Helvetica', 'Times', 'Arial', 'Comic', 'Verdana'), size =(15, 1), key='__tipografia__'),
         sg.Text(' ' *5),
         sg.Ok('Aceptar', button_color=('white', '#475841'))]

    ]

    # ------------------------------------ Window Loop ------------------------------------

    ventana_IngVen = sg.Window('Configuracion', layout=Config)

    while True:
        event, values = ventana_IngVen.Read()
        tipo = ''
        if event == '__addbutton__':
            valores = modulo.ProcesarPalabra(values['__input__'], dic_palabras, tipo)
            print(valores[0])
            if (valores[0] == False):
                valores = modulo.ProcesarPalabra(values['__input__'], dic_palabras, tipo)
            else:
                ventana_IngVen.FindElement(valores[1]).Update(dic_palabras[valores[1]])       #pos 0 = boolean si se pudo o no #pos 1 el tipo de palabra
            ventana_IngVen.Refresh()

        elif event == '__deletebutton__':
            tipo_borrado = borrar_valor(values['__input__'], dic_palabras)
            ventana_IngVen.FindElement(tipo_borrado).Update(dic_palabras[tipo_borrado])
            ventana_IngVen.Refresh()
            if tipo_borrado == '':                                           #Chequear que la palabra a eliminar sea valida
                sg.PopupError('Palabra no existente',title='')

        else:
            break

    ventana_IngVen.Refresh()

    valoresInservibles = ['__input__','__verbos__','__adjetivos__','__sustantivos__']
    for dato in valoresInservibles:
        if dato in values.keys():
            del values[dato]
    print(dic_palabras , values)
    return values
