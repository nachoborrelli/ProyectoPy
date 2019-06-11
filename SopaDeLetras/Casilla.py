class Casilla:
    def __init__(self, letra, posicion):
        self.__letter__ = letra
        self.__position__ = posicion
        self.__color__ = (255, 255, 255)

    def get_letter(self):
        return self.__letter__

    def get_position(self):
        return self.__position__

    def get_color(self):
        return self.__color__

    def set_color(self, c):
        self.__color__ = c

