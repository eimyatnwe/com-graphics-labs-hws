from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

current_object = 'cube'

tx, ty, tz = 0.0, 0.0, -5.0
scale_factor = 1.0
rotation_y = 0.0

def multiply_matrix_vector(m, v):
    result = [0, 0, 0, 0]
    for i in range(4):
        result[i] = (
            m[i][0] * v[0] +
            m[i][1] * v[1] +
            m[i][2] * v[2] +
            m[i][3] * v[3]
        )
    return result

def translation_matrix(tx, ty, tz):
    return [
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ]

def scaling_matrix(s):
    return [
        [s, 0, 0, 0],
        [0, s, 0, 0],
        [0, 0, s, 0],
        [0, 0, 0, 1]
    ]

def rotation_y_matrix(angle):
    rad = math.radians(angle)
    return [
        [ math.cos(rad), 0, math.sin(rad), 0],
        [ 0,             1, 0,             0],
        [-math.sin(rad), 0, math.cos(rad), 0],
        [ 0,             0, 0,             1]
    ]

cube_vertices = [
    [-1, -1, -1, 1], [1, -1, -1, 1], [1, 1, -1, 1], [-1, 1, -1, 1],
    [-1, -1,  1, 1], [1, -1,  1, 1], [1, 1,  1, 1], [-1, 1,  1, 1]
]

cube_edges = [
    (0,1),(1,2),(2,3),(3,0),
    (4,5),(5,6),(6,7),(7,4),
    (0,4),(1,5),(2,6),(3,7)
]

pyramid_vertices = [
    [-1, 0, -1, 1], [1, 0, -1, 1],
    [1, 0,  1, 1], [-1, 0,  1, 1],
    [0, 2,  0, 1]
]

pyramid_edges = [
    (0,1),(1,2),(2,3),(3,0),
    (0,4),(1,4),(2,4),(3,4)
]

def generate_sphere(radius=1, stacks=12, slices=12):
    vertices = []
    for i in range(stacks):
        lat = math.pi * (-0.5 + i / stacks)
        for j in range(slices):
            lon = 2 * math.pi * j / slices
            x = radius * math.cos(lat) * math.cos(lon)
            y = radius * math.sin(lat)
            z = radius * math.cos(lat) * math.sin(lon)
            vertices.append([x, y, z, 1])
    return vertices

sphere_vertices = generate_sphere()

def draw_object(vertices, edges=None):
    sm = scaling_matrix(scale_factor)
    rm = rotation_y_matrix(rotation_y)
    tm = translation_matrix(tx, ty, tz)

    transformed = []
    for v in vertices:
        v1 = multiply_matrix_vector(sm, v)
        v2 = multiply_matrix_vector(rm, v1)
        v3 = multiply_matrix_vector(tm, v2)
        transformed.append(v3)

    glBegin(GL_LINES)
    if edges:
        for e in edges:
            for idx in e:
                glVertex3f(
                    transformed[idx][0],
                    transformed[idx][1],
                    transformed[idx][2]
                )
    else:
        for v in transformed:
            glVertex3f(v[0], v[1], v[2])
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1, 1, 1)

    if current_object == 'cube':
        draw_object(cube_vertices, cube_edges)
    elif current_object == 'pyramid':
        draw_object(pyramid_vertices, pyramid_edges)
    elif current_object == 'sphere':
        draw_object(sphere_vertices)

    glutSwapBuffers()


def keyboard(key, x, y):
    global current_object, tx, tz
    key = key.decode('utf-8')

    if key == 'c': current_object = 'cube'
    if key == 'p': current_object = 'pyramid'
    if key == 's': current_object = 'sphere'
    if key == 'w': tz -= 0.2
    if key == 'S': tz += 0.2
    if key == 'a': tx -= 0.2
    if key == 'd': tx += 0.2

    glutPostRedisplay()

def special(key, x, y):
    global scale_factor, rotation_y

    if key == GLUT_KEY_UP: scale_factor += 0.1
    if key == GLUT_KEY_DOWN: scale_factor -= 0.1
    if key == GLUT_KEY_LEFT: rotation_y -= 5
    if key == GLUT_KEY_RIGHT: rotation_y += 5

    glutPostRedisplay()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Manual 3D Transformations Lab")

    glEnable(GL_DEPTH_TEST)
    glClearColor(0, 0, 0, 1)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 100)

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special)
    glutMainLoop()

main()
