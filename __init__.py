from parques import Parques
from constantes import *

if __name__ == '__main__':
    parques = Parques(
        (
            ["", Color.AMARILLO, 1],
            ["", Color.AZUL, 2],
            ["", Color.ROJO, 3]
        )
    )

    for ficha in parques.fichas:
        print(ficha.id)
