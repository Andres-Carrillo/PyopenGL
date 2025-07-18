
import pathlib
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")
# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

# from core.base import ImGuiBase

from core.meshes.mesh import Mesh
from core.geometry.simple3D.box import BoxGeometry
from core.material.basic.surface import SurfaceMaterial
# from core.input import Input

from core.meshes.terrain import Terrain

# import imgui
# from material.phong import PhongMaterial
from core.base import BaseApp

# Run the application
if __name__ == "__main__":
    app = BaseApp( width=800, height=600,static_camera=False,display_grid=False)

    
    landscape = Terrain()
    # adding objects to the scene before the app is run
    box_geo = BoxGeometry()
    surface_material = SurfaceMaterial()
    box = Mesh(geometry=box_geo, material=surface_material)
    box.set_position([0, 0, 0])
    # app.add_to_scene(box)

    app.add_to_scene(landscape)


    app.run()
