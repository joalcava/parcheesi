from ficha import Ficha

class Jugador:

    def __init__(self, nombre, color, turno):
        self.nombre = nombre
        self.color = color
        self.turno = turno
        self.en_carcel = True
        self.fichas = {
            Ficha(self.color),
            Ficha(self.color),
            Ficha(self.color),
            Ficha(self.color)
        }