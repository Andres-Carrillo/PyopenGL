import pathlib
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")
# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[1])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)


from meshes.mesh import Mesh
from geometry.box import BoxGeometry
from material.surface import SurfaceMaterial
# from core.input import Input

import imgui
# from material.phong import PhongMaterial
from core.base import BaseApp
import random

class Test(BaseApp):
    def __init__(self, width=800, height=600):
        super().__init__(title="Testing Spawning Meshing", display_grid=True,static_camera=False, width=width, height=height)


    def update(self):
        # Example: Add ImGui UI elements
        imgui.begin("Mesh Spawning")
        if imgui.button("Create Box"):
            geo = BoxGeometry()
            surface_material = SurfaceMaterial()
            box = Mesh(geometry=geo, material=surface_material)
            x_pos = random.uniform(-5, 5)
            y_pos = random.uniform(-5, 5)
            z_pos = random.uniform(-5, 5)
            box.set_position([x_pos, y_pos, z_pos])
            self.add_to_scene(box)
        imgui.end()


    def render(self):
        # clock delta time so all objects can be updated with the same delta time
        self._tick()
        # Update the input handler
        self._handle_input()

        # if self.input_handler.right_click():
            # print(" right clicked mouse at position",self.input_handler.mouse_position)

        if self.input_handler.left_click():
            # print(" left clicked mouse at position",self.input_handler.mouse_position)
            self.scene.pick_object(self.input_handler.mouse_position, self.camera,width=self.window_width, height=self.window_height)

        
         # set the window size in case the window was resized
        self.renderer.update_window_size(self.window_width, self.window_height)
        
        # update the camera aspect ratio to avoid distortion
        self.camera.update_aspect_ratio(self.window_width / self.window_height)
        #render the scene
        self.renderer.render(self.scene, self.camera)
# Run the application
if __name__ == "__main__":
    app = Test( width=800, height=600)
    app.run()
