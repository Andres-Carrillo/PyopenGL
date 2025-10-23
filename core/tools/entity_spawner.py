import imgui
from core.meshes.mesh import Mesh

# Geometry imports
from core.geometry.geometry import GEOMETRY_TYPE
from core.geometry.simple3D.box import BoxGeometry
from core.geometry.simple3D.sphere import Sphere
from core.geometry.simple3D.cylinder import Cylinder
from core.geometry.simple3D.plane import Plane
from core.geometry.simple2D.rectangle import Rectangle
from core.geometry.simple2D.circle import Circle
from core.geometry.simple2D.triangle import Triangle
from core.geometry.simple2D.polygon import Polygon
from core.geometry.simple2D.pentagon import Pentagon
from core.geometry.simple2D.hexagon import Hexagon
from core.geometry.simple2D.octagon import Octagon
from core.geometry.simple2D.heptagon import Heptagon
from core.geometry.simple2D.quad import Quad
from core.geometry.simple3D.cone import Cone
from core.geometry.simple3D.prism import Prism
from core.geometry.simple3D.pyramid import Pyramid
from core.geometry.simple2D.point import PointGeometry
from core.geometry.simple2D.line_segment import LineSegment

# Material imports
from core.material.basic.material import MATERIAL_TYPE
from core.material.basic.surface import SurfaceMaterial
from core.material.lighted.lambert import LambertMaterial
from core.material.lighted.phong import PhongMaterial
from core.material.lighted.flat import FlatMaterial
from core.material.basic.line import LineMaterial
from core.material.basic.point import PointMaterial
from core.material.basic.sprite import Sprite
from core.material.basic.texture import TextureMaterial

import random
from core.entity import Entity
from core.components.mesh import MeshComponent
from core.components.types import Components

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



# Model For Object Spawner
class ObjectSpawnerModel:
    def __init__(self) -> None:
        self._range = [-2,2]
        self.location = [0.0, 0.0, 0.0]
        self._light_count = 0
        self.create_new_object = False
        self.geometry_type = GEOMETRY_TYPE.BOX.value
        self.material_type = MATERIAL_TYPE.SURFACE.value

    @property
    def light_count(self):
        return self._light_count
    
    @light_count.setter
    def light_count(self, value:int):
        if value < 0:
            raise ValueError("Light count must be non-negative")
        self._light_count = value

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

        imgui.text("Location:")
        imgui.same_line()
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

            entity = Entity()
            entity.add_component(Components.MESH, MeshComponent(mesh=mesh))

            self.model.create_new_object = False
            
            return entity            
        
        return None
    
    def render(self):
        self.view.render()  
        if imgui.button("Generate Mesh"):
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