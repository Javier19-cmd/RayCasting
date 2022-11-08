from math import *
import pygame
import random
from OpenGL.GL import *

BLACK = (0, 0, 0)
WHITE = (200, 210, 220)
RED = (255, 0, 0)
SKY = (0, 100, 200)
GROUND = (0, 100, 0)

colors = [
    (0, 20, 10),
    (4, 40, 63),
    (0, 91, 82),
    (219, 242, 38),
    (21, 42, 138),
]

#Texturas de paredes.
walls = {
    "1": pygame.image.load("wall1.png"),
    "2": pygame.image.load("wall2.png"),
    "3": pygame.image.load("wall3.png"),
    "4": pygame.image.load("wall4.png"),
    "5": pygame.image.load("wall5.png"),
}

class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen #Pantalla.
        _, _, self.w, self.h = screen.get_rect() #Dimensiones de la pantalla.
        self.blocksize = 50 #Tamaño de los bloques.
        self.map = [] #Mapa.
        self.player = {
            "x": int(self.blocksize + self.blocksize/2), #Posicion en x del jugador.
            "y": int(self.blocksize + self.blocksize/2), #Posicion en y del jugador.
            "fov": int(pi/3), #Campo de vision.
            "a": int(pi/3), #Angulo.
        }

    def point(self, x, y, color = RED): #Dibuja un punto en la pantalla.
        #print(x, y, color)
        #self.pixel(x, y, color)
        self.screen.set_at((x, y), color)

    def pixel(self, x, y, color): #Dibuja un pixel en la pantalla.
        glEnable(GL_SCISSOR_TEST)
        glScissor(x, y, 1, 1)
        glClearColor(color[0], color[1], color[2], 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glDisable(GL_SCISSOR_TEST)

    def block(self, x, y, wall): #Dibuja un bloque en la pantalla.
        for i in range(x, x + self.blocksize + 1):
            for j in range(y, y + self.blocksize + 1):
                tx = (i - x) * 128 / self.blocksize
                ty = (i - y) * 128 / self.blocksize
                c = texture.get_at((tx, ty))
                self.point(i, j, c)

    def load_map(self, filename): #Carga el mapa.
        with open(filename) as f: #Abre el archivo.
            for line in f.readlines(): #Lee cada linea del archivo.
                self.map.append(list(line))
        #print(self.map)

    def draw_stake(self, x, h, c): #Dibuja un stake.
        start_y = int(self.h/2 - h/2)
        end_y = int(self.h/2 + h/2)

        for y in range(start_y, end_y): #Dibuja el stake.
            self.point(x, y, c)

    def cast_ray(self, a): #Castea un rayo.
        d = 0 #Contador.
        ox = self.player["x"] #Posicion en x del jugador. Origen en x.
        oy = self.player["y"] #Posicion en y del jugador. Origen en y.
        
        while True: 
            x = int(ox + d * cos(a)) #Posicion en x del rayo.
            y = int(oy + d * sin(a)) #Posicion en y del rayo.

            i = int(x/self.blocksize) #Posicion en x del mapa.
            j = int(y/self.blocksize) #Posicion en y del mapa.

            if self.map[j][i] != ' ':
                return d, self.map[j][i]

            #print(x, y)
            self.point(x, y) #Dibuja el rayo.
            d += 3 #Aumenta el contador.
    
    def draw_map(self): #Dibuja el mapa.
        for x in range(0, 500, self.blocksize):
            for y in range(0, 500, self.blocksize):

                #Calculando el tamaño del mapa.
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)
                
                if self.map[j][i] != ' ': #Si el bloque no es un espacio.
                    #print(colors[int(self.map[j][i])])
                    self.block(x, y, walls[self.map[j][i]])
    
    def draw_player(self): #Dibuja al jugador.
        #self.block(self.player["x"], self.player["y"], (255, 0, 0))
        self.point(self.player["x"], self.player["y"])

    def render(self): #Dibuja el mapa.
        self.draw_map()
        self.draw_player()

        density = 100 #Densidad de rayos.
        #Minimapa.
        for i in range(0, density):
            a = self.player["a"] - self.player["fov"]/2 + self.player["fov"] * i/density 
            d, c = self.cast_ray(a)

        #Línea.
        for i in range(0, 500):
            self.point(499, i)
            self.point(500, i)
            self.point(501, i)
            #Dibujar en 3D.
        
        #Pared.
        for i in range(0, int(self.w/2)): #Sirve para dibujar las paredes.
            a = self.player["a"] - self.player["fov"]/2 + self.player["fov"] * i/(int(self.w/2)) 
            d, c = self.cast_ray(a) 

            x = int(self.w/2) + i #Largo de la pared.
            h = self.h/(d * cos(a - self.player["a"])) * 100

            self.draw_stake(x, h, colors[int(c)]) #Dibuja la pared.

pygame.init() #Inicializa pygame.
screen = pygame.display.set_mode((1000, 500)) #Crea la pantalla.
r = Raycaster(screen) #Crea el raycaster.
r.load_map("map.txt") #Carga el mapa.

running = True
while running: 
    screen.fill(BLACK, (0, 0, r.w/2, r.h)) #Limpia la pantalla.
    screen.fill(SKY, (r.w/2, 0, r.w, r.h/2)) #Llena el cielo.
    screen.fill(GROUND, (r.w/2, r.h/2, r.w, r.h/2)) #Llena el suelo.
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
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT: #Si se presiona la tecla derecha.
                r.player["x"] += 10
            if event.key == pygame.K_LEFT: #Si se presiona la tecla izquierda.
                r.player["x"] -= 10
            if event.key == pygame.K_UP: #Si se presiona la tecla arriba.
                r.player["y"] -= 10
            if event.key == pygame.K_DOWN: #Si se presiona la tecla abajo.
                r.player["y"] += 10

            if event.key == pygame.K_a: #Si se presiona la tecla a.
                r.player["a"] -= pi/10
            
            if event.key == pygame.K_d: #Si se presiona la tecla d.
                r.player["a"] += pi/10