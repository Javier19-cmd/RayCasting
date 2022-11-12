import random
from math import *

import pygame
from OpenGL.GL import *

BLACK = (0, 0, 0)
WHITE = (200, 210, 220)
RED = (255, 0, 0)
SKY = (0, 100, 200)
GROUND = (0, 100, 0)
TRANSPARENT = (152, 0, 136, 255)

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

#Texturas de los enemigos.
sprite1 = pygame.image.load("sprite1.png")
sprite2 = pygame.image.load("sprite2.png")
sprite3 = pygame.image.load("sprite3.png")
sprite4 = pygame.image.load("sprite4.png")

enemies = [
    {
        "x": 150,
        "y": 150,
        "sprite": sprite1,
    },
    {
        "x": 300,
        "y": 300,
        "sprite": sprite2,
    },
] #Lista de enemigos.

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
        self.clearZ() #Limpia el buffer de profundidad.
    
    def clearZ(self):
        self.zbuffer = [99999 for z in range(0, self.w)] #Buffer de profundidad.

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
        for i in range(x, x + self.blocksize):
            for j in range(y, y + self.blocksize):
                tx = int((i - x) * 128 / self.blocksize)
                ty = int((j - y) * 128 / self.blocksize)
                #print(tx, ty)
                c = wall.get_at((tx, ty))
                self.point(i, j, c)

    def load_map(self, filename): #Carga el mapa.
        with open(filename) as f: #Abre el archivo.
            for line in f.readlines(): #Lee cada linea del archivo.
                self.map.append(list(line))
        #print(self.map)

    def draw_stake(self, x, h, c, tx): #Dibuja un stake.
        start_y = int(self.h/2 - h/2)
        end_y = int(self.h/2 + h/2)
        height = end_y - start_y

        for y in range(start_y, end_y): #Dibuja el stake.
            ty = int((y - start_y) * 128 / height) #Posicion en y de la textura.

            color = walls[c].get_at((tx, ty))
            
            self.point(x, y, color) #Dibuja la pared.d

    def cast_ray(self, a): #Castea un rayo.
        d = 0 #Contador.
        ox = self.player["x"] #Posicion en x del jugador. Origen en x.
        oy = self.player["y"] #Posicion en y del jugador. Origen en y.
        
        while True: 
            x = int(ox + d * cos(a)) #Posicion en x del rayo.
            y = int(oy + d * sin(a)) #Posicion en y del rayo.

            i = int(x/self.blocksize) #Posicion en x del mapa.
            j = int(y/self.blocksize) #Posicion en y del mapa.

            if self.map[j][i] != ' ': #Si el bloque no es un espacio.
                hitx = x - i * self.blocksize #Posicion en x del bloque.
                hity = y - j * self.blocksize #Posicion en y del bloque.

                if 1 < hitx < self.blocksize - 1: #Si la posicion en x del bloque esta entre 1 y el tamaño del bloque - 1.
                    maxhit = hitx #Maximo de hit en x.
                else:  
                    maxhit = hity #Maximo de hit en y.

                tx = int(maxhit * 128 / self.blocksize) #Posicion en x de la textura.
                
                return d, self.map[j][i], tx

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

    def draw_enemies(self, sprite): #Dibuja a los enemigos.
        sprite_a = atan2(
            sprite["y"] - self.player["y"],
            sprite["x"] - self.player["x"]
        )

        d = (
            (self.player["x"] - sprite["x"]) ** 2 
            + 
            (self.player["y"] - sprite["y"]) ** 2
        )**0.5

        sprite_size = int(500/d * (500/10))

        sprite_x = int(
            500 #Offset del mapa.
            + 
            (sprite_a - self.player["a"]) * 500/self.player["fov"] # Angulo del enemigo y del jugador.
            + 
            sprite_size/2
        )
        
        sprite_y = int(500/2 - sprite_size/2) #Posicion en y del enemigo. Mitad de la pantalla menos el tamaño del enemigo.

        #Dibujando el sprite.
        for x in range (sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                tx = int((x - sprite_x) * 128 / sprite_size)
                ty = int((y - sprite_y) * 128 / sprite_size)

                color = sprite["sprite"].get_at((tx, ty)) #Color del sprite.

                if color != TRANSPARENT: #Si el color no es transparente, entonces se dibuja el sprite.
                    if x > 500: #Si la posicion en x del sprite es menor a 500, entonces se dibuja el sprite.
                        if self.zbuffer[x - 500] >= d: #Si el zbuffer es igual a la distancia, entonces se dibuja el sprite.
                            self.point(x, y, color)
                            self.zbuffer[x - 500] = d 

    def render(self): #Dibuja el mapa.
        self.draw_map() #Dibuja el mini mapa.
        self.draw_player()

        density = 100 #Densidad de rayos.
        #Minimapa.
        for i in range(0, density):
            a = self.player["a"] - self.player["fov"]/2 + self.player["fov"] * i/density 
            d, c, tx = self.cast_ray(a)

        #Línea.
        for i in range(0, 500):
            self.point(499, i)
            self.point(500, i)
            self.point(501, i)
            #Dibujar en 3D.
        
        #Pared.
        for i in range(0, int(self.w/2)): #Sirve para dibujar las paredes.
            a = self.player["a"] - self.player["fov"]/2 + self.player["fov"] * i/(int(self.w/2)) 
            d, c, tx = self.cast_ray(a)

            x = int(self.w/2) + i #Largo de la pared.
            
            try: #Si d * cos(a - self.player["a"]) no es 0, entonces el personaje está dentro de la escena.

                h = self.h/(d * cos(a - self.player["a"])) * 100
            
            except: #Si d * cos(a - self.player["a"]) es cero, entonces el personaje se sale de la escena.
            
                #Detener al personaje.
                h = 0

            if self.zbuffer[i] >= d:
                self.draw_stake(x, h, c, tx) #Dibuja la pared.
                self.zbuffer[i] = d

        # for enemy in enemies:
        #     self.point(enemy["x"], enemy["y"], (255, 0, 0))

        #Dibujando a los enemigos.
        for enemy in enemies:
            #print(enemy)
            self.draw_enemies(enemy)

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
    r.clearZ()
    r.render() #Dibujando el mapa.
    pygame.display.flip() #Actualiza la pantalla.

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT: #Si se presiona la tecla derecha.
                r.player["x"] -= 20
            if event.key == pygame.K_LEFT: #Si se presiona la tecla izquierda.
                r.player["x"] += 20
            if event.key == pygame.K_UP: #Si se presiona la tecla arriba.
                r.player["y"] += 20
            if event.key == pygame.K_DOWN: #Si se presiona la tecla abajo.
                r.player["y"] -= 20

            if event.key == pygame.K_a: #Si se presiona la tecla a.
                r.player["a"] -= pi/25
            
            if event.key == pygame.K_d: #Si se presiona la tecla d.
                r.player["a"] += pi/25

            #Esto me lo inventé yo.
            if event.key == pygame.K_w: #Si se presiona la tecla w.
                r.player["y"] += int(20 * sin(r.player["a"]))
                r.player["x"] += int(20 * cos(r.player["a"]))
            
            if event.key == pygame.K_s: #Si se presiona la tecla s.
                r.player["y"] -= int(20 * sin(r.player["a"]))
                r.player["x"] -= int(20 * cos(r.player["a"]))