import imgui
from engine.rendering.meshes.mesh import Mesh

# Geometry imports
from engine.geometry.geometry import GEOMETRY_TYPE
from engine.geometry.simple3D.box import BoxGeometry
from engine.geometry.simple3D.sphere import Sphere
from engine.geometry.simple3D.cylinder import Cylinder
from engine.geometry.simple3D.plane import Plane
from engine.geometry.simple2D.rectangle import Rectangle
from engine.geometry.simple2D.circle import Circle
from engine.geometry.simple2D.triangle import Triangle
from engine.geometry.simple2D.polygon import Polygon
from engine.geometry.simple2D.pentagon import Pentagon
from engine.geometry.simple2D.hexagon import Hexagon
from engine.geometry.simple2D.octagon import Octagon
from engine.geometry.simple2D.heptagon import Heptagon
from engine.geometry.simple2D.quad import Quad
from engine.geometry.simple3D.cone import Cone
from engine.geometry.simple3D.prism import Prism
from engine.geometry.simple3D.pyramid import Pyramid
from engine.geometry.simple2D.point import PointGeometry
from engine.geometry.simple2D.line_segment import LineSegment

# Material imports
from engine.material.basic.material import MATERIAL_TYPE
from engine.material.basic.surface import SurfaceMaterial
from engine.material.lighted.lambert import LambertMaterial
from engine.material.lighted.phong import PhongMaterial
from engine.material.lighted.flat import FlatMaterial
from engine.material.basic.line import LineMaterial
from engine.material.basic.point import PointMaterial
from engine.material.basic.sprite import Sprite
from engine.material.basic.texture import TextureMaterial

import random
from engine.ecs.entity import Entity
from engine.ecs.components.components import MeshComponent, PhysicsBody, CollisionComponent
from engine.ecs.components.types import COMPTYPE
from engine.ecs.components.collision import CollisionType

MATERIAL_TYPE_MAP = {
        MATERIAL_TYPE.POINT.value: PointMaterial,
        MATERIAL_TYPE.LINE.value: LineMaterial,
        MATERIAL_TYPE.SURFACE.value: SurfaceMaterial,
        MATERIAL_TYPE.SPRITE.value: Sprite,
        MATERIAL_TYPE.TEXTURE.value: TextureMaterial,
        MATERIAL_TYPE.FLAT.value: FlatMaterial,
        MATERIAL_TYPE.LAMBERT.value: LambertMaterial,
        MATERIAL_TYPE.PHONG.value: PhongMaterial
    }

GEOMETRY_TYPE_MAP = {
        GEOMETRY_TYPE.BOX.value: BoxGeometry,
        GEOMETRY_TYPE.SPHERE.value: Sphere,
        GEOMETRY_TYPE.CYLINDER.value: Cylinder,
        GEOMETRY_TYPE.PLANE.value: Plane,
        GEOMETRY_TYPE.RECTANGLE.value: Rectangle,
        GEOMETRY_TYPE.CIRCLE.value: Circle,
        GEOMETRY_TYPE.TRIANGLE.value: Triangle,
        # GEOMETRY_TYPE.POLYGON.value: Polygon,
        GEOMETRY_TYPE.PENTAGON.value: Pentagon,
        GEOMETRY_TYPE.HEXAGON.value: Hexagon,
        GEOMETRY_TYPE.OCTAGON.value: Octagon,
        GEOMETRY_TYPE.HEPTAGON.value: Heptagon,
        GEOMETRY_TYPE.QUAD.value: Quad,
        GEOMETRY_TYPE.CONE.value: Cone,
        GEOMETRY_TYPE.PRISM.value: Prism,
        GEOMETRY_TYPE.PYRAMID.value: Pyramid,
        GEOMETRY_TYPE.SINGLE_POINT.value: PointGeometry,
        GEOMETRY_TYPE.LINE_SEGMENT.value: LineSegment
    }

COMPONENT_FLAGS  ={
    "Physics Component": False,
    "Collider Component": False,
}

# Model For Object Spawner
class ObjectSpawnerModel:
    def __init__(self) -> None:
        self._range = [-2,2]
        self.location = [0.0, 0.0, 0.0]
        self._light_count = 0
        self.create_new_object = False
        self.geometry_type = GEOMETRY_TYPE.BOX.value
        self.material_type = MATERIAL_TYPE.SURFACE.value
        
        # Component flags - which components to add
        self.component_flags = COMPTYPE.NONE
        self.add_collider = False
        
        # Physics component settings
        self.physics_mass = 1.0
        self.physics_restitution = 0.5
        self.physics_use_gravity = True
        
        # Collider component settings
        self.collider_shape = CollisionType.SPHERE
        self.collider_radius = 1.0

    @property
    def light_count(self):
        return self._light_count
    
    @light_count.setter
    def light_count(self, value:int):
        if value < 0:
            raise ValueError("Light count must be non-negative")
        self._light_count = value
    
    def has_component(self, component: COMPTYPE) -> bool:
        """Check if a component flag is set."""
        return (self.component_flags & component) == component
    
    def toggle_component(self, component: COMPTYPE, enabled: bool):
        """Set or clear a component flag."""
        if enabled:
            self.component_flags |= component  # Set flag
        else:
            self.component_flags &= ~component  # Clear flag

