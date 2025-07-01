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
    def __init__(self, u_start: float = -100, u_end: float = 100, u_resolution: int = 50,
                 v_start: float = -100, v_end: float = 100, v_resolution: int = 50,
                 surface_functions=None) -> None:
        
        noise = PerlinNoise(octaves=3, seed=42)
        if surface_functions is None:
            def surface_function(u,v):
                return [u + noise([u,v]) * 0.3,sin(u*v),v + noise([u,v]) * 0.1]  # Oscillation only affects the y axis

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


class InfiniteTerrainManager:
    def __init__(self,chunk_size:int =100, view_distance:int = 3,u_resolution:int = 100, v_resolution:int = 100):
        self.chunk_size = chunk_size
        self.view_distance = view_distance
        self.u_resolution = u_resolution
        self.v_resolution = v_resolution
        self.chunks = {}


    def update(self,camera_position):
        current_chunk_x = int(camera_position[0] // self.chunk_size)
        current_chunk_z = int(camera_position[2] // self.chunk_size)

        needed_chunks = set()

        # print(f"Current chunk: ({current_chunk_x}, {current_chunk_z})")

        # print("dx ranges from -view_distance to view_distance:", self.view_distance)
        # print("dz ranges from -view_distance to view_distance:", self.view_distance)

        for dx in range(-self.view_distance,self.view_distance + 1):
            # print(f"Checking chunk: ({current_chunk_x + dx}, {current_chunk_z})")
            for dz in range(-self.view_distance,self.view_distance + 1):
                # print(f"Checking chunk: ({current_chunk_x + dx}, {current_chunk_z + dz})")
                needed_chunks.add((current_chunk_x + dx, current_chunk_z + dz))

        # print(f"Needed chunks: {len(needed_chunks)}")
        # Unload chunks that are no longer needed
        for chunk_key in list(self.chunks.keys()):
            if chunk_key not in needed_chunks:
                # print(f"Unloading chunk: {chunk_key}")
                self.unload_chunk(chunk_key)

        # Load any new chunks that are needed
        # print(f"Loading chunks: {len(needed_chunks)}")

        # print(f"view_distance: {self.view_distance}")
        # print(f"current_chunk: ({current_chunk_x}, {current_chunk_z})")
        # print(f"needed_chunks: {needed_chunks}")
        # print(f"currently loaded chunks: {list(self.chunks.keys())}")
        for chunk_key in needed_chunks:
            if chunk_key not in self.chunks:
                # print(f"Loading chunk: {chunk_key}")
                self.load_chunk(chunk_key)



    def load_chunk(self, chunk_key):
        chunk_x, chunk_z = chunk_key
        u_start = chunk_x * self.chunk_size
        u_end = u_start + self.chunk_size
        v_start = chunk_z * self.chunk_size
        v_end = v_start + self.chunk_size

        # set u and v resoltion based on chunk distance from the camera
        geometry = Terrain_Geometry(u_start=u_start, u_end=u_end, u_resolution=self.u_resolution,
                                    v_start=v_start, v_end=v_end, v_resolution=self.v_resolution)

        terrain = Terrain(geometry=geometry)
        self.chunks[chunk_key] = terrain


    def unload_chunk(self, chunk_key):
        if chunk_key in self.chunks:
            del self.chunks[chunk_key]
        else:
            print(f"Chunk {chunk_key} not found.")
