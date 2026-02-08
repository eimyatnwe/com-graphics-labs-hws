import math
from objects import SphereObject, BoxObject

class Scene:
    def __init__(self):
        self.objects = []
        self.selected_object = None
    
    def add_object(self, obj):
        self.objects.append(obj)
    
    def remove_object(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)
            if self.selected_object == obj:
                self.selected_object = None
    
    def select_object(self, obj):
        # Deselect previous
        if self.selected_object:
            self.selected_object.selected = False
        
        # Select new
        self.selected_object = obj
        if obj:
            obj.selected = True
    
    def get_selected(self):
        return self.selected_object
    
    def render(self, camera_eye):
        # Separate opaque and transparent objects
        opaque = [obj for obj in self.objects if not obj.transparent]
        transparent = [obj for obj in self.objects if obj.transparent]
        
        for obj in opaque:
            obj.render()
        
        if transparent:
            def distance_to_camera(obj):
                dx = obj.position[0] - camera_eye[0]
                dy = obj.position[1] - camera_eye[1]
                dz = obj.position[2] - camera_eye[2]
                return -(dx*dx + dy*dy + dz*dz) 
            
            transparent.sort(key=distance_to_camera)
            
            for obj in transparent:
                obj.render()
    
    def clear(self):
        self.objects.clear()
        self.selected_object = None


def initialize_default_scene():
    scene = Scene()
    
    # at least 10 spheres
    scene.add_object(SphereObject(
        position=(-3.0, 2.0, 0.0),
        radius=2.0,
        color=(0.0, 1.0, 1.0, 1.0),
        shininess=60.0,
        specular_strength=1.0
    ))
    
    scene.add_object(SphereObject(
        position=(3.0, 2.0, 0.0),
        radius=2.0,
        color=(0.7, 0.7, 1.0, 0.30),
        shininess=30.0,
        specular_strength=0.6
    ))
    
    scene.add_object(SphereObject(
        position=(0.0, 3.5, -4.0),
        radius=1.5,
        color=(1.0, 0.2, 0.2, 1.0),
        shininess=40.0,
        specular_strength=0.8
    ))
    
    scene.add_object(SphereObject(
        position=(-6.0, 1.5, -3.0),
        radius=1.5,
        color=(0.2, 1.0, 0.2, 1.0),
        shininess=35.0,
        specular_strength=0.7
    ))
    
    scene.add_object(SphereObject(
        position=(6.0, 1.5, -3.0),
        radius=1.5,
        color=(1.0, 1.0, 0.2, 1.0),
        shininess=45.0,
        specular_strength=0.6
    ))
    
    scene.add_object(SphereObject(
        position=(-4.0, 1.0, 4.0),
        radius=1.0,
        color=(1.0, 0.5, 0.0, 1.0),
        shininess=50.0,
        specular_strength=0.9
    ))
    
    scene.add_object(SphereObject(
        position=(4.0, 1.0, 4.0),
        radius=1.0,
        color=(0.5, 0.0, 1.0, 1.0),
        shininess=55.0,
        specular_strength=0.8
    ))
    
    scene.add_object(SphereObject(
        position=(0.0, 1.0, 6.0),
        radius=1.2,
        color=(1.0, 0.0, 0.5, 0.5),
        shininess=40.0,
        specular_strength=0.7
    ))
    
    scene.add_object(SphereObject(
        position=(-8.0, 2.5, 0.0),
        radius=1.8,
        color=(0.0, 0.5, 1.0, 0.6),
        shininess=30.0,
        specular_strength=0.5
    ))
    
    scene.add_object(SphereObject(
        position=(8.0, 2.5, 0.0),
        radius=1.8,
        color=(1.0, 0.8, 0.0, 1.0),
        shininess=38.0,
        specular_strength=0.85
    ))
    
    scene.add_object(SphereObject(
        position=(0.0, 0.8, -8.0),
        radius=0.8,
        color=(0.5, 1.0, 0.5, 1.0),
        shininess=25.0,
        specular_strength=0.6
    ))
    
    scene.add_object(SphereObject(
        position=(2.0, 1.5, -6.0),
        radius=1.0,
        color=(0.8, 0.3, 0.8, 0.7),
        shininess=42.0,
        specular_strength=0.75
    ))
    
    scene.add_object(BoxObject(
        position=(0.0, 0.75, 0.0),
        size=1.5,
        color=(0.7, 0.7, 0.7, 1.0),
        shininess=20.0,
        specular_strength=0.4
    ))
    
    return scene
