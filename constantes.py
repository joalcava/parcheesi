class Color:
    ROJO = 1
    AMARILLO = 2
    AZUL = 3
    VERDE = 4

    __actual = 0

    def obtener(self):
        Color.__actual += 1
        if Color.__actual == 5:
            Color.__actual = 1
        return self.__actual

class TipoDeCelda:
    NORMAL = 1
    SALIDA = 2
    SEGURO = 3
    LLEGADA = 4
    CIELO = 5
