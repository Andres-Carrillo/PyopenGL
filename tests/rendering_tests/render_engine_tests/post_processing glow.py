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
from material.basic.texture import TextureMaterial
from core.geometry.simple2D.rectangle import  Rectangle
from core.geometry.simple3D.sphere import Sphere
from meshes.mesh import Mesh  

from tools.post_processor import Postprocessor
from core.effects.tint import TintEffect
from core.effects.bright_filter import BrightFilterEffect
from core.effects.blur_horizontal import HBlurEffect
from core.effects.blur_vertical import VBlurEffect
from core.effects.additive_blend import AdditiveBlendEffect
from core.rendering.scene import Scene
from material.basic.surface import SurfaceMaterial
from core.rendering.render_target import RenderTarget
from math import sin,cos

class PostProcessingTest(Test):
    def __init__(self):
        super().__init__(title="Glow Test",display_grid=False)
        
        

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
        self.glow_scene = Scene()

        red_mat = SurfaceMaterial(properties={"base_color":[1.0,0.5,1.0]})

        

        self.glow_sphere = Mesh(sphere_geo, red_mat)
        self.glow_sphere._matrix = self.sphere_mesh._matrix

        self.glow_scene.add(self.glow_sphere)

        glow_target = RenderTarget(resolution=[self.window_width, self.window_height])
        self.glow_pass = Postprocessor(self.renderer, self.glow_scene, self.camera, render_target=glow_target)

        self.h_blur_effect = HBlurEffect(texture_size=[self.window_width, self.window_height], blur_radius=50)
        self.v_blur_effect = VBlurEffect(texture_size=[self.window_width, self.window_height], blur_radius=50)
        self.glow_pass.add_effect(self.h_blur_effect)
        self.glow_pass.add_effect(self.v_blur_effect)

        # combne glow with main scene
        self.combo_pass = Postprocessor(self.renderer, self.scene, self.camera)

        self.combo_pass.add_effect(AdditiveBlendEffect(blend_texture=glow_target.texture, src_strength=1, blend_strength=4))

        # self.post_processor.add_effect(AdditiveBlendEffect(blend_texture=main_scene, src_strength=2, blend_strength=1))



    def update(self) -> None:
        self._base_update()
        self.sphere_mesh.rotate_y(0.01337)
        self.h_blur_effect.uniforms["texture_size"].data = [self.window_width, self.window_height]
        self.v_blur_effect.uniforms["texture_size"].data = [self.window_width, self.window_height]

        self.glow_sphere.material.uniforms["base_color"].data = [sin(self.timer.elapsed_time()), 1, 1]    
        # self.post_processor.render()
        self.glow_pass.render()
        self.combo_pass.render()



if __name__ == "__main__":
    test = PostProcessingTest()
    test.run()
    test.quit()