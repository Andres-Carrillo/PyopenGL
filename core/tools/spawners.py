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

# Light imports
from core.light.directional import DirectionalLight
from core.light.point import PointLight
from core.light.ambient import AmbientLight
from core.light.light import LIGHT_TYPE

# tool imports
from core.tools.point_light_tool import PointLightTool
from core.tools.directional_light_tool import DirectionalLightTool

# import shadows
from core.light.shadow import Shadow
from core.tools.bbox import BBoxMesh
import random
import enum

from core.entity import Entity




class ObjectSpawner: 
    def __init__(self) -> None:
        self._range = None 
        self._location = None
        self._material_type = MATERIAL_TYPE.SURFACE.value
        self._geometry_type = GEOMETRY_TYPE.BOX.value
        self.show_bbox = False
        self.lights_in_scene = 0

    def set_range(self, range:list = [-2,2]):
        self._range = range

    def set_location(self, location:list = [0,0,0]):
        self._location = location

    def get_object(self):
        return self._obj
    
    def get_bbox(self):
        if self._obj is not None:
            bbox = BBoxMesh(self._obj)
            return bbox.get_bbox()
        else:
            return None

    def spawn_object(self, geometry_type:int = None, material_type:int = None, location:list = None):
        if geometry_type is not None:
            self._geometry_type = geometry_type
        if material_type is not None:
            self._material_type = material_type
        if location is not None:
            self._location = location



        return {
            "object": self._obj,
            "bbox": self.get_bbox()
        }


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



class ObjectFactory:
    def create_object(self, geometry_type:int, material_type:int, location:list):
        geometry = self.create_geometry(geometry_type)
        material = self.create_material(material_type)
        mesh = Mesh(geometry=geometry, material=material, position=location)
        
        return Entity(mesh=mesh)

    def create_geometry(self, geometry_type:int):
        try:
            GEOMETRY_TYPE(geometry_type)
        except KeyError:
            raise KeyError("Invalid geometry type")

        return GEOMETRY_TYPE_MAP[geometry_type]()


    def create_material(self, material_type:int):
        try:
            MATERIAL_TYPE(material_type)
        except KeyError:
            raise KeyError("Invalid material type")

        return MATERIAL_TYPE_MAP[material_type]()
    


class ObjectSpawner:
    """ Handles state and logic for spawning objects in the scene"""

    def __init__(self,object_factory:ObjectFactory) -> None:
        self._object_factory = object_factory 
        self.show_bbox = False
        self.object = None
        self._location = None
        self.lights_in_scene = 0

        self.material_type = MATERIAL_TYPE.SURFACE.value
        self.geometry_type = GEOMETRY_TYPE.BOX.value


    def set_location(self, location:list = [0,0,0]):
        self._location = location


    def genereate_entity(self):
        if self._location is None:
            self._location = [random.uniform(-2, 2) for _ in range(3)]

        self._object = self._object_factory.create_object(
            geometry_type=self.geometry_type,
            material_type=self.material_type,
            location=self._location
        )

        return self._object
    
    def get_spawned_data(self):
        return {
            "object": self._object,
        }
    
    def clear_object(self):
        self._object = None


class ObjectSpawnerWidget:

   