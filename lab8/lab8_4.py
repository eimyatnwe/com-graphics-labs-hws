import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import os

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

class OBJModel:
    def __init__(self, filename):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.has_normals = False
        self.has_texcoords = False
        
        self.load(filename)
    
    def load(self, filename):
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found!")
            return
        
        print(f"Loading OBJ file: {filename}")
        
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split()
                if not parts:
                    continue
                
                # Vertex position
                if parts[0] == 'v':
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    self.vertices.append((x, y, z))
                
                # Vertex normal
                elif parts[0] == 'vn':
                    nx, ny, nz = float(parts[1]), float(parts[2]), float(parts[3])
                    self.normals.append((nx, ny, nz))
                    self.has_normals = True
                
                # Texture coordinate
                elif parts[0] == 'vt':
                    u, v = float(parts[1]), float(parts[2])
                    self.texcoords.append((u, v))
                    self.has_texcoords = True
                
                # Face
                elif parts[0] == 'f':
                    face = []
                    for vertex_str in parts[1:]:
                        indices = vertex_str.split('/')
                        
                        v_idx = int(indices[0]) - 1  
                        vt_idx = None
                        vn_idx = None
                        
                        if len(indices) >= 2 and indices[1]:
                            vt_idx = int(indices[1]) - 1
                        
                        if len(indices) >= 3 and indices[2]:
                            vn_idx = int(indices[2]) - 1
                        
                        face.append((v_idx, vt_idx, vn_idx))
                    
                    # Convert quads to triangles
                    if len(face) == 3:
                        self.faces.append(face)
                    elif len(face) == 4:
                        # Split quad into two triangles
                        self.faces.append([face[0], face[1], face[2]])
                        self.faces.append([face[0], face[2], face[3]])
        
        print(f"Loaded: {len(self.vertices)} vertices, {len(self.normals)} normals, {len(self.faces)} faces")
    
    def render(self):
        glBegin(GL_TRIANGLES)
        
        for face in self.faces:
            for v_idx, vt_idx, vn_idx in face:
                # Set normal if available
                if vn_idx is not None and vn_idx < len(self.normals):
                    glNormal3fv(self.normals[vn_idx])
                
                # Set texture coordinate if available
                if vt_idx is not None and vt_idx < len(self.texcoords):
                    glTexCoord2fv(self.texcoords[vt_idx])
                
                # Set vertex position
                if v_idx < len(self.vertices):
                    glVertex3fv(self.vertices[v_idx])
        
        glEnd()

def init_pygame_opengl():
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OBJ Model Viewer - Ice Cream")
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    fov = 60.0
    aspect = WINDOW_WIDTH / WINDOW_HEIGHT
    near = 0.1
    far = 100.0
    gluPerspective(fov, aspect, near, far)
    
    glMatrixMode(GL_MODELVIEW)
    
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # Set up light
    light_position = [5.0, 5.0, 5.0, 1.0]
    light_ambient = [0.3, 0.3, 0.3, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    
    # Set background color
    glClearColor(0.1, 0.1, 0.15, 1.0)
    
    # Enable smooth shading
    glShadeModel(GL_SMOOTH)

def main():
    init_pygame_opengl()
    clock = pygame.time.Clock()
    
    # Load the OBJ model
    obj_file = "icecream.obj"
    model = OBJModel(obj_file)
    
    if not model.vertices:
        print("Error: No vertices loaded. Exiting.")
        pygame.quit()
        return
    
    # Animation and camera variables
    rotation_y = 0.0
    rotation_speed = 1.0
    camera_distance = 8.0
    auto_rotate = True
    
    print("\n" + "=" * 60)
    print("OBJ Model Viewer - Controls:")
    print("=" * 60)
    print("  ESC          - Exit")
    print("  R            - Reset rotation")
    print("  SPACE        - Toggle auto-rotation")
    print("  Arrow Up/Down - Zoom in/out")
    print("  +/-          - Increase/decrease rotation speed")
    print("  Mouse Wheel  - Zoom in/out")
    print("=" * 60)
    
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                
                elif event.key == K_r:
                    # Reset rotation
                    rotation_y = 0.0
                    print("Rotation reset")
                
                elif event.key == K_SPACE:
                    # Toggle auto-rotation
                    auto_rotate = not auto_rotate
                    print(f"Auto-rotation: {'ON' if auto_rotate else 'OFF'}")
                
                elif event.key == K_UP:
                    # Zoom in
                    camera_distance = max(2.0, camera_distance - 0.5)
                
                elif event.key == K_DOWN:
                    # Zoom out
                    camera_distance = min(50.0, camera_distance + 0.5)
                
                elif event.key == K_PLUS or event.key == K_EQUALS:
                    # Increase rotation speed
                    rotation_speed += 0.2
                    print(f"Rotation speed: {rotation_speed:.1f}")
                
                elif event.key == K_MINUS:
                    # Decrease rotation speed
                    rotation_speed = max(0.1, rotation_speed - 0.2)
                    print(f"Rotation speed: {rotation_speed:.1f}")
            
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 4: 
                    camera_distance = max(2.0, camera_distance - 0.5)
                elif event.button == 5: 
                    camera_distance = min(50.0, camera_distance + 0.5)
        
        # Update rotation
        if auto_rotate:
            rotation_y += rotation_speed
            if rotation_y >= 360.0:
                rotation_y -= 360.0
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glLoadIdentity()
        
        # Position camera
        gluLookAt(
            0, 2, camera_distance, 
            0, 2, 0,               
            0, 1, 0                
        )
    
        glPushMatrix()

        glRotatef(rotation_y, 0, 1, 0)  
    
        glColor3f(0.5, 0.45, 0.8) 
    
        model.render()
        
        glPopMatrix()
        
        pygame.display.flip()
      
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()