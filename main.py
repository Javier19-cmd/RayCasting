import pygame
from OpenGL.GL import *

pygame.init()

screen = pygame.display.set_mode(
    (800, 600),
    pygame.OPENGL | pygame.DOUBLEBUF
)

x = 0
y = 10

glClearColor(0.0, 0.1, 0.0, 0.1)


def pixel(x, y, color):
    glEnable(GL_SCISSOR_TEST)
    glScissor(x, y, 10, 10)
    glClearColor(color[0], color[1], color[2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)


x = 0
speed = 1

running = True
while running:

    # clear
    glClearColor(0.1, 0.8, 0.2, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # paint
    pixel(x, 100, (1.0, 0.0, 0.0))
    x += speed

    if x == 800:
        speed = -1
    if x == 0:
        speed = 1

    # flip
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False