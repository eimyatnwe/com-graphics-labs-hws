import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

hull_vertices = [
    
    (-1.8, -0.6, -1.2),  
    (1.8, -0.6, -1.2),   
    (1.8, -0.6, 1.2),    
    (-1.8, -0.6, 1.2),   
   
    (-1.4, 0.5, -1.0),   
    (1.4, 0.5, -1.0),    
    (1.4, 0.5, 1.0),     
    (-1.4, 0.5, 1.0)     
]

hull_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0), 
    (4, 5), (5, 6), (6, 7), (7, 4),  
    (0, 4), (1, 5), (2, 6), (3, 7)   
]

turret_vertices = [
  
    (-0.9, 0.5, -0.7),   
    (0.9, 0.5, -0.7),    
    (0.9, 0.5, 0.7),    
    (-0.9, 0.5, 0.7),    

    (-0.9, 1.3, -0.7),   
    (0.9, 1.3, -0.7),    
    (0.9, 1.3, 0.7),     
    (-0.9, 1.3, 0.7)     
]

turret_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

barrel_vertices = [
    (-0.12, 0.85, -0.7),   
    (0.12, 0.85, -0.7),   
    (0.12, 1.05, -0.7),    
    (-0.12, 1.05, -0.7),   
    (-0.12, 0.85, -2.5),  
    (0.12, 0.85, -2.5),    
    (0.12, 1.05, -2.5),    
    (-0.12, 1.05, -2.5)    
]

barrel_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]


muzzle_vertices = [
    (-0.18, 0.8, -2.5),    
    (0.18, 0.8, -2.5),     
    (0.18, 1.1, -2.5),     
    (-0.18, 1.1, -2.5),    
    (-0.18, 0.8, -2.7),    
    (0.18, 0.8, -2.7),     
    (0.18, 1.1, -2.7),     
    (-0.18, 1.1, -2.7)     
]

muzzle_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

cupola_vertices = [
    (-0.25, 1.3, 0.2),   
    (0.25, 1.3, 0.2),    
    (0.25, 1.3, 0.5),    
    (-0.25, 1.3, 0.5),   
    (-0.2, 1.6, 0.25),   
    (0.2, 1.6, 0.25),    
    (0.2, 1.6, 0.45),    
    (-0.2, 1.6, 0.45)    
]

cupola_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

left_track_vertices = [
    (-2.2, -0.9, -1.4),  
    (-1.7, -0.9, -1.4),  
    (-1.7, -0.9, 1.4),   
    (-2.2, -0.9, 1.4),   
    (-2.2, -0.5, -1.4),  
    (-1.7, -0.5, -1.4),  
    (-1.7, -0.5, 1.4),   
    (-2.2, -0.5, 1.4)    
]

left_track_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

right_track_vertices = [
    (1.7, -0.9, -1.4),   
    (2.2, -0.9, -1.4),   
    (2.2, -0.9, 1.4),    
    (1.7, -0.9, 1.4),    
    (1.7, -0.5, -1.4),   
    (2.2, -0.5, -1.4),   
    (2.2, -0.5, 1.4),    
    (1.7, -0.5, 1.4)     
]

right_track_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

def draw_component(vertices, edges):
    glBegin(GL_LINES)
    for edge in edges:
        glVertex3fv(vertices[edge[0]])
        glVertex3fv(vertices[edge[1]])
    glEnd()

def draw_tank():
    glColor3f(0.3, 0.5, 0.2)
    draw_component(hull_vertices, hull_edges)
    
    glColor3f(0.3, 0.3, 0.3)
    draw_component(left_track_vertices, left_track_edges)
    draw_component(right_track_vertices, right_track_edges)
    
    glColor3f(0.4, 0.6, 0.3)
    draw_component(turret_vertices, turret_edges)
    
    glColor3f(0.6, 0.6, 0.65)
    draw_component(barrel_vertices, barrel_edges)
    
    glColor3f(0.5, 0.5, 0.5)
    draw_component(muzzle_vertices, muzzle_edges)
    
    glColor3f(0.7, 0.6, 0.4)
    draw_component(cupola_vertices, cupola_edges)
    
def main():
    pygame.init()
    display = (1000, 750)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Homework 1 : Tank")
    
    glClearColor(0.05, 0.05, 0.15, 1.0)
    glEnable(GL_DEPTH_TEST)
    glLineWidth(1.5) 
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, display[0] / display[1], 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    
    angle = 0.0
    tilt = 20

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        glTranslatef(0.0, -0.3, -7.5)
        glRotatef(tilt, 1.0, 0.0, 0.0)
        glRotatef(angle, 0.0, 1.0, 0.0)
        
        draw_tank()
        
        pygame.display.flip()
        
        angle += 0.4
        if angle >= 360:
            angle -= 360
        
        pygame.time.wait(10)
    
    pygame.quit()

if __name__ == "__main__":
    main()