import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from rendering_tests.template import Test
from core.textures.texture import Texture
from core.material.basic.texture import TextureMaterial
from core.geometry.simple2D.rectangle import  Rectangle
from core.geometry.simple3D.box import BoxGeometry
from core.geometry.simple3D.sphere import Sphere
from core.meshes.mesh import Mesh  

class TextureTest(Test):
    def __init__(self):
        super().__init__(title="Texture Test", display_grid=False)
        self.camera.set_position([0, 0, 2])
        geometry = Sphere(radius=0.5, seg_radius=128, seg_height=64)
        grid = Texture("images/lunar.jpeg")
        material = TextureMaterial(texture=grid)

        self.mesh = Mesh(geometry, material)

        self.scene.add(self.mesh)

      
    def update(self):
        self.input_handler.update()
        self.mesh.rotate_y(0.00514)
        self.mesh.rotate_x(0.00337)
        # Update the scene with the texture applied
        self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    test = TextureTest()
    test.run()
    test.quit()