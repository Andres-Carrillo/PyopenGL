import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[1])
# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

# from core.app_base import Base
from core.camera import Camera
from meshes.mesh import Mesh
from core.scene import Scene
from core.textures.texture import Texture
from geometry.box import BoxGeometry
from geometry.simple2D.rectangle import Rectangle
from material.texture import TextureMaterial
from core.textures.text import TextTexture
from tests.template import Test

class Example(Test):
    """
    Demonstrate a heads-up display (HUD): a transparent layer containing some images
    (for example, with a text), rendered after the main scene, and appearing on the top layer.
    Move the camera: WASDRF(move), QE(turn), TG(look).
    """
    def __init__(self):

        super().__init__(title="HUD Example", display_grid=True, static_camera=False)

        crate_geometry = BoxGeometry()
        crate_material = TextureMaterial(Texture("images/crate.jpg"))
        crate = Mesh(crate_geometry, crate_material)
        crate.translate(0, 0.5, 0)
        self.scene.add(crate)


        self.hud_scene = Scene()
        self.hud_camera = Camera()
        self.hud_camera.set_orthographic(0, 800, 0, 600, 1, -1)

        label_geometry1 = Rectangle(
            width=400, height=200,
            position=[0, 600],
            alignment=[0, 1]
        )
        label_material1 = TextureMaterial(Texture("images/crate-simulator.png"))
        label1 = Mesh(label_geometry1, label_material1)
        self.hud_scene.add(label1)

        label_geometry2 = Rectangle(
            width=200, height=200,
            position=[800, 0],
            alignment=[1, 0]
        )
        message = TextTexture(
            text="Version 1.0",
            system_font_name="Ink Free",
            font_size=32,
            font_color=[127, 255, 127],
            image_width=200,
            image_height=200,
            transparent=True
        )
        label_material2 = TextureMaterial(message)
        label2 = Mesh(label_geometry2, label_material2)
        self.hud_scene.add(label2)

    def update(self):

         # set the window size in case the window was resized
        self.renderer.update_window_size(self.window_width, self.window_height)
        # update the camera aspect ratio to avoid distortion
        self.camera.update_aspect_ratio(self.window_width / self.window_height)

        # update the input handler
        self.rig.update(self.input_handler, self.timer.delta_time())
        
        # render the main scene
        self.renderer.render(self.scene, self.camera)
        # Render the HUD scene
        self.renderer.render(
            scene=self.hud_scene,
            camera=self.hud_camera,
            clear_color=False
        )


# Instantiate this class and run the program
# Example(screen_size=[800, 600]).run()

if __name__ == "__main__":
    test = Example()
    test.run()
    # test.quit()
