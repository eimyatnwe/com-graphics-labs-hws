# lab02_03.py
# Keyboard-controlled camera: WASD move, arrow keys rotate

import sys
import math
import pygame
from pygame.locals import (
    DOUBLEBUF, OPENGL, QUIT, K_ESCAPE,
    K_w, K_s, K_a, K_d,
    K_UP, K_DOWN, K_LEFT, K_RIGHT
)
from OpenGL.GL import *
from OpenGL.GLU import *


def init_pygame_opengl(width=800, height=600, title="Lab02_03 - Camera / Cockpit View"):
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


def draw_grid(size=10, step=1):
    glColor3f(0.4, 0.4, 0.4)
    glBegin(GL_LINES)
    for i in range(-size, size + 1, step):
        glVertex3f(-size, 0, i)
        glVertex3f(size, 0, i)
        glVertex3f(i, 0, -size)
        glVertex3f(i, 0, size)
    glEnd()


def draw_axes(length=1.5):
    glBegin(GL_LINES)
    # X
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(length, 0, 0)
    # Y
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, length, 0)
    # Z
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, length)
    glEnd()


def draw_cube_wire(size=1.0):
    s = size / 2.0
    vertices = [
        (-s, -s, -s), (s, -s, -s),
        (s,  s, -s), (-s,  s, -s),
        (-s, -s,  s), (s, -s,  s),
        (s,  s,  s), (-s,  s,  s),
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


def main():
    init_pygame_opengl()
    clock = pygame.time.Clock()
    running = True

    # camera position & orientation
    cam_x, cam_y, cam_z = 0.0, 2.0, 8.0
    cam_yaw = 0.0      # rotate left/right (horizontal)
    cam_pitch = 10.0   # look up/down

    move_speed = 5.0   # movement units per second
    turn_speed = 60.0  # degrees per second

    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            running = False

        # --- ROTATION: arrow keys ---
        if keys[K_LEFT]:
            cam_yaw += turn_speed * dt
        if keys[K_RIGHT]:
            cam_yaw -= turn_speed * dt
        if keys[K_UP]:
            cam_pitch += turn_speed * dt
        if keys[K_DOWN]:
            cam_pitch -= turn_speed * dt

        # clamp pitch so we don't flip
        cam_pitch = max(-80.0, min(80.0, cam_pitch))

        # --- MOVEMENT: WASD ---
        # forward/back relative to where camera faces
        forward = 0.0
        strafe = 0.0

        if keys[K_w]:
            forward += 1.0
        if keys[K_s]:
            forward -= 1.0
        if keys[K_d]:
            strafe += 1.0
        if keys[K_a]:
            strafe -= 1.0

        if forward != 0.0 or strafe != 0.0:
            # direction based on yaw (horizontal angle)
            rad_yaw = math.radians(cam_yaw)

            # forward vector in XZ plane
            fwd_x = math.sin(rad_yaw)
            fwd_z = math.cos(rad_yaw)

            # right vector (perpendicular to forward)
            right_x = math.cos(rad_yaw)
            right_z = -math.sin(rad_yaw)

            move_x = (fwd_x * forward + right_x * strafe) * move_speed * dt
            move_z = (fwd_z * forward + right_z * strafe) * move_speed * dt

            cam_x += move_x
            cam_z += move_z

        # --- RENDER ---
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # compute direction vector from yaw + pitch
        rad_yaw = math.radians(cam_yaw)
        rad_pitch = math.radians(cam_pitch)
        dir_x = math.sin(rad_yaw) * math.cos(rad_pitch)
        dir_y = math.sin(rad_pitch)
        dir_z = math.cos(rad_yaw) * math.cos(rad_pitch)

        target_x = cam_x + dir_x
        target_y = cam_y + dir_y
        target_z = cam_z + dir_z

        gluLookAt(cam_x, cam_y, cam_z,
                  target_x, target_y, target_z,
                  0, 1, 0)

        # Scene
        draw_grid(10, 1)
        draw_axes(1.5)

        glColor3f(1, 0, 0)
        glPushMatrix()
        glTranslatef(0, 0.5, 0)
        draw_cube_wire(1.0)
        glPopMatrix()

        glColor3f(0, 1, 0)
        glPushMatrix()
        glTranslatef(3, 0.5, -2)
        draw_cube_wire(1.0)
        glPopMatrix()

        glColor3f(0, 0, 1)
        glPushMatrix()
        glTranslatef(-2, 0.5, 3)
        draw_cube_wire(1.0)
        glPopMatrix()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()