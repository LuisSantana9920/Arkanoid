import pygame
import random
from ball import Ball
from bate import Bate
from ladrillo import Ladrillo
from limites import DibujaLimites

class Game:
    def __init__(self):
        pygame.init()
                
        self.VERDE = (100, 255, 10)
        self.AMARILLO = (240, 220, 10)
        self.AZUL_C = (144, 205, 205)
        self.GRIS = (67, 67, 67)
        self.GRIS2 = (170, 170, 170)
        self.GRIS_C = (120, 120, 120)
        self.TITULO_COLOR = (234, 76, 46)
        self.COLOR_FONDO = (86, 40, 53)

        self.ventana = pygame.display.set_mode((1020, 660))
        pygame.display.flip()

        self.fuente = pygame.font.Font(None, 36)
        self.usar_teclado = self.mostrar_pantalla_inicial()
        self.BLOQUE_SIZEX = 60
        self.BLOQUE_SIZEY = 30
        self.LIMITE_IZQ = 60
        self.LIMITE_DER = 960
        self.LIMITE_UP = 30
        self.LIMITE_BAJO = 660
        self.bola = Ball(self, x=510, y=330)
        self.bate = Bate(self, self.LIMITE_BAJO)
        self.jugando = True

        self.puntos = 0
        self.nivel = 1  # Inicializar nivel aquí
        self.crear_listas_imagenes()
        self.new_nivel() 
        self.programaEjecutandose = True
        self.jugador_dies = False
        self.nivel_superado = False
        self.vidas = 3

    def crear_listas_imagenes(self):
        self.lista_sprites_adibujar = pygame.sprite.Group()
        self.lista_ladrillos = pygame.sprite.Group()
        self.lista_bate = pygame.sprite.Group()
        self.lista_pelotas = pygame.sprite.Group()
        self.lista_particulas = pygame.sprite.Group()

    def vaciar_listas_imagenes(self):
        print("Vaciando listas de imágenes")
        self.lista_sprites_adibujar.empty()
        self.lista_ladrillos.empty()
        self.lista_bate.empty()
        self.lista_pelotas.empty()
        self.lista_particulas.empty()
        print("Listas de imágenes vaciadas")

    def new_nivel(self):
        self.vaciar_listas_imagenes()  # Asegurarse de vaciar las listas antes de iniciar un nuevo nivel
        Ladrillo.reiniciar_contadores()  # Reiniciar contadores de ladrillos
        self.dibujalimites = DibujaLimites(self)
        self.dibujalimites.dibuja_limites()

        print(f"Iniciando nuevo nivel: {self.nivel}")

        if self.nivel == 1: 
            for y in range(3, 7):
                for x in range(3, 14):
                    aleatorio = random.randrange(9) + 1
                    ladrillo = Ladrillo(self, x * self.BLOQUE_SIZEX, y * self.BLOQUE_SIZEY, aleatorio)
                    self.lista_sprites_adibujar.add(ladrillo)
                    self.lista_ladrillos.add(ladrillo)
                    print(f"Ladrillo creado en ({x}, {y}) para nivel 1.")
        elif self.nivel == 2: 
            for y in range(3, 9):
                if y < 5:
                    for x in range(3, 14):
                        aleatorio = random.randrange(9) + 1
                        ladrillo = Ladrillo(self, x * self.BLOQUE_SIZEX, y * self.BLOQUE_SIZEY, aleatorio)
                        self.lista_sprites_adibujar.add(ladrillo)
                        self.lista_ladrillos.add(ladrillo)
                        print(f"Ladrillo creado en ({x}, {y}) para nivel 2.")
                else:
                    start = 3 + (y - 5) 
                    end = 14 - (y - 5)
                    for x in range(start, end):
                        if x == start or x == end - 1:
                            aleatorio = random.randrange(9) + 1
                            ladrillo = Ladrillo(self, x * self.BLOQUE_SIZEX, y * self.BLOQUE_SIZEY, aleatorio)
                            self.lista_sprites_adibujar.add(ladrillo)
                            self.lista_ladrillos.add(ladrillo)
                            print(f"Ladrillo creado en ({x}, {y}) para nivel 2.")
        elif self.nivel == 3: 
            for y in range(2, 10):
                for x in range(2, 15):
                    aleatorio = random.randrange(9) + 1
                    ladrillo = Ladrillo(self, x * self.BLOQUE_SIZEX, y * self.BLOQUE_SIZEY, aleatorio)
                    self.lista_sprites_adibujar.add(ladrillo)
                    self.lista_ladrillos.add(ladrillo)
                    print(f"Ladrillo creado en ({x}, {y}) para nivel 3.")

        print(f'Total ladrillos después de crear el nivel: {Ladrillo.ladrillos_totales}')
        print(f'Ladrillos destruidos: {Ladrillo.ladrillos_destruidos}')
        self.nivel_superado = False  # Restablecer el indicador de nivel superado

    def dibuja_texto(self, surface, texto, size, x, y, qcolor):
        font = pygame.font.SysFont('serif', size)
        text_surface = font.render(texto, True, qcolor)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def mostrar_textos(self):
        centroX = self.ventana.get_width() // 2
        sizeMarcador = self.ventana.get_width() // 40

        if self.programaEjecutandose:
            self.dibuja_texto(self.ventana, f' Puntos: {str(self.puntos)}', sizeMarcador, 150, 10, self.VERDE)
            self.dibuja_texto(self.ventana, f' Nivel: {str(self.nivel)}', sizeMarcador, centroX, 10, self.AMARILLO)
            self.dibuja_texto(self.ventana, f' Vidas: {str(self.vidas)}', sizeMarcador, self.ventana.get_width() - 150, 10, self.AZUL_C)
            self.dibuja_texto(self.ventana, f' Ladrillos restantes: {str(Ladrillo.restantes())}', sizeMarcador, centroX, 50, self.GRIS)

    def mostrar_pantalla_inicial(self):
        self.ventana.fill(self.COLOR_FONDO)
        texto1 = self.fuente.render("ARKANOID", True, (255, 255, 255))
        texto2 = self.fuente.render("Selecciona el método de control:", True, (255, 255, 255))
        texto3 = self.fuente.render("Presiona 'T' para Teclado o 'M' para Mouse", True, (255, 255, 255))
        self.ventana.blit(texto1, (self.ventana.get_width() // 2 - texto1.get_width() // 2, 150))
        self.ventana.blit(texto2, (self.ventana.get_width() // 2 - texto2.get_width() // 2, 200))
        self.ventana.blit(texto3, (self.ventana.get_width() // 2 - texto3.get_width() // 2, 250))
        pygame.display.flip()

        seleccionando = True
        while seleccionando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        return True
                    elif event.key == pygame.K_m:
                        return False

    def mostrar_pantalla_pausa(self):
        self.ventana.fill((0, 0, 0))
        texto1 = self.fuente.render("Juego en pausa", True, (255, 255, 255))
        texto2 = self.fuente.render("Presiona 'C' para continuar o 'Q' para salir", True, (255, 255, 255))
        self.ventana.blit(texto1, (self.ventana.get_width() // 2 - texto1.get_width() // 2, 150))
        self.ventana.blit(texto2, (self.ventana.get_width() // 2 - texto2.get_width() // 2, 200))
        pygame.display.flip()

        pausado = True
        
        while pausado:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        pausado = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        exit()

    def mostrar_menu_game_over(self):
        self.ventana.fill(self.COLOR_FONDO)
        texto1 = self.fuente.render("Game Over", True, (125, 125, 125))
        texto2 = self.fuente.render(f"Tu puntuación: {self.puntos}", True, (255, 255, 255))
        texto3 = self.fuente.render("Presiona 'R' para reiniciar o 'Q' para salir", True, (255, 255, 255))
        self.ventana.blit(texto1, (self.ventana.get_width() // 2 - texto1.get_width() // 2, 150))
        self.ventana.blit(texto2, (self.ventana.get_width() // 2 - texto2.get_width() // 2, 200))
        self.ventana.blit(texto3, (self.ventana.get_width() // 2 - texto3.get_width() // 2, 250))
        pygame.display.flip()

        seleccionando = True
        while seleccionando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.vidas = 3
                        self.bola.rect.x = 510
                        self.bola.rect.y = 330
                        self.bate.reset()
                        self.puntos = 0
                        self.nivel_superado = False
                        self.vaciar_listas_imagenes()
                        self.nivel = 1
                        self.new_nivel()
                        return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        exit()

    def mostrar_pantalla_victoria(self):
        self.ventana.fill(self.COLOR_FONDO)
        texto1 = self.fuente.render("¡Has ganado!", True, (255, 255, 0))
        texto2 = self.fuente.render(f"Tu puntuación: {self.puntos}", True, (255, 255, 255))
        texto3 = self.fuente.render("Presiona 'R' para volver a jugar o 'Q' para salir", True, (255, 255, 255))
        self.ventana.blit(texto1, (self.ventana.get_width() // 2 - texto1.get_width() // 2, 150))
        self.ventana.blit(texto2, (self.ventana.get_width() // 2 - texto2.get_width() // 2, 200))
        self.ventana.blit(texto3, (self.ventana.get_width() // 2 - texto3.get_width() // 2, 250))
        pygame.display.flip()

        seleccionando = True
        while seleccionando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.vidas = 3
                        self.bola.rect.x = 510
                        self.bola.rect.y = 330
                        self.bate.reset()
                        self.puntos = 0
                        self.nivel_superado = False
                        self.vaciar_listas_imagenes()
                        self.nivel = 1
                        self.new_nivel()
                        return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        exit()

    def ejecutar(self):
        while self.jugando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.jugando = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.usar_teclado = not self.usar_teclado
                    elif event.key == pygame.K_SPACE:
                        self.mostrar_pantalla_pausa()
                    elif event.key == pygame.K_n:
                        self.nivel_superado = True
                        self.nivel += 1
                        if self.nivel <= 3:
                            self.new_nivel()
                        else:
                            self.mostrar_pantalla_victoria()

            self.bate.move(self.usar_teclado)
            self.bola.move()
            self.bola.check_colisiones(self.bate.rect)

            if self.bola.rect.bottom > self.LIMITE_BAJO:
                self.vidas -= 1
                print("Vidas restantes:", self.vidas) 
                if self.vidas <= 0:  
                    self.mostrar_menu_game_over()
                else:
                    self.bola.rect.x = 510
                    self.bola.rect.y = 330
                    self.bate.reset()
                    self.lista_sprites_adibujar.remove(self.bate)
                    self.lista_sprites_adibujar.remove(self.bola)
                    self.lista_pelotas.remove(self.bola)
                    self.lista_bate.remove(self.bate)
            else:
                self.ventana.fill((252, 243, 207))
                self.dibujalimites.dibuja_limites()  # Llama al método dibuja_limites
                self.ventana.blit(self.bola.image, self.bola.rect)
                self.ventana.blit(self.bate.image, self.bate.rect)
                self.lista_sprites_adibujar.draw(self.ventana)

            self.mostrar_textos()
            pygame.display.flip()
            pygame.time.Clock().tick(60)

            # Transición al siguiente nivel
            if Ladrillo.restantes() == 0 and not self.nivel_superado:
                self.nivel_superado = True
                self.nivel += 1
                if self.nivel <= 3:
                    self.new_nivel()
                else:
                    self.mostrar_pantalla_victoria()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.ejecutar()
