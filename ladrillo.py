import pygame
import random

class Ladrillo(pygame.sprite.Sprite):
    ladrillos_totales = 0
    ladrillos_destruidos = 0

    def __init__(self, game, x, y, hit_points):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.image = pygame.Surface((game.BLOQUE_SIZEX, game.BLOQUE_SIZEY))
        self.image.fill((random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit_points = hit_points

        # Incrementar el contador de ladrillos totales
        Ladrillo.ladrillos_totales += 1
        print(f"Ladrillos totales: {Ladrillo.ladrillos_totales}")

    @classmethod
    def destruir(cls):
        cls.ladrillos_destruidos += 1
        print(f"Ladrillos destruidos: {cls.ladrillos_destruidos}")

    @classmethod
    def restantes(cls):
        return cls.ladrillos_totales - cls.ladrillos_destruidos

    @classmethod
    def reiniciar_contadores(cls):
        cls.ladrillos_totales = 0
        cls.ladrillos_destruidos = 0
