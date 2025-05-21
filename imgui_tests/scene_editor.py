import pathlib
import sys
import warnings
import imgui
import numpy as np
import glfw.GLFW as GLFW_CONSTANTS
import random
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")
# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[1])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from tools.imgui_tools import MeshEditor
from tools.imgui_tools import ObjectSpawner
from core.base import BaseApp
from core.rendering.utils import drag_object
from core.utils.math import Math

class SceneEditor(BaseApp):
    def __init__(self, width=800, height=600):
        super().__init__(title="SceneEditor", display_grid=True,static_camera=False, width=width, height=height)
        self._is_targetting_object = False
        self.disable_camera_rig = False
        self.selected_mesh= None
        self.menu_deadzones = []
        self.mesh_editor = MeshEditor()
        self.obj_maker = ObjectSpawner()
        
    def update(self):
        self.menu_deadzones = []

        # handle object creation
        self.obj_maker.show()
        self.menu_deadzones.append(self.obj_maker.get_menu_deadzones())
        obj = self.obj_maker.get_object()
        if obj is not None:
            self.scene.add(obj)

        # handle mesh editing
        if self._is_targetting_object and self.selected_mesh is not None:
            self.mesh_editor.show()
            self.disable_camera_rig = True

            # store position of the menu to avoid mouse picking while interacting with the menu
            mesh_bbox,shader_bbox = self.mesh_editor.get_menu_deadzones()
            self.menu_deadzones.append(mesh_bbox)
            self.menu_deadzones.append(shader_bbox)


    def render(self):
        # clock delta time so all objects can be updated with the same delta time
        self._tick()
        # Update the input handler
        if not self.mesh_editor.editing_shader:
            self._handle_input()
         
         # set the window size in case the window was resized
        self.renderer.update_window_size(self.window_width, self.window_height)
        
        # update the camera aspect ratio to avoid distortion
        self.camera.update_aspect_ratio(self.window_width / self.window_height)

        if not Math.point_in_regions(self.input_handler.mouse_position, self.menu_deadzones):
        # handle mouse input
            self._handle_mouse_input()
       
        #render the scene
        self.renderer.render(self.scene, self.camera)


    def _handle_mouse_input(self):
         if self.input_handler.left_click() or self.input_handler.right_click():
            
            mesh_picked = self.scene.pick_object(self.input_handler.mouse_position, self.camera,width=self.window_width, height=self.window_height)
            
            if mesh_picked:
                self.selected_mesh = mesh_picked
                self._is_targetting_object = True
                if not self.mesh_editor.mesh:
                    self.mesh_editor.change_mesh(self.selected_mesh)

            if not mesh_picked and self.input_handler.right_click():
                self._is_targetting_object = False
                self.selected_mesh = None
                self.mesh_editor.change_mesh(None)
                self.disable_camera_rig = False
                
            if self.input_handler.left_click() and self.input_handler.mouse_held and mesh_picked:
                drag_object(mouse_position=self.input_handler.mouse_position, mesh=self.selected_mesh, camera=self.camera, 
                            width=self.window_width, height=self.window_height, input_handler=self.input_handler)
                
        
# Run the application
if __name__ == "__main__":

    app = SceneEditor( width=1280, height=720)
    app.run()
