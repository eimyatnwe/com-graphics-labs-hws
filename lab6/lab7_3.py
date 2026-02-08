from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

mouse_x = 400
mouse_y = 400
first_mouse = True


light_position = [5.0, 5.0, 5.0]  
light_intensity = 1.0              
kd = 0.8                          
ks = 0.5                          
shininess = 32.0                  
light_move_speed = 0.3           

class Camera:
    
    def __init__(self, position=None, yaw=-90.0, pitch=0.0):
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
        front_x = math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        front_y = math.sin(math.radians(self.pitch))
        front_z = math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        
        length = math.sqrt(front_x**2 + front_y**2 + front_z**2)
        self.front = [front_x/length, front_y/length, front_z/length]
        
        right_x = self.front[1] * self.world_up[2] - self.front[2] * self.world_up[1]
        right_y = self.front[2] * self.world_up[0] - self.front[0] * self.world_up[2]
        right_z = self.front[0] * self.world_up[1] - self.front[1] * self.world_up[0]
        
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
        self.position[0] += self.front[0] * self.movement_speed
        self.position[1] += self.front[1] * self.movement_speed
        self.position[2] += self.front[2] * self.movement_speed
    
    def move_backward(self):
        self.position[0] -= self.front[0] * self.movement_speed
        self.position[1] -= self.front[1] * self.movement_speed
        self.position[2] -= self.front[2] * self.movement_speed
    
    def move_left(self):
        self.position[0] -= self.right[0] * self.movement_speed
        self.position[1] -= self.right[1] * self.movement_speed
        self.position[2] -= self.right[2] * self.movement_speed
    
    def move_right(self):
        self.position[0] += self.right[0] * self.movement_speed
        self.position[1] += self.right[1] * self.movement_speed
        self.position[2] += self.right[2] * self.movement_speed
    
    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
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
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def compute_blinn_phong_color(position, normal, base_color):
    light_dir = [
        light_position[0] - position[0],
        light_position[1] - position[1],
        light_position[2] - position[2]
    ]
    
    # Normalize light direction
    l = normalize(light_dir)
    
    # Normalize normal vector
    n = normalize(normal)
    
    n_dot_l = dot(n, l)
    diffuse_factor = max(0.0, n_dot_l)
    diffuse_intensity = kd * light_intensity * diffuse_factor
    
    # Compute diffuse color
    diffuse_color = [
        base_color[0] * diffuse_intensity,
        base_color[1] * diffuse_intensity,
        base_color[2] * diffuse_intensity
    ]
    
   
    view_dir = [
        camera.position[0] - position[0],
        camera.position[1] - position[1],
        camera.position[2] - position[2]
    ]
    v = normalize(view_dir)
    
    # Compute halfway vector: h = normalize(l + v)
    halfway = [l[0] + v[0], l[1] + v[1], l[2] + v[2]]
    h = normalize(halfway)
    
    # Compute specular term: (n · h)^p
    n_dot_h = dot(n, h)
    
    if diffuse_factor > 0.0 and n_dot_h > 0.0:
        specular_factor = pow(n_dot_h, shininess)
        specular_intensity = ks * light_intensity * specular_factor
    else:
        specular_intensity = 0.0
    
    # Specular highlights are white
    specular_color = [specular_intensity, specular_intensity, specular_intensity]
    
    # Combine diffuse and specular components
    final_color = [
        min(1.0, diffuse_color[0] + specular_color[0]),
        min(1.0, diffuse_color[1] + specular_color[1]),
        min(1.0, diffuse_color[2] + specular_color[2])
    ]
    
    return final_color

