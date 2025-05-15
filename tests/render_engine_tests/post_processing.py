import pathlib
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")
# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from tests.template import Test
from core.textures.texture import Texture
from material.basic.texture import TextureMaterial
from geometry.simple2D.rectangle import  Rectangle
from geometry.simple3D.sphere import Sphere
from meshes.mesh import Mesh  

from tools.post_processor import Postprocessor
from effects.tint import TintEffect
from effects.bright_filter import BrightFilterEffect
from effects.blur_horizontal import HBlurEffect
from effects.blur_vertical import VBlurEffect
from effects.additive_blend import AdditiveBlendEffect


class PostProcessingTest(Test):
    def __init__(self):
        super().__init__(title="Skybox Test",display_grid=False)

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
        sphere_mat = TextureMaterial(Texture("images/default_texture.jpg"))
        self.sphere_mesh = Mesh(sphere_geo, sphere_mat)
        self.sphere_mesh.set_position([0, 1, 0])
        self.scene.add(self.sphere_mesh)

        self.post_processor = Postprocessor(self.renderer, self.scene, self.camera)
        self.blur_effect = HBlurEffect(texture_size=[self.window_width, self.window_height], blur_radius=50)
        self.vertical_blur_effect = VBlurEffect(texture_size=[self.window_width, self.window_height], blur_radius=50)

        self.post_processor.add_effect(BrightFilterEffect(2.4))
        self.post_processor.add_effect(self.blur_effect)
        self.post_processor.add_effect(self.vertical_blur_effect)

        main_scene = self.post_processor.render_target_list[0].texture

        self.post_processor.add_effect(AdditiveBlendEffect(blend_texture=main_scene, src_strength=2, blend_strength=1))



    def update(self) -> None:
        self._base_update()
        self.blur_effect.uniforms["texture_size"].data = [self.window_width, self.window_height]
        self.vertical_blur_effect.uniforms["texture_size"].data = [self.window_width, self.window_height]

        self.post_processor.render()


if __name__ == "__main__":
    test = PostProcessingTest()
    test.run()
    test.quit()