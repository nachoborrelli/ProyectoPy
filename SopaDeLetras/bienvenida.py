import pygame,sys
from pygame.locals import *
import PySimpleGUI as sg
import os.path


def bienvenida():

    layout_bienvenido = [
                            [sg.Image(filename='bienvenido_image.png')]

                         ]


    bienvenido = sg.Window('Bienvenido!', layout=layout_bienvenido)
    event,  values = bienvenido.Read(timeout=4000)
bienvenida()


def MostrarSopa ():
    layoutsopa= [
                [sg.]
    ]