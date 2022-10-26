import path
from OpenGL.GL import *

print(path.__file__)

pygame.init()


screen = pygame.display.set_mode(
    (640, 480),
    pygame.OPENGL | pygame.DOUBLEBUF
    )

x = 0
speed = 1

def pixel(x, y, color):
    glEnable(GL_SCISSOR_TEST)
    glScissor(x, y, 100, 100)
    glClearColor(1.0, 0.0, 0.0, 1.0)
    glClear(color[0], color[1], color[2], 1.0)
    glDisable(GL_SCISSOR_TEST)

while True:

    #Clear.
    glClearColor(0.1, 0.8, 0.2, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    #Paint.

    # screen.set_at((x, y), (255, 255, 255))
    x += 1
    pixel(x, 100, (1.0, 0.0, 0.0))
    
    if x == 800:
        x = -1
    if x == 0:
        speed = 1

    #Flip.
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()