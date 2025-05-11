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
from core.rendering.render_target import RenderTarget
from geometry.simple3D.box import BoxGeometry
from material.basic.surface import SurfaceMaterial
from core.rendering.camera import Camera

class SkyboxTest(Test):
    def __init__(self):
        super().__init__(title="Skybox Test",display_grid=False)
        sky_geo = Sphere(radius=50)
        sky_mat = TextureMaterial(Texture("images/sky.jpg"))
        sky = Mesh(sky_geo, sky_mat)
        self.scene.add(sky)

        grass_geo = Rectangle(width=self.camera.far, height=self.camera.far)
        grass_mat = TextureMaterial(Texture("images/grass.jpg"))
        grass = Mesh(grass_geo, grass_mat)
        grass.rotate_x(-3.14/2)

        self.scene.add(grass)

        sphere_geo = Sphere()
        sphere_mat = TextureMaterial(Texture("images/grid.jpg"))
        self.sphere_mesh = Mesh(sphere_geo, sphere_mat)
        self.sphere_mesh.set_position([-1.2, 1, 0])
        self.scene.add(self.sphere_mesh)

        box_geo = BoxGeometry(width=2,height=2,depth=0.2)
        box_mat = SurfaceMaterial({"base_color": [0, 0, 0]})
        box = Mesh(box_geo, box_mat)
        box.set_position([1.2, 1, 0])
        self.scene.add(box)

        # Create a render target for the second camera
        self.render_target = RenderTarget(resolution=[self.window_width, self.window_height])

        screen_geo = Rectangle(width=1.8, height=1.8)
        screen_mat = TextureMaterial(self.render_target.texture)
        self.screen = Mesh(screen_geo, screen_mat)
        self.screen.set_position([1.2, 1, 0.11])
        self.scene.add(self.screen)
        # Set up the second camera
        self.sky_cam = Camera(aspect_ratio=self.window_width/self.window_height)
        self.sky_cam.set_position([0, 10, 0.1])
        self.sky_cam.look_at([0, 0, 0])
        self.scene.add(self.sky_cam)

    def update(self) -> None:
        # set the window size in case the window was resized
        self.renderer.update_window_size(self.window_width, self.window_height)
        # self.render_target.update_window_size(self.window_width, self.window_height)
        # update the camera aspect ratio to avoid distortion
        self.camera.update_aspect_ratio(self.window_width / self.window_height)
        # self.sky_cam.update_aspect_ratio(self.window_width / self.window_height)
        self.sphere_mesh.rotate_y(0.00514)

        # update the input handler
        if self.rig is not None:
            self.rig.update(self.input_handler, self.timer.delta_time())

        self.renderer.render(self.scene, self.sky_cam, render_target=self.render_target)
        # render the scene        
        self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    test = SkyboxTest()
    test.run()
    test.quit()