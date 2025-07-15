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
from core.geometry.simple2D.rectangle import Rectangle
from meshes.mesh import Mesh
from core.textures.text import TextTexture
from core.textures.texture import Texture
from material.basic.texture import TextureMaterial
from core.utils.matrix import Matrix


class BillboardTest(Test):

    def __init__(self):
        super().__init__(title="Billboard Test", display_grid=False)
        self.camera.set_position([0, 0, 1])

        label_texture = TextTexture(text=" This is a Crate ",
                                    system_font_name="Arial Bold",
                                    font_size=40,
                                    font_color=[0, 0, 200],
                                    image_width=256,
                                    image_height=128,
                                    align_horizontal=0.5,
                                    align_vertical=0.5,
                                    image_border_width=4,
                                    image_border_color=[255, 0, 0])

        label_material = TextureMaterial(texture=label_texture)
        label_geometry = Rectangle(width=1, height=0.5)
        label_geometry.apply_transform(Matrix.mat4_rotate_y(3.14))

        self.label = Mesh(label_geometry, label_material)
        self.label.set_position([0, 1, 0])
        self.scene.add(self.label)


        crate_geometry = BoxGeometry()
        crate_texture = Texture("images/crate.jpg")
        crate_material = TextureMaterial(texture=crate_texture)    

        crate = Mesh(crate_geometry, crate_material)

        self.scene.add(crate)



    def update(self):
        self.rig.update(self.input_handler, self.timer.delta_time())
        self.label.look_at(self.camera.global_position)
      
        self.renderer.render(self.scene, self.camera)



if __name__ == "__main__":
    test = BillboardTest()
    test.run()
 