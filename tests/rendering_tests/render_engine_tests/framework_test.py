import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from core.meshes.mesh import Mesh
from core.geometry.simple3D.box import BoxGeometry
from core.material.basic.surface import SurfaceMaterial
from rendering_tests.template import Test

class FrameworkTest(Test):

    def __init__(self):
        super().__init__(title="Framework Test",display_grid=False)
        
        geometry = BoxGeometry()
        material = SurfaceMaterial(
           properties= {'use_vertex_colors':True,
             "wire_frame":False,}
        )


        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)



    def update(self):  
        self.mesh.rotate_y(0.00514)
        self.mesh.rotate_x(0.00337)
        super().update()



if __name__ == "__main__":
    test = FrameworkTest()
    test.run()
    test.quit()





