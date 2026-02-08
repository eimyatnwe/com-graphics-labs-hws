import math
import pygame

# ========== Basic vector helpers ==========

def v_add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def v_sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

def v_mul(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)

def v_dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def v_length(a):
    return math.sqrt(v_dot(a, a))

def v_norm(a):
    l = v_length(a)
    if l == 0:
        return (0.0, 0.0, 0.0)
    return (a[0]/l, a[1]/l, a[2]/l)

def v_cross(a, b):
    return (a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0])

def v_reflect(i, n):
    dot = v_dot(i, n)
    return v_sub(i, v_mul(n, 2.0 * dot))

# ========== Rotation matrix ==========

def make_rotation_matrix(rx_deg, ry_deg, rz_deg):
    rx = math.radians(rx_deg)
    ry = math.radians(ry_deg)
    rz = math.radians(rz_deg)

    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    cz, sz = math.cos(rz), math.sin(rz)

    Rx = [
        [1, 0, 0],
        [0, cx, -sx],
        [0, sx,  cx],
    ]
    Ry = [
        [ cy, 0, sy],
        [  0, 1,  0],
        [-sy, 0, cy],
    ]
    Rz = [
        [cz, -sz, 0],
        [sz,  cz, 0],
        [ 0,   0, 1],
    ]

    def mat_mul(a, b):
        r = [[0]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                r[i][j] = a[i][0]*b[0][j] + a[i][1]*b[1][j] + a[i][2]*b[2][j]
        return r

    return mat_mul(Rz, mat_mul(Ry, Rx))

def mat_vec_mul(M, v):
    return (
        M[0][0]*v[0] + M[0][1]*v[1] + M[0][2]*v[2],
        M[1][0]*v[0] + M[1][1]*v[1] + M[1][2]*v[2],
        M[2][0]*v[0] + M[2][1]*v[1] + M[2][2]*v[2],
    )

# ========== Ray–Triangle (Möller–Trumbore) ==========

def intersect_triangle(ray_origin, ray_dir, v0, v1, v2):
    eps = 1e-6
    edge1 = v_sub(v1, v0)
    edge2 = v_sub(v2, v0)
    h = v_cross(ray_dir, edge2)
    a = v_dot(edge1, h)
    if -eps < a < eps:
        return (False, None, None)
    f = 1.0 / a
    s = v_sub(ray_origin, v0)
    u = f * v_dot(s, h)
    if u < 0.0 or u > 1.0:
        return (False, None, None)
    q = v_cross(s, edge1)
    v = f * v_dot(ray_dir, q)
    if v < 0.0 or u + v > 1.0:
        return (False, None, None)
    t = f * v_dot(edge2, q)
    if t > eps:
        n = v_norm(v_cross(edge1, edge2))
        return (True, t, n)
    return (False, None, None)

# ========== Build rotated box as triangle mesh ==========

def build_rotated_box_mesh(angle_y_deg):
    # local cube vertices
        # local cube vertices (bigger box)
    verts = [
        (-1.0, -1.0, -1.0),  # 0
        ( 1.0, -1.0, -1.0),  # 1
        ( 1.0,  1.0, -1.0),  # 2
        (-1.0,  1.0, -1.0),  # 3
        (-1.0, -1.0,  1.0),  # 4
        ( 1.0, -1.0,  1.0),  # 5
        ( 1.0,  1.0,  1.0),  # 6
        (-1.0,  1.0,  1.0),  # 7
    ]

    tris_idx = [
        (4, 5, 6), (4, 6, 7),    # frontangle += 2.0
        (1, 0, 3), (1, 3, 2),    # back
        (0, 4, 7), (0, 7, 3),    # left
        (5, 1, 2), (5, 2, 6),    # right
        (0, 1, 5), (0, 5, 4),    # bottom
        (3, 7, 6), (3, 6, 2),    # top
    ]

    # base rotation + extra spin around Y
    R = make_rotation_matrix(45.0, 46.0 + angle_y_deg, 47.0)

    rot_verts = [mat_vec_mul(R, v) for v in verts]

    triangles = []
    for i0, i1, i2 in tris_idx:
        v0 = rot_verts[i0]
        v1 = rot_verts[i1]
        v2 = rot_verts[i2]
        triangles.append((v0, v1, v2))

    return triangles

# ========== Shading ==========

def trace_ray(ray_origin, ray_dir, triangles, lights, background_color):
    t_min = float('inf')
    hit_normal = None

    for v0, v1, v2 in triangles:
        hit, t, n = intersect_triangle(ray_origin, ray_dir, v0, v1, v2)
        if hit and t < t_min:
            t_min = t
            hit_normal = n

    if hit_normal is None:
        return background_color

    p = v_add(ray_origin, v_mul(ray_dir, t_min))

    base_color = (1.0, 0.0, 0.0)
    spec_color = (0.6, 0.6, 0.6)
    ambient_k = 0.1
    shininess = 50.0

    r, g, b = [ambient_k * c for c in base_color]
    view_dir = v_norm(v_mul(ray_dir, -1.0))

    for light_pos, light_col in lights:
        L = v_norm(v_sub(light_pos, p))
        ndotl = v_dot(hit_normal, L)
        if ndotl > 0.0:
            diff = ndotl
            refl = v_reflect(v_mul(L, -1.0), hit_normal)
            rv = max(0.0, v_dot(refl, view_dir))
            spec = (rv ** shininess) if rv > 0.0 else 0.0

            r += light_col[0] * (base_color[0] * diff + spec_color[0] * spec)
            g += light_col[1] * (base_color[1] * diff + spec_color[1] * spec)
            b += light_col[2] * (base_color[2] * diff + spec_color[2] * spec)

    r = max(0.0, min(1.0, r))
    g = max(0.0, min(1.0, g))
    b = max(0.0, min(1.0, b))
    return (r, g, b)

# ========== Render one frame ==========

def render(width, height, angle_y_deg):
    eye     = (0.0, 0.5, -4.0)
    look_at = (0.0, 0.0,  0.0)
    up      = (0.0, 1.0,  0.0)

    fov_y = math.radians(60.0)
    aspect = width / float(height)

    forward = v_norm(v_sub(look_at, eye))
    right   = v_norm(v_cross(forward, up))
    up_cam  = v_cross(right, forward)

    half_h = math.tan(fov_y / 2.0)
    half_w = aspect * half_h

    triangles = build_rotated_box_mesh(angle_y_deg)

    lights = [
        ((-5.0,  5.0, -5.0), (1.0, 1.0, 1.0)),
        (( 6.0, -6.0, -6.0), (0.25, 0.25, 0.25)),
    ]
    background_color = (0.25, 0.25, 0.25)

    framebuffer = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]

    for j in range(height):
        ndc_y = 1.0 - 2.0 * (j + 0.5) / float(height)
        for i in range(width):
            ndc_x = 2.0 * (i + 0.5) / float(width) - 1.0

            px = ndc_x * half_w
            py = ndc_y * half_h

            dir_world = v_add(
                forward,
                v_add(v_mul(right, px), v_mul(up_cam, py))
            )
            dir_world = v_norm(dir_world)

            color = trace_ray(eye, dir_world, triangles, lights, background_color)
            framebuffer[j][i] = (
                int(color[0]*255),
                int(color[1]*255),
                int(color[2]*255),
            )

    return framebuffer

# ========== Main loop (animation) ==========

def main():
    width, height = 320, 240

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("CPU Ray Tracer - Rotating Box Mesh")

    surface = pygame.Surface((width, height))
    clock = pygame.time.Clock()

    angle = 0.0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        framebuffer = render(width, height, angle)

        for y in range(height):
            for x in range(width):
                surface.set_at((x, y), framebuffer[y][x])

        screen.blit(surface, (0, 0))
        pygame.display.flip()

        angle += 8.0   # degree per frame
        clock.tick(15) # fps (ray tracing แบบ python ขอลดลงหน่อย)

    pygame.quit()

if __name__ == "__main__":
    main()
