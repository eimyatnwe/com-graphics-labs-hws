import sys
import pygame
from pygame.locals import DOUBLEBUF, OPENGL, QUIT, K_ESCAPE
from OpenGL.GL import *
from OpenGL.GLU import *


def init_pygame_opengl(width=800, height=600, title="Lab02_01 - Basic Objects"):
    pygame.init()
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption(title)

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, width / float(height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)


def draw_axes(length=1.5):
    glBegin(GL_LINES)
    # X axis (red)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(length, 0.0, 0.0)
    # Y axis (green)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, length, 0.0)
    # Z axis (blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, length)
    glEnd()


def draw_grid(size=5, step=1):
    glColor3f(0.4, 0.4, 0.4)
    glBegin(GL_LINES)
    for i in range(-size, size + 1, step):
        # lines parallel to X axis
        glVertex3f(-size, 0, i)
        glVertex3f(size, 0, i)
        # lines parallel to Z axis
        glVertex3f(i, 0, -size)
        glVertex3f(i, 0, size)
    glEnd()


def draw_cube_wire(size=1.0):
    s = size / 2.0
    vertices = [
        (-s, -s, -s), (s, -s, -s),
        (s, s, -s), (-s, s, -s),
        (-s, -s, s), (s, -s, s),
        (s, s, s), (-s, s, s),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    ]
    glBegin(GL_LINES)
    for e in edges:
        for idx in e:
            glVertex3fv(vertices[idx])
    glEnd()

def draw_pyramid_wire(size=1.0, height=1.0):
    s = size / 2.0
    # 4 base corners (square in XZ plane)
    v0 = (-s, 0.0, -s)
    v1 = ( s, 0.0, -s)
    v2 = ( s, 0.0,  s)
    v3 = (-s, 0.0,  s)
    # top point
    top = (0.0, height, 0.0)

    glBegin(GL_LINES)
    # base square
    glVertex3fv(v0); glVertex3fv(v1)
    glVertex3fv(v1); glVertex3fv(v2)
    glVertex3fv(v2); glVertex3fv(v3)
    glVertex3fv(v3); glVertex3fv(v0)
    # sides
    glVertex3fv(v0); glVertex3fv(top)
    glVertex3fv(v1); glVertex3fv(top)
    glVertex3fv(v2); glVertex3fv(top)
    glVertex3fv(v3); glVertex3fv(top)
    glEnd()


def main():
    init_pygame_opengl()

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000.0  # not used, but kept for consistency

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        # simple fixed camera
        gluLookAt(3, 3, 6, 0, 0, 0, 0, 1, 0)

        draw_grid(5, 1)
        draw_axes(1.5)

        # cube in the middle
        glPushMatrix()
        glTranslatef(0, 0.5, 0)
        glColor3f(1.0, 1.0, 0.0)
        draw_cube_wire(1.0)
        glPopMatrix()

        # "tank body" as a stretched cube
        glPushMatrix()
        glTranslatef(2, 0.5, 0)
        glScalef(1.5, 0.5, 1.0)
        glColor3f(0.0, 1.0, 1.0)
        draw_cube_wire(1.0)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-2, 0.0, 0.0)
        glColor3f(1.0, 0.3, 1.0)
        draw_pyramid_wire(size=1.0, height=1.2)
        glPopMatrix()
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()