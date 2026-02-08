from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Rotation angles
rotate_x = 0
rotate_y = 0


def draw_cube():
    """Draw a colorful cube with different colors on each face"""
    glBegin(GL_QUADS)
    
    # Front face - Red
    glNormal3f(0.0, 0.0, 1.0)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    
    # Back face - Green
    glNormal3f(0.0, 0.0, -1.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)
    
    # Top face - Blue
    glNormal3f(0.0, 1.0, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    
    # Bottom face - Yellow
    glNormal3f(0.0, -1.0, 0.0)
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    
    # Right face - Magenta
    glNormal3f(1.0,0.0,0.0)
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    
    # Left face - Cyan
    glNormal3f(-1.0,0.0,0.0)
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    
    glEnd()

def display():
    """Display callback function"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Position camera
    gluLookAt(3, 3, 5, 0, 0, 0, 0, 1, 0)
    
    # Apply rotations
    glRotatef(rotate_x, 1, 0, 0)
    glRotatef(rotate_y, 0, 1, 0)
    
    # Draw the cube
    draw_cube()
    
    glutSwapBuffers()

def keyboard(key, x, y):
    """Keyboard callback for rotation control"""
    global rotate_x, rotate_y
    
    if key == b'w':
        rotate_x += 5
    elif key == b's':
        rotate_x -= 5
    elif key == b'a':
        rotate_y -= 5
    elif key == b'd':
        rotate_y += 5
    elif key == b'q' or key == b'\x1b':  # q or ESC to quit
        exit(0)
    
    glutPostRedisplay()

def init():
    """Initialize OpenGL settings"""
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # Set up light position
    light_position = [2.0, 2.0, 2.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    
    # Set up perspective projection
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1.0, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    """Main function"""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Colorful 3D Cube - Use W/A/S/D to rotate, Q to quit")
    
    init()
    
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    
    print("Controls:")
    print("W - Rotate up")
    print("S - Rotate down")
    print("A - Rotate left")
    print("D - Rotate right")
    print("Q/ESC - Quit")
    
    glutMainLoop()

if __name__ == "__main__":
    main()