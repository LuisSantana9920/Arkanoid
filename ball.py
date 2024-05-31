import pygame
from random import randint
from ladrillo import Ladrillo

class Ball(pygame.sprite.Sprite):
    def __init__(self, game, x=0, y=0, vx=None, vy=None):
        super().__init__()
        
        self.game = game
        self.image = pygame.image.load("ball.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velx = vx if vx is not None else randint(3, 6)
        self.vely = vy if vy is not None else randint(3, 6)

    def move(self):
        self.rect.move_ip(self.velx, self.vely)

        if self.rect.left <= self.game.LIMITE_IZQ or self.rect.right >= self.game.LIMITE_DER:
            self.velx = -self.velx

        if self.rect.top <= self.game.LIMITE_UP:
            self.vely = -self.vely

        if pygame.sprite.collide_rect(self, self.game.bate):
            if abs(self.rect.bottom - self.game.bate.rect.top) < 10 and self.vely > 0:
                self.vely = -self.vely
            elif abs(self.rect.right - self.game.bate.rect.left) < 10 and self.velx > 0:
                self.velx = -self.velx
            elif abs(self.rect.left - self.game.bate.rect.right) < 10 and self.velx < 0:
                self.velx = -self.velx

        ladrillos_hit = pygame.sprite.spritecollide(self, self.game.lista_ladrillos, True)
        if ladrillos_hit:
            self.vely = -self.vely
            for ladrillo in ladrillos_hit:
                self.game.puntos += 10
                Ladrillo.destruir()
            print(f"Ladrillos restantes: {Ladrillo.restantes()}")
            if Ladrillo.restantes() == 0:
                self.game.nivel_superado = True

    def check_colisiones(self, bate_rect):
        veloc_x = abs(self.velx) + 2
        veloc_y = abs(self.vely) + 2

        impactos = pygame.sprite.groupcollide(self.game.lista_ladrillos, self.game.lista_pelotas, True, False)
        for impacto in impactos:
            if self.velx > 0:
                if self.rect.right > impacto.rect.left and self.rect.right < impacto.rect.left + veloc_x:
                    self.velx = -self.velx 
                    return True
                else:
                    self.vely = -self.vely 
                    return True
            if self.velx < 0:
                if self.rect.left < impacto.rect.right and self.rect.left > impacto.rect.right - veloc_x:
                    self.velx = -self.velx 
                    return True
                else:
                    self.vely = -self.vely 
                    return True
        return False
