from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Mouse control variables
mouse_x = 400
mouse_y = 400
first_mouse = True

# Light properties
light_position = [5.0, 5.0, 5.0]  # Light position in world space
light_intensity = 1.0              # Light intensity
kd = 0.8                          # Diffuse reflection coefficient

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

def normalize(v):
    """Normalize a 3D vector"""
    length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if length > 0:
        return [v[0]/length, v[1]/length, v[2]/length]
    return v

def dot(v1, v2):
    """Compute dot product of two 3D vectors"""
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def compute_lambertian_color(position, normal, base_color):
    """
    Compute Lambertian diffuse shading
    Ld = kd × I × max(0, n · l)
    
    Args:
        position: Surface position [x, y, z]
        normal: Surface normal vector [nx, ny, nz]
        base_color: Base color of the surface [r, g, b]
    
    Returns:
        Final color [r, g, b] with Lambertian shading applied
    """
    # Compute light direction vector: l = light_position - surface_position
    light_dir = [
        light_position[0] - position[0],
        light_position[1] - position[1],
        light_position[2] - position[2]
    ]
    
    # Normalize light direction
    l = normalize(light_dir)
    
    # Normalize normal vector (should already be normalized, but ensure it)
    n = normalize(normal)
    
    # Compute dot product: n · l
    n_dot_l = dot(n, l)
    
    # Clamp negative values: max(0, n · l)
    diffuse_factor = max(0.0, n_dot_l)
    
    # Apply Lambertian formula: Ld = kd × I × max(0, n · l)
    intensity = kd * light_intensity * diffuse_factor
    
    # Modulate base color with computed intensity
    final_color = [
        base_color[0] * intensity,
        base_color[1] * intensity,
        base_color[2] * intensity
    ]
    
    return final_color

def draw_cube():
    """Draw a colorful cube with Lambertian diffuse shading"""
    
    # Define vertices of the cube
    vertices = [
        [-1.0, -1.0, -1.0], [1.0, -1.0, -1.0], [1.0, 1.0, -1.0], [-1.0, 1.0, -1.0],  # Back
        [-1.0, -1.0, 1.0], [1.0, -1.0, 1.0], [1.0, 1.0, 1.0], [-1.0, 1.0, 1.0],      # Front
    ]
    
    # Define faces with vertex indices, normals, and base colors
    faces = [
        # Front face - Red
        {
            'indices': [4, 5, 6, 7],
            'normal': [0.0, 0.0, 1.0],
            'color': [1.0, 0.0, 0.0]
        },
        # Back face - Green
        {
            'indices': [0, 3, 2, 1],
            'normal': [0.0, 0.0, -1.0],
            'color': [0.0, 1.0, 0.0]
        },
        # Top face - Blue
        {
            'indices': [3, 7, 6, 2],
            'normal': [0.0, 1.0, 0.0],
            'color': [0.0, 0.0, 1.0]
        },
        # Bottom face - Yellow
        {
            'indices': [0, 1, 5, 4],
            'normal': [0.0, -1.0, 0.0],
            'color': [1.0, 1.0, 0.0]
        },
        # Right face - Magenta
        {
            'indices': [1, 2, 6, 5],
            'normal': [1.0, 0.0, 0.0],
            'color': [1.0, 0.0, 1.0]
        },
        # Left face - Cyan
        {
            'indices': [0, 4, 7, 3],
            'normal': [-1.0, 0.0, 0.0],
            'color': [0.0, 1.0, 1.0]
        }
    ]
    
    glBegin(GL_QUADS)
    
    for face in faces:
        # Get face center for lighting calculation
        face_center = [0.0, 0.0, 0.0]
        for idx in face['indices']:
            face_center[0] += vertices[idx][0]
            face_center[1] += vertices[idx][1]
            face_center[2] += vertices[idx][2]
        face_center[0] /= 4
        face_center[1] /= 4
        face_center[2] /= 4
        
        # Compute Lambertian color for this face
        final_color = compute_lambertian_color(
            face_center,
            face['normal'],
            face['color']
        )
        
        # Set the computed color
        glColor3f(final_color[0], final_color[1], final_color[2])
        
        # Set normal for the face
        glNormal3f(face['normal'][0], face['normal'][1], face['normal'][2])
        
        # Draw vertices
        for idx in face['indices']:
            glVertex3f(vertices[idx][0], vertices[idx][1], vertices[idx][2])
    
    glEnd()

def display():
    """Display callback function"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Apply camera transformation using gluLookAt
    view_params = camera.get_view_matrix()
    gluLookAt(*view_params)
    
    # Draw the cube with Lambertian shading
    draw_cube()
    
    # Draw light position as a small sphere for reference
    glPushMatrix()
    glTranslatef(light_position[0], light_position[1], light_position[2])
    glColor3f(1.0, 1.0, 0.0)  # Yellow color for light
    glutSolidSphere(0.2, 10, 10)
    glPopMatrix()
    
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
    
    # Disable OpenGL's built-in lighting since we're doing manual calculations
    glDisable(GL_LIGHTING)
    
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
    glutCreateWindow(b"Lab 7.1: Lambertian Diffuse Shading")
    
    init()
    
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutPassiveMotionFunc(mouse_motion)
    
    print("=== Lab 7.1: Lambertian Diffuse Shading ===")
    print("Formula: Ld = kd × I × max(0, n · l)")
    print(f"Light Position: {light_position}")
    print(f"Diffuse Coefficient (kd): {kd}")
    print(f"Light Intensity (I): {light_intensity}")
    print("\nControls:")
    print("W - Move forward")
    print("S - Move backward")
    print("A - Move left")
    print("D - Move right")
    print("Mouse - Look around")
    print("Q/ESC - Quit")
    
    glutMainLoop()

if __name__ == "__main__":
    main()