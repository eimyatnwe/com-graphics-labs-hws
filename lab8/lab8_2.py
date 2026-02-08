import pygame
import sys

# Initialize Pygame
pygame.init()

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)

# Create window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Triangle Rasterization with Gouraud Shading")

# Triangle vertices (x, y)
A = (200, 120)
B = (120, 420)
C = (520, 380)

# Vertex colors (R, G, B)
CA = (255, 0, 0)    # Red
CB = (0, 255, 0)    # Green
CC = (0, 0, 255)    # Blue

def sign(p1, p2, p3):
    """
    Compute the signed area of triangle formed by three points.
    Used for barycentric coordinate calculation.
    """
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def barycentric_coordinates(p, a, b, c):
    """
    Compute barycentric coordinates (alpha, beta, gamma) for point p
    with respect to triangle (a, b, c).
    
    Returns (alpha, beta, gamma) where:
    - alpha is the weight for vertex a
    - beta is the weight for vertex b
    - gamma is the weight for vertex c
    - alpha + beta + gamma = 1
    """
    # Calculate the area of the entire triangle ABC
    # Using the cross product formula: area = 0.5 * |AB × AC|
    v0x = c[0] - a[0]
    v0y = c[1] - a[1]
    v1x = b[0] - a[0]
    v1y = b[1] - a[1]
    v2x = p[0] - a[0]
    v2y = p[1] - a[1]
    
    # Compute dot products
    dot00 = v0x * v0x + v0y * v0y
    dot01 = v0x * v1x + v0y * v1y
    dot02 = v0x * v2x + v0y * v2y
    dot11 = v1x * v1x + v1y * v1y
    dot12 = v1x * v2x + v1y * v2y
    
    # Compute barycentric coordinates
    inv_denom = 1.0 / (dot00 * dot11 - dot01 * dot01)
    beta = (dot11 * dot02 - dot01 * dot12) * inv_denom
    gamma = (dot00 * dot12 - dot01 * dot02) * inv_denom
    alpha = 1.0 - beta - gamma
    
    return alpha, beta, gamma

def is_inside_triangle(alpha, beta, gamma, epsilon=1e-6):
    """
    Check if barycentric coordinates represent a point inside the triangle.
    Allow small epsilon for numerical stability.
    """
    return alpha >= -epsilon and beta >= -epsilon and gamma >= -epsilon

def interpolate_color(alpha, beta, gamma, ca, cb, cc):
    """
    Interpolate color using barycentric coordinates (Gouraud shading).
    CP = alpha*CA + beta*CB + gamma*CC
    """
    r = int(alpha * ca[0] + beta * cb[0] + gamma * cc[0])
    g = int(alpha * ca[1] + beta * cb[1] + gamma * cc[1])
    b = int(alpha * ca[2] + beta * cb[2] + gamma * cc[2])
    
    # Clamp values to valid range [0, 255]
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    
    return (r, g, b)

def get_bounding_box(a, b, c):
    """
    Compute the axis-aligned bounding box for the triangle.
    Returns (min_x, max_x, min_y, max_y)
    """
    min_x = max(0, int(min(a[0], b[0], c[0])))
    max_x = min(WINDOW_WIDTH - 1, int(max(a[0], b[0], c[0])))
    min_y = max(0, int(min(a[1], b[1], c[1])))
    max_y = min(WINDOW_HEIGHT - 1, int(max(a[1], b[1], c[1])))
    
    return min_x, max_x, min_y, max_y

def rasterize_triangle(surface, a, b, c, ca, cb, cc):
    """
    Rasterize a triangle with Gouraud shading using barycentric coordinates.
    
    Args:
        surface: PyGame surface to draw on
        a, b, c: Triangle vertices (x, y)
        ca, cb, cc: Colors at vertices (R, G, B)
    """
    # Get bounding box
    min_x, max_x, min_y, max_y = get_bounding_box(a, b, c)
    
    # Iterate over all pixels in bounding box
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            # Pixel center
            p = (x + 0.5, y + 0.5)
            
            # Compute barycentric coordinates
            alpha, beta, gamma = barycentric_coordinates(p, a, b, c)
            
            # Check if pixel is inside triangle
            if is_inside_triangle(alpha, beta, gamma):
                # Interpolate color using Gouraud shading
                color = interpolate_color(alpha, beta, gamma, ca, cb, cc)
                
                # Set pixel color
                surface.set_at((x, y), color)

def draw_vertex_markers(surface, a, b, c, ca, cb, cc):
    """
    Draw small circles at vertices to show their positions and colors.
    """
    radius = 5
    for vertex, color in [(a, ca), (b, cb), (c, cc)]:
        pygame.draw.circle(surface, color, vertex, radius)
        pygame.draw.circle(surface, (255, 255, 255), vertex, radius, 1)

def main():
    clock = pygame.time.Clock()
    
    # Fill background
    screen.fill(BACKGROUND_COLOR)
    
    # Rasterize the triangle with Gouraud shading
    print("Rasterizing triangle with Gouraud shading...")
    print(f"Vertex A: {A}, Color: {CA} (Red)")
    print(f"Vertex B: {B}, Color: {CB} (Green)")
    print(f"Vertex C: {C}, Color: {CC} (Blue)")
    
    rasterize_triangle(screen, A, B, C, CA, CB, CC)
    
    # Draw vertex markers
    draw_vertex_markers(screen, A, B, C, CA, CB, CC)
    
    pygame.display.flip()
    print("Triangle rendered successfully!")
    print("Close the window to exit.")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Maintain frame rate
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()