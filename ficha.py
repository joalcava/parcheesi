class Ficha:

    id_cont = 11

    def __init__(self, color):
        self.id = Ficha.id_cont + 11
        self.color = color
        self.puede_moverse = False
        Ficha.id_cont += 11
