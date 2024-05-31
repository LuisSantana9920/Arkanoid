import pygame

class Bate(pygame.sprite.Sprite):
    def __init__(self, game, limite_bajo):
        super().__init__()
        self.game = game
        self.image = pygame.image.load("bate.png")  # Carga la imagen del bate
        self.rect = self.image.get_rect()
        self.rect.midbottom = (game.ventana.get_width() // 2, limite_bajo - 10)

    def move(self, usar_teclado):
        keys = pygame.key.get_pressed()
        if usar_teclado:
            if keys[pygame.K_LEFT] and self.rect.left > self.game.LIMITE_IZQ:
                self.rect.x -= 5
            if keys[pygame.K_RIGHT] and self.rect.right < self.game.LIMITE_DER:
                self.rect.x += 5
        else:
            mouse_x = pygame.mouse.get_pos()[0]
            self.rect.centerx = mouse_x

        if self.rect.left < self.game.LIMITE_IZQ:
            self.rect.left = self.game.LIMITE_IZQ
        if self.rect.right > self.game.LIMITE_DER:
            self.rect.right = self.game.LIMITE_DER

    def reset(self):
        self.rect.midbottom = (self.game.ventana.get_width() // 2, self.game.LIMITE_BAJO - 10)