def draw_cube():    
    # Define vertices of the cube
    vertices = [
        [-1.0, -1.0, -1.0], [1.0, -1.0, -1.0], [1.0, 1.0, -1.0], [-1.0, 1.0, -1.0],
        [-1.0, -1.0, 1.0], [1.0, -1.0, 1.0], [1.0, 1.0, 1.0], [-1.0, 1.0, 1.0],
    ]
    
    # Define faces with vertex indices, normals, and base colors
    faces = [
        {'indices': [4, 5, 6, 7], 'normal': [0.0, 0.0, 1.0], 'color': [1.0, 0.0, 0.0]},   # Front - Red
        {'indices': [0, 3, 2, 1], 'normal': [0.0, 0.0, -1.0], 'color': [0.0, 1.0, 0.0]},  # Back - Green
        {'indices': [3, 7, 6, 2], 'normal': [0.0, 1.0, 0.0], 'color': [0.0, 0.0, 1.0]},   # Top - Blue
        {'indices': [0, 1, 5, 4], 'normal': [0.0, -1.0, 0.0], 'color': [1.0, 1.0, 0.0]},  # Bottom - Yellow
        {'indices': [1, 2, 6, 5], 'normal': [1.0, 0.0, 0.0], 'color': [1.0, 0.0, 1.0]},   # Right - Magenta
        {'indices': [0, 4, 7, 3], 'normal': [-1.0, 0.0, 0.0], 'color': [0.0, 1.0, 1.0]}   # Left - Cyan
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
        
        # Compute Blinn-Phong color for this face (recalculated every frame)
        final_color = compute_blinn_phong_color(
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

def draw_light_source():
    """Draw a visual representation of the light source"""
    glPushMatrix()
    glTranslatef(light_position[0], light_position[1], light_position[2])
    glColor3f(1.0, 1.0, 0.0)  # Yellow color for light
    glutSolidSphere(0.2, 20, 20)
    glPopMatrix()

def display():
    """Display callback function - recalculates lighting every frame"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Apply camera transformation using gluLookAt
    view_params = camera.get_view_matrix()
    gluLookAt(*view_params)
    
    # Draw the cube with Blinn-Phong shading (recalculated with current light position)
    draw_cube()
    
    # Draw light source position
    draw_light_source()
    
    glutSwapBuffers()

def keyboard(key, x, y):
    """Keyboard callback for camera movement and light control"""
    global camera, shininess, ks, light_position
    
    # Camera controls
    if key == b'w':
        camera.move_forward()
    elif key == b's':
        camera.move_backward()
    elif key == b'a':
        camera.move_left()
    elif key == b'd':
        camera.move_right()
    
    # Light position controls - X axis
    elif key == b'4':
        light_position[0] -= light_move_speed
        print(f"Light Position: [{light_position[0]:.2f}, {light_position[1]:.2f}, {light_position[2]:.2f}]")
    elif key == b'5':
        light_position[0] += light_move_speed
        print(f"Light Position: [{light_position[0]:.2f}, {light_position[1]:.2f}, {light_position[2]:.2f}]")
    
    # Light position controls - Y axis
    elif key == b'8':
        light_position[1] += light_move_speed
        print(f"Light Position: [{light_position[0]:.2f}, {light_position[1]:.2f}, {light_position[2]:.2f}]")
    elif key == b'2':
        light_position[1] -= light_move_speed
        print(f"Light Position: [{light_position[0]:.2f}, {light_position[1]:.2f}, {light_position[2]:.2f}]")
    
    # Light position controls - Z axis
    elif key == b'+' or key == b'=':
        light_position[2] += light_move_speed
        print(f"Light Position: [{light_position[0]:.2f}, {light_position[1]:.2f}, {light_position[2]:.2f}]")
    elif key == b'-' or key == b'_':
        light_position[2] -= light_move_speed
        print(f"Light Position: [{light_position[0]:.2f}, {light_position[1]:.2f}, {light_position[2]:.2f}]")
    
    # Material property controls
    elif key == b'[':
        ks = max(0.0, ks - 0.1)
        print(f"Specular coefficient (ks): {ks:.2f}")
    elif key == b']':
        ks = min(1.0, ks + 0.1)
        print(f"Specular coefficient (ks): {ks:.2f}")
    elif key == b'<' or key == b',':
        shininess = max(1.0, shininess - 4.0)
        print(f"Shininess: {shininess}")
    elif key == b'>' or key == b'.':
        shininess = min(256.0, shininess + 4.0)
        print(f"Shininess: {shininess}")
    
    # Quit
    elif key == b'q' or key == b'\x1b':
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
    yoffset = mouse_y - y
    
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
    glutCreateWindow(b"Lab 7.3: Interactive Light Movement")
    
    init()
    
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutPassiveMotionFunc(mouse_motion)
    
    print("=" * 60)
    print("Lab 7.3: Interactive Light Movement")
    print("=" * 60)
    print("Lighting recalculated every frame with current light position")
    print(f"\nInitial Light Position: {light_position}")
    print(f"Diffuse Coefficient (kd): {kd}")
    print(f"Specular Coefficient (ks): {ks}")
    print(f"Shininess (p): {shininess}")
    print("\n" + "=" * 60)
    print("CAMERA CONTROLS:")
    print("  W/A/S/D - Move camera")
    print("  Mouse   - Look around")
    print("\nLIGHT POSITION CONTROLS:")
    print("  4 / 5   - Move light along X-axis (left/right)")
    print("  8 / 2   - Move light along Y-axis (up/down)")
    print("  + / -   - Move light along Z-axis (forward/backward)")
    print("\nMATERIAL PROPERTY CONTROLS:")
    print("  [ / ]   - Decrease/Increase specular coefficient")
    print("  < / >   - Decrease/Increase shininess")
    print("\nOTHER:")
    print("  Q/ESC   - Quit")
    print("=" * 60)
    
    glutMainLoop()

if __name__ == "__main__":
    main()