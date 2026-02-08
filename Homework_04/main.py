"""
Interactive Scene Editor - Part C Challenge Homework
All features C1-C6 implemented
"""
import os
import math
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

# Pillow (PIL) for loading textures
try:
    from PIL import Image
except ImportError:
    raise SystemExit("Missing Pillow. Install with: python -m pip install Pillow")

# Import our modules
from scene import Scene, initialize_default_scene
from picking import pick_object
from io_scene import save_scene, load_scene

# -------------------------
# Config
# -------------------------
WIN_W, WIN_H = 800, 600
FLOOR_SIZE = 120.0
TILE_REPEAT = 30.0
FPS = 60

# Orbit camera
target = [0.0, 1.0, 0.0]
yaw = 0.0
pitch = 15.0
distance = 18.0

# Mouse state
last_mouse = None
orbiting = False
panning = False
zooming = False

# Light
light_pos = [0.0, 6.0, 2.0, 1.0]

# C5: Control mode (camera vs light)
control_mode = "camera"  # "camera" or "light"


# -------------------------
# Small math helpers
# -------------------------
def clamp(x, a, b):
    return max(a, min(b, x))


def normalize(v):
    l = math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
    if l == 0:
        return [0.0, 0.0, 0.0]
    return [v[0]/l, v[1]/l, v[2]/l]


def cross(a, b):
    return [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0],
    ]


