from constantes import *


class Celda:

    def __init__(self, posicion, tipo, color):
        self.posicion = posicion
        self.tipo = tipo
        self.color = color
        self.fichas = set()

    def es_seguro(self):
        if self.tipo != TipoDeCelda.NORMAL:
            return True
        return False
