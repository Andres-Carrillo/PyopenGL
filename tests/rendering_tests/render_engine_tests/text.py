import pathlib
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")
# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from rendering_tests.template import Test
from core.geometry.simple3D.box import BoxGeometry
from rendering_tests.template import Test
from meshes.mesh import Mesh
from core.textures.text import TextTexture
from core.material.basic.texture import TextureMaterial

class TextureTest(Test):
    def __init__(self):
        super().__init__(title="Texture Test", display_grid=False)
        self.camera.set_position([0,0,1])
        geometry = BoxGeometry(width=2,height=2,depth=2)

        message = TextTexture(text="Python 3D",
                              system_font_name="Impact",
                              font_size=32,
                              font_color=[0, 0, 200],
                              image_width=256,
                              image_height=256,
                              align_horizontal=0.5,
                              align_vertical=0.5,
                              image_border_width=4,
                              image_border_color=[255, 0, 0],transparent=False)
        
        material = TextureMaterial(texture=message)
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
    # test.quit()