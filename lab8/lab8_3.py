import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

def init_pygame_opengl():
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Cubes - Perspective & Depth Buffer Demo")
    
    # Set up perspective projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    # gluPerspective(fov, aspect, near, far)
    fov = 60.0
    aspect = WINDOW_WIDTH / WINDOW_HEIGHT
    near = 0.1
    far = 100.0
    gluPerspective(fov, aspect, near, far)
    
    # Switch to modelview matrix
    glMatrixMode(GL_MODELVIEW)
    
    # Enable depth testing (Z-buffer)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    
    # Set background color (dark gray/black)
    glClearColor(0.1, 0.1, 0.15, 1.0)

def draw_cube():
    vertices = [
        # Front face
        [-1, -1,  1],
        [ 1, -1,  1],
        [ 1,  1,  1],
        [-1,  1,  1],
        # Back face
        [-1, -1, -1],
        [ 1, -1, -1],
        [ 1,  1, -1],
        [-1,  1, -1],
    ]
    
    faces = [
        [0, 1, 2, 3],  # Front
        [4, 5, 6, 7],  # Back
        [0, 3, 7, 4],  # Left
        [1, 2, 6, 5],  # Right
        [3, 2, 6, 7],  # Top
        [0, 1, 5, 4],  # Bottom
    ]
    
    glBegin(GL_QUADS)
    for face in faces:
        for vertex_idx in face:
            glVertex3fv(vertices[vertex_idx])
    glEnd()

def draw_cube_edges():
    vertices = [
        [-1, -1,  1], [ 1, -1,  1], [ 1,  1,  1], [-1,  1,  1],
        [-1, -1, -1], [ 1, -1, -1], [ 1,  1, -1], [-1,  1, -1],
    ]
    
    edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],  # Front face
        [4, 5], [5, 6], [6, 7], [7, 4],  # Back face
        [0, 4], [1, 5], [2, 6], [3, 7],  # Connecting edges
    ]
    
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex_idx in edge:
            glVertex3fv(vertices[vertex_idx])
    glEnd()

def render_cube(x, y, z, scale, color, rotation_angle, rotation_axis):
    glPushMatrix()
    
    # Apply transformations
    glTranslatef(x, y, z)
    glRotatef(rotation_angle, rotation_axis[0], rotation_axis[1], rotation_axis[2])
    glScalef(scale, scale, scale)
    
    # Draw filled cube
    glColor3f(*color)
    draw_cube()
    
    # Draw wireframe edges
    draw_cube_edges()
    
    glPopMatrix()

def main():
    init_pygame_opengl()
    clock = pygame.time.Clock()
    
    # Animation variables
    rotation_angle = 0.0
    oscillation_time = 0.0
    
    print("3D Cubes Demo - Perspective Projection & Depth Buffering")
    print("=" * 60)
    print("Controls:")
    print("  ESC or close window to exit")
    print("\nFeatures:")
    print("  • Perspective projection (FOV=60°)")
    print("  • Z-buffer depth testing")
    print("  • 3 cubes at different depths")
    print("  • Continuous rotation and oscillation animation")
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
        
        # Clear both color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Reset modelview matrix
        glLoadIdentity()
        
        # Camera position: look from a point behind and above
        gluLookAt(
            0, 3, 10,   # Camera position (x, y, z)
            0, 0, 0,    # Look at point (center)
            0, 1, 0     # Up vector
        )
        
        # Update animation variables
        rotation_angle += 1.0  # Degrees per frame
        oscillation_time += 0.05
        
        # Calculate oscillation for moving cube
        oscillation_x = math.sin(oscillation_time) * 2.0
        oscillation_z = math.cos(oscillation_time * 0.5) * 1.5
        
        # CUBE 1: Closest (Red) - Rotating around Y-axis
        # Position: slightly to the left and forward
        render_cube(
            x=-2.0 + oscillation_x * 0.3,
            y=0.0,
            z=-5.0,
            scale=1.2,
            color=(0.9, 0.2, 0.2),  # Red
            rotation_angle=rotation_angle,
            rotation_axis=(0, 1, 0)  # Rotate around Y-axis
        )
        
        # CUBE 2: Mid-distance (Green) - Rotating around multiple axes
        # Position: slightly to the right and mid-depth
        render_cube(
            x=2.0,
            y=0.0,
            z=-10.0 + oscillation_z,
            scale=1.0,
            color=(0.2, 0.9, 0.2),  # Green
            rotation_angle=rotation_angle * 1.5,
            rotation_axis=(1, 1, 0)  # Rotate around diagonal axis
        )
        
        render_cube(
            x=0.0,
            y=-1.0,
            z=-15.0,
            scale=0.8,
            color=(0.2, 0.2, 0.9),  # Blue
            rotation_angle=rotation_angle * 0.7,
            rotation_axis=(1, 0, 0)  # Rotate around X-axis
        )
        
        render_cube(
            x=1.0,
            y=1.5,
            z=-8.0 + oscillation_z * 0.5,
            scale=0.7,
            color=(0.9, 0.9, 0.2),  # Yellow
            rotation_angle=rotation_angle * 2.0,
            rotation_axis=(0, 1, 1)
        )
        
        # Swap buffers (double buffering)
        pygame.display.flip()
        
        # Maintain 60 FPS
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()