# Controller For Object Spawner

# View For Object Spawner
class ObjectSpawnerView:
    def __init__(self,model:ObjectSpawnerModel) -> None:
        self.model = model
    

    def render(self):
        #   Title:
        imgui.text("Geometry Type:")
        imgui.same_line()
        imgui.text(" Material Type:")
        

        # Combos
        imgui.set_next_item_width(100)
        _,self.model.geometry_type = imgui.combo("##Geometry Type", self.model.geometry_type, 
                                            [str(geo_type) for geo_type in GEOMETRY_TYPE])

        imgui.same_line()
        imgui.set_next_item_width(100)
        _,self.model.material_type = imgui.combo("##Material Type", self.model.material_type, [str(mat_type) for mat_type in MATERIAL_TYPE])


        imgui.separator()
        imgui.text("Components:")
        
        # Physics Component checkbox
        has_physics = self.model.has_component(COMPTYPE.PHYSICS)
        _, has_physics = imgui.checkbox("Physics", has_physics)
        self.model.toggle_component(COMPTYPE.PHYSICS, has_physics)
        
        if has_physics:
            imgui.indent()
            imgui.set_next_item_width(120)
            _, self.model.physics_mass = imgui.slider_float("Mass", self.model.physics_mass, 0.1, 100.0)
            imgui.set_next_item_width(120)
            _, self.model.physics_restitution = imgui.slider_float("Bounciness", self.model.physics_restitution, 0.0, 1.0)
            _, self.model.physics_use_gravity = imgui.checkbox("Use Gravity", self.model.physics_use_gravity)
            imgui.unindent()
        
        # Collider Component checkbox
        has_collider = self.model.has_component(COMPTYPE.COLLIDER)
        _, has_collider = imgui.checkbox("Collider", has_collider)
        self.model.toggle_component(COMPTYPE.COLLIDER, has_collider)
        
        if has_collider:
            imgui.indent()
            imgui.set_next_item_width(120)
            _, self.model.collider_radius = imgui.slider_float("Radius", self.model.collider_radius, 0.1, 10.0)
            imgui.unindent()
        
        imgui.separator()
        imgui.text("Location:")
        imgui.set_next_item_width(150)
        _,self.model.location = imgui.input_float3("##Location", *self.model.location)
        



class SpawnController:
    def __init__(self, view:ObjectSpawnerView) -> None:
        self.model = view.model
        self.view = view
    
    def run(self):
        if self.model.create_new_object:
            geometry = self._create_geometry(self.model.geometry_type)
            material = self._create_material(self.model.material_type)
            mesh = Mesh(geometry=geometry, material=material)
            mesh.visible = True

            if  self.model.location[0] == 0.0 and self.model.location[1] == 0.0 and self.model.location[2] == 0.0:
                random_location = [random.uniform(self.model._range[0],self.model._range[1]) for _ in range(3)]
                mesh.set_position(random_location)
            else:
                mesh.set_position(self.model.location)

            # Create entity with mesh component (always added)
            entity = Entity()
            entity.add_component(COMPTYPE.MESH, MeshComponent(mesh=mesh))
            
            # Add physics component if flag is set
            if self.model.has_component(COMPTYPE.PHYSICS):
                physics = PhysicsBody(
                    mass=self.model.physics_mass,
                    restitution=self.model.physics_restitution,
                    use_gravity=self.model.physics_use_gravity
                )
                entity.add_component(COMPTYPE.PHYSICS, physics)
            
            # Add collider component if flag is set
            if self.model.has_component(COMPTYPE.COLLIDER):
                collider = CollisionComponent(
                    shape=self.model.collider_shape,
                    radius=self.model.collider_radius
                )
                entity.add_component(COMPTYPE.COLLIDER, collider)

            self.model.create_new_object = False
            
            return entity            
        
        return None
    
    def render(self):
        self.view.render()  
        if imgui.button("Spawn Entity"):
            self.model.create_new_object = True
    
    def _create_geometry(self,geometry_type:int):
        try:
            GEOMETRY_TYPE(geometry_type)
        except KeyError:
            raise KeyError("Invalid geometry type")

        return GEOMETRY_TYPE_MAP[geometry_type]()
    

    def _create_material(self,material_type:int):
        try:
            MATERIAL_TYPE(material_type)
        except KeyError:
            raise KeyError("Invalid material type")

        material = MATERIAL_TYPE_MAP[material_type]

        if material_type == MATERIAL_TYPE.FLAT.value or material_type == MATERIAL_TYPE.LAMBERT.value or material_type == MATERIAL_TYPE.PHONG.value:
            material = material(number_of_lights=self.model.light_count)
        else:
            material = material()

        return material