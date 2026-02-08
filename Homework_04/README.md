## Installation

### Requirements
- Python 3.7+
- Required packages:

```bash
pip install pygame PyOpenGL Pillow numpy
```

2. **Run the application:**
   python main.py


3. **Verify the window opens** with a textured floor and 13 objects (spheres and a box)


## Controls

### Camera Controls
Action               Control 
Orbit camera         Left mouse drag 
Pan camera           Middle mouse drag OR Shift + Left drag 
Zoom                 Right mouse drag OR Mouse wheel 

### Object Selection 
Action                  Control 
Select object           Left click on object 
Deselect                Click on empty space 

##Visual Feedback:
- Selected objects show yellow wireframe overlay
- Selected objects have emissive glow

### Transform Controls
*Requires an object to be selected first*

Action                  Key 
Move +Z (forward)       `I` 
Move -Z (backward)      `K` 
Move -X (left)          `J` 
Move +X (right)         `L` 
Move +Y (up)            `U` 
Move -Y (down)          `O` 
Fine movement           Hold `Shift` + movement key 

**Movement Speeds:**
- Normal: 0.2 units/frame
- Fine (with Shift): 0.05 units/frame

### Lighting Controls (C5)

**Toggle control mode:** Press `TAB`

#### Camera Mode (default)
Action                  Key 
Move light -X           `A` 
Move light +X           `D` 
Move light -Z           `W` 
Move light +Z           `S` 
Move light +Y           `Q` 
Move light -Y           `E` 

#### Light Mode (after pressing TAB)
Action                  Key 
Move light -X           `Left Arrow` 
Move light +X           `Right Arrow` 
Move light -Z           `Up Arrow` 
Move light +Z           `Down Arrow` 
Move light +Y           `Page Up` 
Move light -Y           `Page Down` 

### Scene Management (C6)
Action                  Key 
Save scene              `Ctrl + S` 
Load scene              `Ctrl + L` 
Quit                    `ESC` 

**Scenes are saved to/loaded from `scene.json` in the same directory.**


## Technical Explanations

### 1. Picking Math 

**Problem:** Convert a 2D mouse click into a 3D object selection.

**Solution:** Ray-casting with intersection testing.

#### Step 1: Unproject Mouse to 3D Ray
```python
# Get OpenGL matrices
modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
projection = glGetDoublev(GL_PROJECTION_MATRIX)
viewport = glGetIntegerv(GL_VIEWPORT)

# Convert mouse (x, y) to two 3D points (near and far planes)
near_point = gluUnProject(mouse_x, mouse_y, 0.0, modelview, projection, viewport)
far_point = gluUnProject(mouse_x, mouse_y, 1.0, modelview, projection, viewport)

# Compute ray direction
ray_origin = near_point
ray_direction = normalize(far_point - near_point)

#### Step 2: Ray-Sphere Intersection
**Math:** Solve the quadratic equation for ray-sphere intersection.

Given:
- Ray: `P = O + t*D` (origin O, direction D, parameter t)
- Sphere: `P - C² = r²` (center C, radius r)

Substitute ray into sphere equation:
```
O + t*D - C² = r²
(O - C + t*D) · (O - C + t*D) = r²

Expand to quadratic: at² + bt + c = 0
where:
  a = D · D
  b = 2(O - C) · D
  c = (O - C) · (O - C) - r²
```

Solve using quadratic formula:
```python
discriminant = b² - 4ac
if discriminant < 0: return None  # No intersection

t1 = (-b - sqrt(discriminant)) / (2a)
t2 = (-b + sqrt(discriminant)) / (2a)

# Return smallest positive t (closest hit in front of camera)
return min(t1, t2) if both > 0 else None
```

#### Step 3: Ray-Box Intersection
**Algorithm:** Slab method for axis-aligned bounding boxes (AABB).

For each axis (x, y, z):
```python
# Compute intersection distances with pair of parallel planes
t1 = (box_min[axis] - ray_origin[axis]) / ray_dir[axis]
t2 = (box_max[axis] - ray_origin[axis]) / ray_dir[axis]

# Ensure t1 < t2
if t1 > t2: swap(t1, t2)

# Update overall intersection range
t_min = max(t_min, t1)
t_max = min(t_max, t2)

# If ranges don't overlap, no intersection
if t_min > t_max: return None
```

#### Step 4: Select Closest Object
for obj in objects:
    distance = ray_intersection(ray, obj)
    if distance < closest_distance:
        closest_object = obj

---

### 2. Transparency Sorting (C4)

**Problem:** Transparent objects must render correctly from any viewing angle.

**OpenGL Limitation:** Fixed pipeline uses depth testing + alpha blending. For correct transparency:
1. Opaque objects MUST render first (write to depth buffer)
2. Transparent objects MUST render back-to-front (don't write to depth buffer)

#### Algorithm

**Step 1: Separate Objects by Transparency**
```python
opaque = [obj for obj in objects if obj.color[3] >= 1.0]
transparent = [obj for obj in objects if obj.color[3] < 1.0]
```

**Step 2: Render Opaque Objects**
```python
for obj in opaque:
    obj.render()  
```

**Step 3: Sort Transparent Objects**
```python
def distance_to_camera(obj):
    dx = obj.position[0] - camera_eye[0]
    dy = obj.position[1] - camera_eye[1]
    dz = obj.position[2] - camera_eye[2]
    return -(dx² + dy² + dz²)  # Negative for descending order

transparent.sort(key=distance_to_camera)  # Back-to-front
```
I use negative because Python's `sort()` is ascending by default. Negative squared distance gives descending order (farthest first).

**Step 4: Render Transparent Objects**
```python
for obj in transparent:
    glDepthMask(GL_FALSE)  # not write to depth buffer
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    obj.render()
    glDepthMask(GL_TRUE)   # Restore depth write
```


#### Visual Test
- Orbit camera around scene
- Look through multiple transparent spheres
- Verify farther objects never appear in front of closer ones