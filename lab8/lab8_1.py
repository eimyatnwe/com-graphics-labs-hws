import pygame
import sys

# Initialize Pygame
pygame.init()

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)
LINE_COLOR = (255, 255, 255)
POINT_COLOR = (255, 0, 0)

# Create window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Bresenham's Line Algorithm")

def bresenham_line(x0, y0, x1, y1):
    """
    Bresenham's line algorithm implementation.
    Returns a list of (x, y) pixel coordinates forming the line.
    """
    pixels = []
    
    # Calculate differences and step directions
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    
    # Determine step direction
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    
    # Initial error term
    err = dx - dy
    
    # Current position
    x, y = x0, y0
    
    while True:
        # Plot current pixel
        pixels.append((x, y))
        
        # Check if we've reached the endpoint
        if x == x1 and y == y1:
            break
        
        # Calculate error term for next pixel
        e2 = 2 * err
        
        # Update x coordinate and error term
        if e2 > -dy:
            err -= dy
            x += sx
        
        # Update y coordinate and error term
        if e2 < dx:
            err += dx
            y += sy
    
    return pixels

def draw_line(surface, x0, y0, x1, y1, color):
    """
    Draw a line using Bresenham's algorithm.
    """
    pixels = bresenham_line(x0, y0, x1, y1)
    for x, y in pixels:
        surface.set_at((x, y), color)

def draw_point(surface, x, y, color, size=3):
    """
    Draw a small circle to mark a point.
    """
    for dx in range(-size, size + 1):
        for dy in range(-size, size + 1):
            if dx*dx + dy*dy <= size*size:
                px, py = x + dx, y + dy
                if 0 <= px < WINDOW_WIDTH and 0 <= py < WINDOW_HEIGHT:
                    surface.set_at((px, py), color)

def main():
    clock = pygame.time.Clock()
    
    # State variables
    points = []  # Stores clicked points
    first_point = None
    
    # Font for displaying coordinates
    font = pygame.font.Font(None, 24)
    
    # Fill background initially
    screen.fill(BACKGROUND_COLOR)
    pygame.display.flip()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = event.pos
                    
                    if first_point is None:
                        # First click - store start point
                        first_point = (mouse_x, mouse_y)
                        print(f"P0 = ({mouse_x}, {mouse_y})")
                        
                        # Draw the start point
                        draw_point(screen, mouse_x, mouse_y, POINT_COLOR)
                        pygame.display.flip()
                    
                    else:
                        # Second click - draw line
                        x0, y0 = first_point
                        x1, y1 = mouse_x, mouse_y
                        
                        print(f"P1 = ({x1}, {y1})")
                        print(f"Drawing line from P0=({x0},{y0}) to P1=({x1},{y1})")
                        
                        # Draw the line using Bresenham's algorithm
                        draw_line(screen, x0, y0, x1, y1, LINE_COLOR)
                        
                        # Draw the end point
                        draw_point(screen, x1, y1, POINT_COLOR)
                        
                        # Display coordinates on screen
                        text = font.render(f"P0=({x0},{y0}), P1=({x1},{y1})", 
                                         True, (0, 255, 0))
                        
                        pygame.display.flip()
                        
                        # Reset for next line
                        first_point = None
                        print("Ready for next line\n")
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    # Clear screen with 'C' key
                    screen.fill(BACKGROUND_COLOR)
                    first_point = None
                    pygame.display.flip()
                    print("Screen cleared\n")
        
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    print("Bresenham's Line Algorithm")
    print("=" * 40)
    print("Left click twice to draw a line")
    print("Press 'C' to clear the screen")
    print("=" * 40)
    print()
    main()