from jugador import Jugador
from dados import Dados
from celda import Celda
from constantes import *


class Parques:

    def __init__(self, jugadores):

        if len(jugadores) < 2:
            raise AttributeError(
                'No se puede crear un parques con menos de 2 jugadores')

        self.jugadores = []
        self.tablero = []
        self.escalera = []  # Las fichas que van al cielo
        self.fichas = []
        self.carcel = set()
        self.cielo = set()  # Las fichas que ya ganaron
        self.esperando_movimiento = False
        self.jugador_actual = None
        self.dados = Dados()
        self.ganador = None

        for datos in jugadores:
            jugador = Jugador(*datos)
            self.jugadores.append(jugador)
            if datos[2] == 1:
                self.jugador_actual = jugador

        for jugador in self.jugadores:
            for ficha in jugador.fichas:
                self.fichas.append(ficha)

        for ficha in self.fichas:
            self.carcel.add(ficha)

        self.construir_tablero()

    def construir_tablero(self):
        colores = Color()
        cont = 1
        for i in range(1, 5):
            for j in range(1, 18):
                if j == 1:
                    tipo = TipoDeCelda.LLEGADA
                elif j == 6:
                    tipo = TipoDeCelda.SALIDA
                elif j == 13:
                    tipo = TipoDeCelda.SEGURO
                else:
                    tipo = TipoDeCelda.NORMAL
                celda = Celda(cont, tipo, colores.obtener())
                self.tablero.append(celda)
                cont += 1
        cont = 1
        for i in range(1, 5):
            for j in range(1, 8):
                celda = Celda(cont, TipoDeCelda.CIELO, colores.obtener())
                self.escalera.append(celda)
                cont += 1

    def lanzar_dados(self, turno):
        if self.esperando_movimiento or self.jugador_actual.turno != turno:
            return None

        dados = self.dados.lanzar()

        # Si el jugador esta en la carcel y no saco senas:
        if self.jugador_actual.en_carcel and not self.dados.es_senas:
            self.esperando_movimiento = False  # No hacer nada
            self.cambiar_turno()  # Siguiente jugador

        # Si el jugador esta en la carcel y saco senas:
        elif self.jugador_actual.en_carcel and self.dados.es_senas:
            self.jugador_actual.en_carcel = False  # Sacarlo de la carcel
            self.carcel -= self.jugador_actual.fichas  # Sacar su fichas de la carcel
            for celda in self.tablero:  # Buscar la celda de salida del jugador
                if (celda.color == self.jugador_actual.color)\
                        and (celda.tipo == TipoDeCelda.SALIDA):
                    if len(celda.fichas) > 0:  # Si la salida tiene fichas
                        fichas_foraneas = [ficha for ficha in celda.fichas if ficha.color != celda.color]  # Todas las fichas que no son del color de la celda
                        celda.fichas.difference_update(fichas_foraneas)  # Quitarlas de la celda
                        self.carcel.update(fichas_foraneas)  # Y enviarlas a la carcel
                    celda.fichas.update(self.jugador_actual.fichas)  # Finalmente, poner las fichas del jugador en la salida
                    break
        elif not self.jugador_actual.en_carcel:
            self.esperando_movimiento = True
        return dados

    def mover(self, ficha_id, celda_pos, turno):
        if not self.esperando_movimiento or self.jugador_actual.turno != turno:
            return False

        ficha = self.obtener_ficha(ficha_id)
        celda_origen = self.obtener_celda_de(ficha)
        if type(celda_pos) is int:
            celda_destino = self.tablero[celda_pos]
        else:
            celda_destino = self.escalera[int(celda_pos)]

        movimiento_valido = self.validar_movimiento(ficha, celda_origen, celda_destino)

        if not movimiento_valido:
            return False

        # Si el movimiento es valido

        if ficha in self.carcel:  # Si la ficha esta en la carcel
            self.__mover_desde_carcel(ficha, celda_destino)  # Mover desde la carcel
            self.buscar_ganador()
            return True

        # Si la ficha esta en la llegada o en la escalera al cielo
        if celda_origen.tipo == TipoDeCelda.LLEGADA or celda_origen.tipo == TipoDeCelda.CIELO:
            self.__mover_en_cielo(ficha, celda_origen, celda_destino)  # Mover en el cielo
            self.buscar_ganador()
            return True

        # Si nada de lo anterior entonces es una celda normal
        self.__mover_normal(ficha, celda_origen, celda_destino)

        self.buscar_ganador()
        return True

    def buscar_ganador(self):
        rojas = [ficha for ficha in self.cielo if ficha.color == Color.ROJO]
        amarillas = [ficha for ficha in self.cielo if ficha.color == Color.AMARILLO]
        azules = [ficha for ficha in self.cielo if ficha.color == Color.AZUL]
        verdes = [ficha for ficha in self.cielo if ficha.color == Color.VERDE]

        if len(rojas) == 4:
            self.ganador = "rojo"
            return
        elif len(amarillas) == 4:
            self.ganador = "amarillo"
            return
        elif len(azules) == 4:
            self.ganador = "azul"
            return
        elif len(verdes) == 4:
            self.ganador = "verde"
            return

    def __mover_en_cielo(self, ficha, celda_origen, celda_destino):
        celda_origen.fichas.difference_update(ficha)
        if celda_destino.posicion == 7:
            self.cielo.update(ficha)
        else:
            celda_destino.fichas.update(ficha)

    def __mover_normal(self, ficha, celda_origen, celda_destino):
        celda_origen.difference_update(ficha)
        celda_destino.fichas.update(ficha)

        # Si hay otras fichas en la celda de destino:
        if len(celda_destino.fichas) > 0:
            diferentes = [f for f in celda_destino.fichas if f.color != ficha.color]  # Tomar las de diferente color
            celda_destino.difference_update(diferentes)  # Quitarlas de la celda
            self.carcel.update(diferentes)  # Enviarlas a la carcel

    def __mover_desde_carcel(self, ficha, celda_destino):
        self.carcel.difference_update(ficha)
        celda_destino.update(ficha)

        # Si hay otras fichas en la celda de destino:
        if len(celda_destino.fichas) > 0:
            diferentes = [f for f in celda_destino.fichas if f.color != ficha.color]  # Tomar las de diferente color
            celda_destino.difference_update(diferentes)  # Quitarlas de la celda
            self.carcel.update(diferentes)  # Enviarlas a la carcel

    def validar_movimiento(self, ficha, origen, destino):
        # Si la ficha esta en la carcel y no saco senas
        if ficha in self.carcel and not self.dados.es_senas:
            return False
        # Si esta en cielo, solo puede ir a cielo
        if origen.tipo == TipoDeCelda.CIELO and destino.tipo != TipoDeCelda.CIELO:
            return False
        # Si esta en su propia llegada, solo puede ir a cielo
        if (origen.tipo == TipoDeCelda.LLEGADA and origen.color == ficha.color) and destino.tipo != TipoDeCelda.CIELO:
            return False
        # Si la distancia esta cubierta por un resultado de los dados
        diferencia = destino.posicion - origen.posicion
        if diferencia == self.dados.dado1 or diferencia == self.dados.dado2 or diferencia == self.dados.valor():
                return True
        return False

    def agregar_ficha(self, celda, ficha):
        if len(celda.fichas) > 0 and not celda.es_seguro():  # Si la salida tiene fichas
            fichas_foraneas = [f for f in celda.fichas if f.color != ficha.color]  # Todas las fichas de diferente color
            celda.fichas.difference_update(fichas_foraneas)  # Quitarlas de la celda
            self.carcel.update(fichas_foraneas)  # Y enviarlas a la carcel
        celda.fichas.update(ficha)  # Finalmente, poner la fichas del jugador en la celda

    def obtener_celda_de(self, ficha):
        for celda in self.tablero:
            if ficha in celda.fichas:
                return celda
        for celda in self.escalera:
            if ficha in celda.fichas:
                return celda
        return None

    def obtener_ficha(self, ficha_id):
        for ficha in self.fichas:
            if ficha.id == ficha_id:
                return ficha
        return None

    def cambiar_turno(self):
        siguiente = self.jugador_actual.turno + 1
        if siguiente > len(self.jugadores):
            siguiente = 1

        for jugador in self.jugadores:
            if jugador.turno == siguiente:
                self.jugador_actual = jugador
