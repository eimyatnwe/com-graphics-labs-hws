import sys
import math
import pygame
from pygame.locals import *

# Window size
WIDTH, HEIGHT = 800, 600

# Sphere parameters
SPHERE_CENTER = (0.0, 0.0, 0.0)
SPHERE_RADIUS = 1.0

# Camera (same as Part 1)
EYE = (0.0, 0.5, -4.0)
FOV_Y = 60.0


def normalize(v):
    length = math.sqrt(sum(x * x for x in v))
    return tuple(x / length for x in v)


def dot(a, b):
    return sum(a[i] * b[i] for i in range(3))


def add(a, b):
    return tuple(a[i] + b[i] for i in range(3))


def sub(a, b):
    return tuple(a[i] - b[i] for i in range(3))


def mul(v, s):
    return tuple(v[i] * s for i in range(3))


def ray_sphere_intersect(e, d, c, r):
    # Solve ||(e + t d) - c||^2 = r^2
    oc = sub(e, c)

    a = dot(d, d)
    b = 2.0 * dot(oc, d)
    c_val = dot(oc, oc) - r * r

    disc = b * b - 4 * a * c_val
    if disc < 0:
        return None

    sqrt_disc = math.sqrt(disc)
    t1 = (-b - sqrt_disc) / (2 * a)
    t2 = (-b + sqrt_disc) / (2 * a)

    t_min = float("inf")
    if t1 > 0:
        t_min = t1
    if 0 < t2 < t_min:
        t_min = t2

    if t_min == float("inf"):
        return None

    return t_min


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ray–Sphere Intersection (Part 2)")

    clock = pygame.time.Clock()

    aspect = WIDTH / HEIGHT
    scale = math.tan(math.radians(FOV_Y * 0.5))

    # Camera basis
    forward = normalize((0.0, -0.5, 4.0))
    right = normalize((1.0, 0.0, 0.0))
    up = normalize((0.0, 1.0, 0.0))

    # Light (same idea as OpenGL light)
    light_pos = (-5.0, 5.0, -5.0)
    light_color = (1.0, 1.0, 1.0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        for y in range(HEIGHT):
            for x in range(WIDTH):
                # NDC
                ndc_x = (2 * (x + 0.5) / WIDTH - 1) * aspect
                ndc_y = 1 - 2 * (y + 0.5) / HEIGHT

                # Image plane
                px = ndc_x * scale
                py = ndc_y * scale

                # Ray direction
                d = normalize((
                    forward[0] + px * right[0] + py * up[0],
                    forward[1] + px * right[1] + py * up[1],
                    forward[2] + px * right[2] + py * up[2],
                ))

                t = ray_sphere_intersect(EYE, d, SPHERE_CENTER, SPHERE_RADIUS)

                if t is not None:
                    # Intersection point
                    p = add(EYE, mul(d, t))

                    # Normal
                    n = normalize(sub(p, SPHERE_CENTER))

                    # Lighting (diffuse + specular)
                    l = normalize(sub(light_pos, p))
                    v = normalize(sub(EYE, p))
                    h = normalize(add(l, v))

                    diff = max(dot(n, l), 0.0)
                    spec = pow(max(dot(n, h), 0.0), 50)

                    r = min(255, int((diff + 0.6 * spec) * 255))
                    color = (r, 0, 0)
                else:
                    color = (64, 64, 64)

                screen.set_at((x, y), color)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()