# -------------------------
# Texture loading (floor)
# -------------------------
def load_texture(path: str) -> int:
    """Load an image as an OpenGL RGB texture with GL_REPEAT tiling."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Texture not found: {path}")

    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)

    img = Image.open(path).convert("RGB").transpose(Image.FLIP_TOP_BOTTOM)
    data = img.tobytes()

    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGB,
        img.width, img.height, 0,
        GL_RGB, GL_UNSIGNED_BYTE, data
    )

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Repeat pattern across the floor
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glBindTexture(GL_TEXTURE_2D, 0)
    return tex


# -------------------------
# OpenGL overlay text (PyGame font -> GL texture)
# -------------------------
def create_text_texture(font, text, color=(255, 255, 255), bg=(0, 0, 0, 180)):
    """
    Render text to a PyGame RGBA surface, upload it as an OpenGL texture.
    Returns (tex_id, w, h).
    """
    text_surf = font.render(text, True, color)
    w, h = text_surf.get_size()

    box = pygame.Surface((w + 10, h + 6), pygame.SRCALPHA)
    box.fill(bg)
    box.blit(text_surf, (5, 3))

    tex_data = pygame.image.tostring(box, "RGBA", True)
    tw, th = box.get_size()

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tw, th, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glBindTexture(GL_TEXTURE_2D, 0)

    return tex_id, tw, th


def begin_2d():
    """Switch to 2D pixel coordinate rendering (0,0)=top-left."""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, WIN_W, WIN_H, 0, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


def end_2d():
    """Restore 3D state."""
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    glMatrixMode(GL_MODELVIEW)


def draw_tex_2d(tex_id, x, y, w, h):
    glDisable(GL_CULL_FACE)           # ensure it can’t be culled
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    glColor4f(1, 1, 1, 1)
    glBegin(GL_QUADS)
    # Correct mapping for glOrtho(0, W, H, 0, ...) (top-left origin)
    glTexCoord2f(0, 1); glVertex2f(x,     y)      # top-left
    glTexCoord2f(1, 1); glVertex2f(x + w, y)      # top-right
    glTexCoord2f(1, 0); glVertex2f(x + w, y + h)  # bottom-right
    glTexCoord2f(0, 0); glVertex2f(x,     y + h)  # bottom-left
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)



# -------------------------
# Scene setup
# -------------------------
def setup_scene():
    glClearColor(0.55, 0.55, 0.58, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_DIFFUSE,  (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT,  (0.18, 0.18, 0.18, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))


def set_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, WIN_W / WIN_H, 0.1, 300.0)
    glMatrixMode(GL_MODELVIEW)


def get_eye_and_basis():
    """Compute camera eye position + basis vectors (right/up) for panning."""
    ry = math.radians(yaw)
    rp = math.radians(pitch)

    eye = [
        target[0] + distance * math.cos(rp) * math.sin(ry),
        target[1] + distance * math.sin(rp),
        target[2] + distance * math.cos(rp) * math.cos(ry),
    ]

    forward = normalize([target[0] - eye[0], target[1] - eye[1], target[2] - eye[2]])
    world_up = [0.0, 1.0, 0.0]
    right = normalize(cross(forward, world_up))
    up = normalize(cross(right, forward))
    return eye, right, up


def apply_camera():
    glLoadIdentity()
    eye, _, _ = get_eye_and_basis()
    gluLookAt(
        eye[0], eye[1], eye[2],
        target[0], target[1], target[2],
        0.0, 1.0, 0.0
    )


# -------------------------
# Drawing
# -------------------------
def draw_floor(tex):
    half = FLOOR_SIZE / 2.0

    # Do NOT cull the floor (single quad is one-sided)
    glDisable(GL_CULL_FACE)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex)

    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.2, 0.2, 0.2, 1.0))
    glMaterialf(GL_FRONT, GL_SHININESS, 8.0)

    glBegin(GL_QUADS)
    glNormal3f(0.0, 1.0, 0.0)

    glTexCoord2f(0.0, 0.0);                 glVertex3f(-half, 0.0, -half)
    glTexCoord2f(TILE_REPEAT, 0.0);         glVertex3f( half, 0.0, -half)
    glTexCoord2f(TILE_REPEAT, TILE_REPEAT); glVertex3f( half, 0.0,  half)
    glTexCoord2f(0.0, TILE_REPEAT);         glVertex3f(-half, 0.0,  half)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)


# -------------------------
# Input
# -------------------------
def handle_input(scene):
    global last_mouse, orbiting, panning, zooming, yaw, pitch, distance, target, light_pos, control_mode

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            
            # C5: Toggle control mode with TAB
            if event.key == pygame.K_TAB:
                control_mode = "light" if control_mode == "camera" else "camera"
                print(f"Control mode: {control_mode.upper()}")
            
            # C6: Save/Load scene
            mods = pygame.key.get_mods()
            if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                save_scene(scene)
            if event.key == pygame.K_l and (mods & pygame.KMOD_CTRL):
                load_scene(scene)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # C2: Picking on left click (without dragging)
                if not orbiting:
                    mouse = pygame.mouse.get_pos()
                    picked = pick_object(mouse[0], mouse[1], WIN_W, WIN_H, scene.objects)
                    scene.select_object(picked)
                    if picked:
                        print(f"Selected object at {picked.position}")
                orbiting = True
            if event.button == 2: panning = True
            if event.button == 3: zooming = True
            if event.button == 4: distance = max(2.0, distance - 0.8)
            if event.button == 5: distance = min(150.0, distance + 0.8)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: orbiting = False
            if event.button == 2: panning = False
            if event.button == 3: zooming = False

    keys = pygame.key.get_pressed()
    mods = pygame.key.get_mods()
    shift = (mods & pygame.KMOD_SHIFT) != 0
    
    # C5: Light control mode
    if control_mode == "light":
        # Arrow keys move light in X/Z
        light_speed = 0.3
        if keys[pygame.K_LEFT]: light_pos[0] -= light_speed
        if keys[pygame.K_RIGHT]: light_pos[0] += light_speed
        if keys[pygame.K_UP]: light_pos[2] -= light_speed
        if keys[pygame.K_DOWN]: light_pos[2] += light_speed
        if keys[pygame.K_PAGEUP]: light_pos[1] += light_speed
        if keys[pygame.K_PAGEDOWN]: light_pos[1] -= light_speed
    else:
        # Camera control mode (original WASD for light)
        if keys[pygame.K_a]: light_pos[0] -= 0.2
        if keys[pygame.K_d]: light_pos[0] += 0.2
        if keys[pygame.K_w]: light_pos[2] -= 0.2
        if keys[pygame.K_s]: light_pos[2] += 0.2
        if keys[pygame.K_q]: light_pos[1] += 0.2
        if keys[pygame.K_e]: light_pos[1] -= 0.2
    
    # C3: Transform controls (move selected object)
    selected = scene.get_selected()
    if selected:
        # Fine vs coarse movement with Shift
        move_speed = 0.05 if shift else 0.2
        
        if keys[pygame.K_j]: selected.position[0] -= move_speed  # -X
        if keys[pygame.K_l]: selected.position[0] += move_speed  # +X
        if keys[pygame.K_i]: selected.position[2] -= move_speed  # +Z (forward)
        if keys[pygame.K_k]: selected.position[2] += move_speed  # -Z (backward)
        if keys[pygame.K_u]: selected.position[1] += move_speed  # +Y
        if keys[pygame.K_o]: selected.position[1] -= move_speed  # -Y

    mouse = pygame.mouse.get_pos()
    
    if last_mouse is not None:
        dx = mouse[0] - last_mouse[0]
        dy = mouse[1] - last_mouse[1]

        # Orbit (left drag)
        if orbiting and not shift and not panning:
            yaw += dx * 0.35
            pitch -= dy * 0.35
            pitch = clamp(pitch, -89.0, 89.0)

        # Pan (middle drag OR shift+left): pan target using camera basis
        if panning or (orbiting and shift):
            _, right, up = get_eye_and_basis()
            pan_speed = 0.01 * (distance / 10.0)
            target[0] -= right[0] * dx * pan_speed
            target[1] -= right[1] * dx * pan_speed
            target[2] -= right[2] * dx * pan_speed

            target[0] += up[0] * dy * pan_speed
            target[1] += up[1] * dy * pan_speed
            target[2] += up[2] * dy * pan_speed

        # Zoom (right drag)
        if zooming:
            distance += dy * 0.05
            distance = clamp(distance, 2.0, 150.0)

    last_mouse = mouse
    return True


# -------------------------
# Main
# -------------------------
def main():
    pygame.init()
    pygame.display.set_mode((WIN_W, WIN_H), pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.font.init()
    font = pygame.font.SysFont("Consolas", 14)
    pygame.display.set_caption("Scene Editor - All Features C1-C6")

    setup_scene()
    set_projection()
    
    # C1: Initialize scene with 10+ objects
    scene = initialize_default_scene()

    # Load floor texture
    tex = load_texture("floor.jpg")

    clock = pygame.time.Clock()
    running = True
    
    # For dynamic overlay text
    overlay_tex = []

    try:
        while running:
            running = handle_input(scene)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            apply_camera()

            glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

            draw_floor(tex)
            
            eye, _, _ = get_eye_and_basis()
            scene.render(eye)

            selected = scene.get_selected()
            overlay_lines = [
                f"Objects: {len(scene.objects)} | Selected: {'Yes' if selected else 'None'}",
                f"Control Mode: {control_mode.upper()} (TAB to toggle)",
                f"Light Position: ({light_pos[0]:.1f}, {light_pos[1]:.1f}, {light_pos[2]:.1f})",
                "Camera: Left-drag orbit | Shift+Left or Middle pan | Right-drag or Wheel zoom",
                "Light (camera mode): W/A/S/D/Q/E | Light (light mode): Arrows/PgUp/PgDn",
                "Transform: I/K (+Z/-Z) J/L (-X/+X) U/O (+Y/-Y) | Shift=fine",
                "File: Ctrl+S save | Ctrl+L load | ESC quit",
            ]
            
            # Cleanup old textures
            for (tid, _, _) in overlay_tex:
                glDeleteTextures([tid])
            overlay_tex.clear()
            
            # Create new textures
            for line in overlay_lines:
                tid, tw, th = create_text_texture(font, line)
                overlay_tex.append((tid, tw, th))

            # 2D OpenGL overlay
            begin_2d()
            x, y = 10, 10
            for (tid, tw, th) in overlay_tex:
                draw_tex_2d(tid, x, y, tw, th)
                y += th + 4
            end_2d()

            pygame.display.flip()
            clock.tick(FPS)

    finally:
        # Cleanup overlay textures
        for (tid, _, _) in overlay_tex:
            glDeleteTextures([tid])
        pygame.quit()


if __name__ == "__main__":
    main()
