from meshes.mesh import Mesh
from geometry.geometry import Geometry
from material.basic.line import LineMaterial
from material.basic.surface import SurfaceMaterial
from geometry.simple3D.box import generate_box_vertices
import cv2 as cv
from geometry.parametric import Parametric
from math import sin, cos
from perlin_noise import PerlinNoise

# will gernerate terrain as a parametric surface

class Terrain_Geometry(Parametric):
    def __init__(self, u_start: float = -100, u_end: float = 100, u_resolution: int = 100,
                 v_start: float = -100, v_end: float = 100, v_resolution: int = 100,
                 surface_functions=None) -> None:
        
        noise = PerlinNoise(octaves=15, seed=2)
        if surface_functions is None:
            def surface_function(u,v):
                return [u ,sin(u*v) + noise([u,v]),v ]  # Oscillation only affects the y axis

            surface_functions = surface_function
        super().__init__(u_start, u_end, u_resolution, v_start, v_end, v_resolution, surface_functions)




class Terrain(Mesh):
    def __init__(self, geometry: Terrain_Geometry = None, material: SurfaceMaterial = None, hieght_map_source: str = None):

        if geometry is None:
            geometry = Terrain_Geometry()
        if material is None:
            material = SurfaceMaterial(properties={
                "use_vertex_colors": False,
                # "use_texture": False,
                # "texture_path": None,
                "base_color": [0.5, 0.5, 0.5],
                "wire_frame": True,
                "double_sided": True,
            })

        super().__init__(geometry=geometry, material=material)

        if hieght_map_source is not None:
            self.set_height_map(hieght_map_source)

    def set_height_map(self, height_map_source: str):
        height_map = cv.imread(height_map_source, cv.IMREAD_GRAYSCALE)
        self.geometry.set_height_map(height_map)
