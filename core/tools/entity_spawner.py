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
        GEOMETRY_TYPE.PYRAMID.value: Pyramid
    }


# View For Object Spawner
class ObjectSpawnerView:
    def __init__(self):
        self._geometry_type = GEOMETRY_TYPE.BOX.value
        self._material_type = MATERIAL_TYPE.SURFACE.value
        self._location = [0.0, 0.0, 0.0]
    
    @property
    def geometry_type(self):
        return self._geometry_type

    @property
    def material_type(self):
        return self._material_type
    
    @property
    def location(self):
        return self._location
    

    def render(self):
        #   Title:
        imgui.text("Geometry Type:")
        imgui.same_line()
        imgui.text(" Material Type:")

        # Combos
        imgui.set_next_item_width(100)
        _,self._geometry_type = imgui.combo("##Geometry Type", self._geometry_type, 
                                            [str(geo_type) for geo_type in GEOMETRY_TYPE])
        
        imgui.same_line()
        imgui.set_next_item_width(100)
        _,self._material_type = imgui.combo("##Material Type", self._material_type, [str(mat_type) for mat_type in MATERIAL_TYPE])

        imgui.text("Location:")
        imgui.same_line()
        imgui.set_next_item_width(150)
        _,self._location = imgui.input_float3("##Location", *self._location)


# Model For Object Spawner
class ObjectFactory:
    def __init__(self) -> None:
        self._range = [-2,2]
        self._location = [0.0, 0.0, 0.0]
        self._material_type = MATERIAL_TYPE.SURFACE.value
        self._geometry_type = GEOMETRY_TYPE.BOX.value
    

    def create_object(self,geometry_type:int,material_type:int,location:list[float] = None):
        geometry = self.create_geometry(geometry_type)
        material = self.create_material(material_type)
        mesh = Mesh(geometry=geometry, material=material)
        mesh.visible = True

        if  location[0] == 0.0 and location[1] == 0.0 and location[2] == 0.0:
            random_location = [random.uniform(self._range[0],self._range[1]) for _ in range(3)]
            mesh.set_position(random_location)
        else:
            mesh.set_position(location)

        entity = Entity()
        entity.add_component(Components.MESH, MeshComponent(mesh=mesh))

        print("Created object at location:", mesh.global_position)

        return entity

    def create_geometry(self,geometry_type:int):
        try:
            GEOMETRY_TYPE(geometry_type)
        except KeyError:
            raise KeyError("Invalid geometry type")

        return GEOMETRY_TYPE_MAP[geometry_type]()
    

    def create_material(self,material_type:int):
        try:
            MATERIAL_TYPE(material_type)
        except KeyError:
            raise KeyError("Invalid material type")

        material = MATERIAL_TYPE_MAP[material_type]()

        return material


# Controller For Object Spawner
class SpawnController:
    def __init__(self,model:ObjectFactory,view:ObjectSpawnerView) -> None:
        self.model = model
        self.view = view

    def spawn_object(self):
        obj = self.model.create_object(
            geometry_type=self.view.geometry_type,
            material_type=self.view.material_type,
            location=self.view.location
        )
        return obj
    

    def run(self):
        self.view.render()
        if imgui.button("Generate Mesh"):
            obj = self.spawn_object()
            return obj
        
        return None