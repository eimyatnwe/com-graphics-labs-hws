import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from objects import SphereObject, BoxObject


def unproject_mouse(mouse_x, mouse_y, win_w, win_h):
    # Get matrices
    modelview = np.array(glGetDoublev(GL_MODELVIEW_MATRIX))
    projection = np.array(glGetDoublev(GL_PROJECTION_MATRIX))
    viewport = np.array(glGetIntegerv(GL_VIEWPORT))
    
    # Convert mouse Y 
    y = viewport[3] - mouse_y
    
    #near and far points
    near_point = gluUnProject(mouse_x, y, 0.0, modelview, projection, viewport)
    far_point = gluUnProject(mouse_x, y, 1.0, modelview, projection, viewport)
    
    ray_origin = np.array(near_point)
    ray_dir = np.array(far_point) - ray_origin
    
    # Normalize direction
    length = np.linalg.norm(ray_dir)
    if length > 0:
        ray_dir = ray_dir / length
    
    return ray_origin, ray_dir


def ray_sphere_intersection(ray_origin, ray_dir, sphere_pos, sphere_radius):
    # Vector from ray origin to sphere center
    oc = ray_origin - np.array(sphere_pos)
    
    # Quadratic equation
    a = np.dot(ray_dir, ray_dir)
    b = 2.0 * np.dot(oc, ray_dir)
    c = np.dot(oc, oc) - sphere_radius * sphere_radius
    
    # delta
    discriminant = b*b - 4*a*c
    
    if discriminant < 0:
        return None  
    
    sqrt_disc = np.sqrt(discriminant)
    t1 = (-b - sqrt_disc) / (2.0 * a)
    t2 = (-b + sqrt_disc) / (2.0 * a)
    
    # return t 
    if t1 > 0:
        return t1
    elif t2 > 0:
        return t2
    else:
        return None


def ray_box_intersection(ray_origin, ray_dir, box_pos, box_size):
    box_pos = np.array(box_pos)
    half_size = box_size / 2.0
    
    box_min = box_pos - half_size
    box_max = box_pos + half_size
    
    t_min = -np.inf
    t_max = np.inf
    
    for i in range(3):
        if abs(ray_dir[i]) < 1e-8:
            # Ray is parallel to slab, check if origin is within slab
            if ray_origin[i] < box_min[i] or ray_origin[i] > box_max[i]:
                return None
        else:
            # Compute intersection t values with the two planes
            t1 = (box_min[i] - ray_origin[i]) / ray_dir[i]
            t2 = (box_max[i] - ray_origin[i]) / ray_dir[i]
            
            if t1 > t2:
                t1, t2 = t2, t1
        
            t_min = max(t_min, t1)
            t_max = min(t_max, t2)
            
            if t_min > t_max:
                return None
    
    if t_max < 0:
        return None  
    
    if t_min > 0:
        return t_min
    else:
        return t_max


def pick_object(mouse_x, mouse_y, win_w, win_h, objects):
    ray_origin, ray_dir = unproject_mouse(mouse_x, mouse_y, win_w, win_h)
    
    closest_obj = None
    closest_dist = float('inf')
    
    for obj in objects:
        dist = None
        
        if isinstance(obj, SphereObject):
            dist = ray_sphere_intersection(ray_origin, ray_dir, obj.position, obj.radius)
        elif isinstance(obj, BoxObject):
            dist = ray_box_intersection(ray_origin, ray_dir, obj.position, obj.size)
  
        if dist is not None and dist < closest_dist:
            closest_dist = dist
            closest_obj = obj
    
    return closest_obj
