from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Rotation angles for the cube
rotate_x = 0
rotate_y = 0

# Mouse control variables
mouse_x = 400
mouse_y = 400
first_mouse = True

class Camera:
    """Camera class with position, orientation, and movement capabilities"""
    
    def __init__(self, position=None, yaw=-90.0, pitch=0.0):
        """Initialize camera with position and orientation"""
        # Camera position
        self.position = position if position else [0.0, 0.0, 5.0]
        
        # Euler angles
        self.yaw = yaw      # Horizontal rotation
        self.pitch = pitch  # Vertical rotation
        
        # Camera vectors
        self.front = [0.0, 0.0, -1.0]
        self.up = [0.0, 1.0, 0.0]
        self.right = [1.0, 0.0, 0.0]
        self.world_up = [0.0, 1.0, 0.0]
        
        # Movement speed
        self.movement_speed = 0.1
        self.mouse_sensitivity = 0.1
        
        # Update camera vectors
        self.update_camera_vectors()
    
    def update_camera_vectors(self):
        """Update camera direction vectors based on yaw and pitch"""
        # Calculate new front vector
        front_x = math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        front_y = math.sin(math.radians(self.pitch))
        front_z = math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        
        # Normalize front vector
        length = math.sqrt(front_x**2 + front_y**2 + front_z**2)
        self.front = [front_x/length, front_y/length, front_z/length]
        
        # Calculate right vector (cross product of front and world up)
        right_x = self.front[1] * self.world_up[2] - self.front[2] * self.world_up[1]
        right_y = self.front[2] * self.world_up[0] - self.front[0] * self.world_up[2]
        right_z = self.front[0] * self.world_up[1] - self.front[1] * self.world_up[0]
        
        # Normalize right vector
        length = math.sqrt(right_x**2 + right_y**2 + right_z**2)
        self.right = [right_x/length, right_y/length, right_z/length]
        
        # Calculate up vector (cross product of right and front)
        up_x = self.right[1] * self.front[2] - self.right[2] * self.front[1]
        up_y = self.right[2] * self.front[0] - self.right[0] * self.front[2]
        up_z = self.right[0] * self.front[1] - self.right[1] * self.front[0]
        
        # Normalize up vector
        length = math.sqrt(up_x**2 + up_y**2 + up_z**2)
        self.up = [up_x/length, up_y/length, up_z/length]
    
    def move_forward(self):
        """Move camera forward relative to its orientation"""
        self.position[0] += self.front[0] * self.movement_speed
        self.position[1] += self.front[1] * self.movement_speed
        self.position[2] += self.front[2] * self.movement_speed
    
    def move_backward(self):
        """Move camera backward relative to its orientation"""
        self.position[0] -= self.front[0] * self.movement_speed
        self.position[1] -= self.front[1] * self.movement_speed
        self.position[2] -= self.front[2] * self.movement_speed
    
    def move_left(self):
        """Move camera left relative to its orientation"""
        self.position[0] -= self.right[0] * self.movement_speed
        self.position[1] -= self.right[1] * self.movement_speed
        self.position[2] -= self.right[2] * self.movement_speed
    
    def move_right(self):
        """Move camera right relative to its orientation"""
        self.position[0] += self.right[0] * self.movement_speed
        self.position[1] += self.right[1] * self.movement_speed
        self.position[2] += self.right[2] * self.movement_speed
    
    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        """Process mouse movement for yaw and pitch rotation"""
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity
        
        self.yaw += xoffset
        self.pitch += yoffset
        
        # Constrain pitch to avoid screen flip
        if constrain_pitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0
        
        # Update camera vectors
        self.update_camera_vectors()
    
    def get_view_matrix(self):
        """Return camera position and look-at point for gluLookAt"""
        # Calculate look-at point (position + front)
        center_x = self.position[0] + self.front[0]
        center_y = self.position[1] + self.front[1]
        center_z = self.position[2] + self.front[2]
        
        return (self.position[0], self.position[1], self.position[2],
                center_x, center_y, center_z,
                self.up[0], self.up[1], self.up[2])

# Create camera instance
camera = Camera(position=[3.0, 2.0, 5.0], yaw=-120.0, pitch=-15.0)


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
    glNormal3f(1.0, 0.0, 0.0)
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    
    # Left face - Cyan
    glNormal3f(-1.0, 0.0, 0.0)
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
    
    # Apply camera transformation using gluLookAt
    view_params = camera.get_view_matrix()
    gluLookAt(*view_params)
    
    # Draw the cube
    draw_cube()
    
    glutSwapBuffers()

def keyboard(key, x, y):
    """Keyboard callback for camera movement"""
    global camera
    
    if key == b'w':
        camera.move_forward()
    elif key == b's':
        camera.move_backward()
    elif key == b'a':
        camera.move_left()
    elif key == b'd':
        camera.move_right()
    elif key == b'q' or key == b'\x1b':  # q or ESC to quit
        exit(0)
    
    glutPostRedisplay()

def mouse_motion(x, y):
    """Mouse motion callback for camera rotation"""
    global camera, mouse_x, mouse_y, first_mouse
    
    if first_mouse:
        mouse_x = x
        mouse_y = y
        first_mouse = False
    
    # Calculate offset
    xoffset = x - mouse_x
    yoffset = mouse_y - y  # Reversed since y-coordinates range from bottom to top
    
    mouse_x = x
    mouse_y = y
    
    # Process mouse movement
    camera.process_mouse_movement(xoffset, yoffset)
    
    glutPostRedisplay()

def init():
    """Initialize OpenGL settings"""
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # Set up light position
    light_position = [5.0, 5.0, 5.0, 1.0]
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
    glutCreateWindow(b"3D Cube with Camera Control")
    
    init()
    
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutPassiveMotionFunc(mouse_motion)  # Mouse movement for camera rotation
    
    print("Controls:")
    print("W - Move forward")
    print("S - Move backward")
    print("A - Move left")
    print("D - Move right")
    print("Mouse - Look around (yaw and pitch)")
    print("Q/ESC - Quit")
    
    glutMainLoop()

if __name__ == "__main__":
    main()