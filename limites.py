import pygame

class DibujaLimites:
    def __init__(self, game):
        self.game = game

    def dibuja_limites(self):
        pygame.draw.line(self.game.ventana, self.game.GRIS2, (self.game.LIMITE_IZQ, self.game.LIMITE_UP), (self.game.LIMITE_IZQ, self.game.LIMITE_BAJO))
        pygame.draw.line(self.game.ventana, self.game.GRIS2, (self.game.LIMITE_DER, self.game.LIMITE_UP), (self.game.LIMITE_DER, self.game.LIMITE_BAJO))
        pygame.draw.line(self.game.ventana, self.game.GRIS2, (self.game.LIMITE_IZQ, self.game.LIMITE_UP), (self.game.LIMITE_DER, self.game.LIMITE_UP))
