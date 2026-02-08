from OpenGL.GL import *
from OpenGL.GLU import *


class SceneObject:
    def __init__(self, position=(0.0, 0.0, 0.0), scale=1.0, 
                 color=(1.0, 1.0, 1.0, 1.0), shininess=30.0, specular_strength=0.5):
        self.position = list(position)
        self.scale = scale
        self.color = list(color)  
        self.shininess = shininess
        self.specular_strength = specular_strength
        self.selected = False 
    
    @property
    def transparent(self):
        return self.color[3] < 1.0
    
    def render(self, highlight=False):
        raise NotImplementedError("Subclasses must implement render()")
    
    def apply_material(self, highlight=False):
        if self.transparent:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glDepthMask(GL_FALSE)
        else:
            glDisable(GL_BLEND)
            glDepthMask(GL_TRUE)
        
        # Highlight selected objects with emissive color
        if highlight or self.selected:
            glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, (0.3, 0.3, 0.0, 1.0))
        else:
            glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, (0.0, 0.0, 0.0, 1.0))
        
        # Set material properties
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)
        
        spec_color = [self.specular_strength] * 3 + [self.color[3]]
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, spec_color)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, self.shininess)
    
    def cleanup_material(self):
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, (0.0, 0.0, 0.0, 1.0))
        if self.transparent:
            glDepthMask(GL_TRUE)
            glDisable(GL_BLEND)
    
    def to_dict(self):
        raise NotImplementedError("Subclasses must implement to_dict()")
    
    @staticmethod
    def from_dict(data):
        raise NotImplementedError("Subclasses must implement from_dict()")


class SphereObject(SceneObject):
    def __init__(self, position=(0.0, 0.0, 0.0), radius=1.0, 
                 color=(1.0, 1.0, 1.0, 1.0), shininess=30.0, specular_strength=0.5):
        super().__init__(position, radius, color, shininess, specular_strength)
        self.radius = radius
    
    def render(self, highlight=False):
        glPushMatrix()
        glTranslatef(*self.position)
        
        self.apply_material(highlight)
        
        quad = gluNewQuadric()
        gluQuadricNormals(quad, GLU_SMOOTH)
        gluSphere(quad, self.radius, 48, 48)
        gluDeleteQuadric(quad)
        
        if self.selected:
            glDisable(GL_LIGHTING)
            glColor3f(1.0, 1.0, 0.0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glLineWidth(2.0)
            
            quad2 = gluNewQuadric()
            gluSphere(quad2, self.radius * 1.02, 24, 24)
            gluDeleteQuadric(quad2)
            
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glLineWidth(1.0)
            glEnable(GL_LIGHTING)
        
        self.cleanup_material()
        glPopMatrix()
    
    def to_dict(self):
        return {
            'type': 'sphere',
            'position': self.position,
            'radius': self.radius,
            'color': self.color,
            'shininess': self.shininess,
            'specular_strength': self.specular_strength
        }
    
    @staticmethod
    def from_dict(data):
        return SphereObject(
            position=tuple(data['position']),
            radius=data['radius'],
            color=tuple(data['color']),
            shininess=data['shininess'],
            specular_strength=data['specular_strength']
        )


class BoxObject(SceneObject):
    def __init__(self, position=(0.0, 0.0, 0.0), size=1.0, 
                 color=(1.0, 1.0, 1.0, 1.0), shininess=20.0, specular_strength=0.4):
        super().__init__(position, size, color, shininess, specular_strength)
        self.size = size
    
    def render(self, highlight=False):
        glPushMatrix()
        glTranslatef(*self.position)
        
        self.apply_material(highlight)
        
        s = self.size / 2.0
        
        # Front face
        glBegin(GL_QUADS)
        glNormal3f(0.0, 0.0, 1.0)
        glVertex3f(-s, -s, s)
        glVertex3f( s, -s, s)
        glVertex3f( s,  s, s)
        glVertex3f(-s,  s, s)
        glEnd()
        
        # Back face
        glBegin(GL_QUADS)
        glNormal3f(0.0, 0.0, -1.0)
        glVertex3f(-s, -s, -s)
        glVertex3f(-s,  s, -s)
        glVertex3f( s,  s, -s)
        glVertex3f( s, -s, -s)
        glEnd()
        
        # Top face
        glBegin(GL_QUADS)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(-s, s, -s)
        glVertex3f(-s, s,  s)
        glVertex3f( s, s,  s)
        glVertex3f( s, s, -s)
        glEnd()
        
        # Bottom face
        glBegin(GL_QUADS)
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(-s, -s, -s)
        glVertex3f( s, -s, -s)
        glVertex3f( s, -s,  s)
        glVertex3f(-s, -s,  s)
        glEnd()
        
        # Right face
        glBegin(GL_QUADS)
        glNormal3f(1.0, 0.0, 0.0)
        glVertex3f(s, -s, -s)
        glVertex3f(s,  s, -s)
        glVertex3f(s,  s,  s)
        glVertex3f(s, -s,  s)
        glEnd()
        
        # Left face
        glBegin(GL_QUADS)
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(-s, -s, -s)
        glVertex3f(-s, -s,  s)
        glVertex3f(-s,  s,  s)
        glVertex3f(-s,  s, -s)
        glEnd()
        
        self.cleanup_material()
        glPopMatrix()
    
    def to_dict(self):
        return {
            'type': 'box',
            'position': self.position,
            'size': self.size,
            'color': self.color,
            'shininess': self.shininess,
            'specular_strength': self.specular_strength
        }
    
    @staticmethod
    def from_dict(data):
        return BoxObject(
            position=tuple(data['position']),
            size=data['size'],
            color=tuple(data['color']),
            shininess=data['shininess'],
            specular_strength=data['specular_strength']
        )
