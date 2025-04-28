import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[1])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from core.mesh import Mesh
from geometry.box import BoxGeometry
from material.surface_material import SurfaceMaterial
from tests.template import Test

class FrameworkTest(Test):

    def __init__(self):
        super().__init__(title="Framework Test")
        
        geometry = BoxGeometry()
        material = SurfaceMaterial(
            {'use_vertex_colors':True,
             "wire_frame":True,}
        )


        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)



    def update(self):
        self.mesh.rotate_y(0.00514)
        self.mesh.rotate_x(0.00337)

        self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    test = FrameworkTest()
    test.run()
    test.quit()





