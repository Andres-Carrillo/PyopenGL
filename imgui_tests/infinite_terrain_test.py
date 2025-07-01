
import pathlib
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")
# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[1])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

# from core.base import ImGuiBase

from meshes.mesh import Mesh
from geometry.simple3D.box import BoxGeometry
from material.basic.surface import SurfaceMaterial
# from core.input import Input
from core.base import SceneEditor
from meshes.terrain import Terrain, InfiniteTerrainManager

# import imgui
# from material.phong import PhongMaterial
from core.base import BaseApp

# Run the application
if __name__ == "__main__":
    app = SceneEditor( width=800, height=600,display_grid=False,static_camera=False)

    
    # landscape = Terrain()
    # adding objects to the scene before the app is run
    box_geo = BoxGeometry()
    terrian_manager = InfiniteTerrainManager(chunk_size=100, view_distance=3, u_resolution=10, v_resolution=10)
    surface_material = SurfaceMaterial()
    box = Mesh(geometry=box_geo, material=surface_material)
    box.set_position([0, 0, 0])
    # app.set_terrain_manager(terrian_manager)
    # app.add_to_scene(box)

    # app.add_to_scene(landscape)


    app.run()
