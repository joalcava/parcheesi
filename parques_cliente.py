import pygame

class FichaCliente(pygame.sprite.Sprite):

    def __init__(self, imagen, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class ParquesCliente(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.tablero = []
        self.escalera = []
        self.carcel = []
        self.dados = []
        self.imagenes = {
            "fondo": pygame.image.load("cliente/parques.jpg"),
            "rojo": pygame.image.load("cliente/rojo.png").convert_alpha(),
            "azul": pygame.image.load("cliente/azul.png").convert_alpha(),
            "amarillo": pygame.image.load("cliente/amarillo.png").convert_alpha(),
            "verde": pygame.image.load("cliente/verde.png").convert_alpha()
        }
        fichas = [
            FichaCliente(self.imagenes["rojo"], (50, 50)),
            FichaCliente(self.imagenes["rojo"], (100, 50)),
            FichaCliente(self.imagenes["rojo"], (50, 100)),
            FichaCliente(self.imagenes["rojo"], (100, 100)),

            FichaCliente(self.imagenes["amarillo"], (50, 600)),
            FichaCliente(self.imagenes["amarillo"], (100, 600)),
            FichaCliente(self.imagenes["amarillo"], (50, 650)),
            FichaCliente(self.imagenes["amarillo"], (100, 650)),

            FichaCliente(self.imagenes["azul"], (600, 600)),
            FichaCliente(self.imagenes["azul"], (650, 600)),
            FichaCliente(self.imagenes["azul"], (600, 650)),
            FichaCliente(self.imagenes["azul"], (650, 650)),

            FichaCliente(self.imagenes["verde"], (600, 50)),
            FichaCliente(self.imagenes["verde"], (650, 50)),
            FichaCliente(self.imagenes["verde"], (600, 100)),
            FichaCliente(self.imagenes["verde"], (650, 100))
        ]
        self.fichas = pygame.sprite.Group(fichas)

    def update(self, data):
        pass

    def draw(self, pantalla):
        pantalla.fill((255, 255, 255))
        pantalla.blit(self.imagenes["fondo"], (0, 0))
        self.fichas.draw(pantalla)