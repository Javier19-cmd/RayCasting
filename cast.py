import pygame
import random
from OpenGL.GL import *

BLACK = (0, 0, 0)
WHITE = (200, 210, 220)

class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen #Pantalla.
        _, _, self.w, self.h = screen.get_rect() #Dimensiones de la pantalla.
        self.blocksize = 50 #Tamaño de los bloques.
        self.map = [] #Mapa.

    def point(self, x, y, color = WHITE): #Dibuja un punto en la pantalla.
        #print(x, y, color)
        self.screen.set_at((x, y), color)

    def pixel(self, x, y, color): #Dibuja un pixel en la pantalla.
        glEnable(GL_SCISSOR_TEST)
        glScissor(x, y, 1, 1)
        glClearColor(color[0], color[1], color[2], 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glDisable(GL_SCISSOR_TEST)

    def block(self, x, y, c = WHITE): #Dibuja un bloque en la pantalla.
        for i in range(x, x + self.blocksize + 1):
            for j in range(y, y + self.blocksize + 1):
                self.pixel(i, j, c)

    def load_map(self, filename): #Carga el mapa.
        with open(filename) as f: #Abre el archivo.
            for line in f.readlines(): #Lee cada linea del archivo.
                self.map.append(list(line))
        #print(self.map)
    
    def draw_map(self): #Dibuja el mapa.
        for x in range(0, 500, self.blocksize):
            for y in range(0, 500, self.blocksize):

                #Calculando el tamaño del mapa.
                j = int(x/self.blocksize)
                i = int(y/self.blocksize)
                
                if self.map[j][i] != ' ': #Si el bloque no es un espacio.
                    self.block(x, y)

    def render(self): #Dibuja el mapa.
        self.draw_map()

pygame.init() #Inicializa pygame.
screen = pygame.display.set_mode((500, 500), pygame.OPENGL | pygame.DOUBLEBUF) #Crea la pantalla.
r = Raycaster(screen) #Crea el raycaster.
r.load_map("map.txt") #Carga el mapa.

running = True
while running: 
    # x = random.randint(0, 500) #Genera un número aleatorio entre 0 y 500.
    # y = random.randint(0, 500) #Genera un número aleatorio entre 0 y 500.
    
    #r.pixel(x, y, WHITE) #Dibuja un punto blanco en la pantalla.
    #r.point(x, y) #Dibuja un pixel blanco en la pantalla.
    #r.block(x, y) #Dibuja un bloque blanco en la pantalla.
    r.render() #Dibujando el mapa.
    pygame.display.flip() #Actualiza la pantalla.

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    