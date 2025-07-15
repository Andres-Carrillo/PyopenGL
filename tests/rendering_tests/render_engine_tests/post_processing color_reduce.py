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
from core.textures.texture import Texture
from core.material.basic.texture import TextureMaterial
from core.geometry.simple2D.rectangle import  Rectangle
from core.geometry.simple3D.sphere import Sphere
from core.meshes.mesh import Mesh  

from tools.post_processor import Postprocessor
from core.effects.color_reduce import ColorReduceEffect


class ColorReduceTest(Test):
    def __init__(self):
        super().__init__(title="Color Reduction Test",display_grid=False)

        sky_geo = Sphere(radius=50)
        sky_mat = TextureMaterial(Texture("images/sky.jpg"))
        sky = Mesh(sky_geo, sky_mat)
        self.scene.add(sky)

        grass_geo = Rectangle(width=self.camera.far, height=self.camera.far)
        grass_mat = TextureMaterial(Texture("images/grass.jpg"),
                                    properties={"repeat_uv": [50,50]})
        
        grass = Mesh(grass_geo, grass_mat)
        grass.rotate_x(-3.14/2)

        self.scene.add(grass)


        sphere_geo = Sphere()
        sphere_mat = TextureMaterial(Texture("images/grid.jpg"))
        self.sphere_mesh = Mesh(sphere_geo, sphere_mat)
        self.sphere_mesh.set_position([0, 1, 0])
        self.scene.add(self.sphere_mesh)

        self.post_processor = Postprocessor(self.renderer, self.scene, self.camera)

        self.post_processor.add_effect(ColorReduceEffect())



    def update(self) -> None:
        self._base_update()
        self.post_processor.render()


if __name__ == "__main__":
    test = ColorReduceTest()
    test.run()
    test.quit()