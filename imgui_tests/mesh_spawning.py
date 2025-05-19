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
from geometry.simple3D.box import BoxGeometry
from geometry.simple3D.sphere import Sphere
from geometry.simple3D.cylinder import Cylinder
from geometry.simple3D.plane import Plane
from material.basic.surface import SurfaceMaterial
from material.lighted.lambert import LambertMaterial
from material.lighted.phong import PhongMaterial
from material.lighted.flat import FlatMaterial
from tools.imgui_tools import MeshEditor
# from core.input import Input

import imgui
# from material.phong import PhongMaterial
from core.base import BaseApp
import random
import math

from core.utils.math import Math as RenderMath

import numpy as np

import glfw.GLFW as GLFW_CONSTANTS

EDIT_SHADERS = False

def rodrigues_rotation_matrix(axis, theta):
    """
    Returns the rotation matrix using Rodrigues' rotation formula.
    axis: 3-element array-like, should be normalized
    theta: rotation angle in radians
    """
    axis = np.asarray(axis, dtype=np.float64)
    axis = axis / np.linalg.norm(axis)
    K = np.array([
        [0, -axis[2], axis[1]],
        [axis[2], 0, -axis[0]],
        [-axis[1], axis[0], 0]
    ])
    I = np.eye(3)
    R = I + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)
    # Convert to 4x4 matrix
    R4 = np.eye(4)
    R4[:3, :3] = R
    return R4


def ray_plane_intersection(ray_origin, ray_direction, plane_point, plane_normal):
    """
    Find the intersection point of a ray and a plane.
    ray_origin: np.array([x, y, z]) - origin of the ray (camera position)
    ray_direction: np.array([dx, dy, dz]) - normalized direction of the ray
    plane_point: np.array([x, y, z]) - a point on the plane (e.g., object's original position)
    plane_normal: np.array([nx, ny, nz]) - normal vector of the plane (e.g., [0, 1, 0] for y=constant)
    Returns: intersection point as np.array([x, y, z]) or None if no intersection
    """
    ray_direction = ray_direction / np.linalg.norm(ray_direction)
    denom = np.dot(plane_normal, ray_direction)
    if abs(denom) < 1e-6:
        return None  # Ray is parallel to the plane
    t = np.dot(plane_point - ray_origin, plane_normal) / denom
    if t < 0:
        return None  # Intersection is behind the ray origin
    intersection = ray_origin + t * ray_direction
    return intersection

def choose_drag_plane(ray_direction, mesh_position):
    # Find the axis least aligned with the ray direction
    abs_dir = np.abs(ray_direction)
    # The axis with the smallest component is the best normal
    axis = np.argmin(abs_dir)
    if axis == 0:
        # X is the best normal, so use the YZ plane (normal [1,0,0])
        plane_normal = np.array([1, 0, 0])
        plane_point = np.array(mesh_position)
    elif axis == 1:
        # Y is the best normal, so use the XZ plane (normal [0,1,0])
        plane_normal = np.array([0, 1, 0])
        plane_point = np.array(mesh_position)
    else:
        # Z is the best normal, so use the XY plane (normal [0,0,1])
        plane_normal = np.array([0, 0, 1])
        plane_point = np.array(mesh_position)
    return plane_point, plane_normal


def drag_object(mouse_position, mesh, camera,width,height,input_handler):
  # Get ray origin and direction from your camera and mouse
    ray_origin = np.array(camera.global_position)  # or self.camera.global_position
    ray_direction = RenderMath.ray_cast(mouse_position, camera, width, height)

    if input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_1):
        plane_point = np.array([0, mesh.global_position[1], mesh.global_position[2]])
        plane_normal = np.array([1, 0, 0])
    else:
        plane_point = np.array([mesh.global_position[0], mesh.global_position[1], 0])
        plane_normal = np.array([0, 0, 1])
    
    new_pos = ray_plane_intersection(ray_origin, ray_direction, plane_point, plane_normal)

    if new_pos is not None:
            mesh.set_position(new_pos)


class Test(BaseApp):
    def __init__(self, width=800, height=600):
        super().__init__(title="Testing Spawning Meshing", display_grid=True,static_camera=False, width=width, height=height)
        self._is_targetting_object = False
        self.selected_mesh= None
        self._geometry_type = None
        self._material_type = None
        self.mesh_editor = MeshEditor()
        self.disable_camera_rig = False


    def update(self):
        # Example: Add ImGui UI elements
        imgui.begin("Mesh Spawning")
        if imgui.button("Spawn Mesh"):
            geo = BoxGeometry()
            surface_material = SurfaceMaterial()
            box = Mesh(geometry=geo, material=surface_material)
            x_pos = random.uniform(-5, 5)
            y_pos = random.uniform(-5, 5)
            z_pos = random.uniform(-5, 5)
            box.set_position([x_pos, y_pos, z_pos])
            self.add_to_scene(box)
        imgui.end()

        if self._is_targetting_object and self.selected_mesh is not None:
            self.mesh_editor.show()
            self.disable_camera_rig = True

    def render(self):
        # clock delta time so all objects can be updated with the same delta time
        self._tick()
        # Update the input handler
        if not self.disable_camera_rig:
            self._handle_input()
         
         # set the window size in case the window was resized
        self.renderer.update_window_size(self.window_width, self.window_height)
        
        # update the camera aspect ratio to avoid distortion
        self.camera.update_aspect_ratio(self.window_width / self.window_height)


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
                
    app = Test( width=800, height=600)
    app.run()
