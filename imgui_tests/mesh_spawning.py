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
from geometry.sphere import Sphere
from geometry.cylinder import Cylinder
from geometry.plane import Plane
from material.surface import SurfaceMaterial
from material.lambert import LambertMaterial
from material.phong import PhongMaterial
from material.flat import FlatMaterial
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


def shader_editor(mesh,vertex_source=None,fragment_source=None):
    if vertex_source is None:
        vertex_source = mesh.material.vertex_shader
    # vertex_buffer_len
    print("vertex source",vertex_source)

    if fragment_source is None:
            fragment_source = mesh.material.fragment_shader
    print("fragment source",fragment_source)
    input_width = 700
    input_height = 400
    
    # Open the shader editor window
    imgui.begin("Shader Editor")

    imgui.separator()
    changed_v,new_vertex_code = imgui.input_text_multiline(" ", vertex_source, 2048, input_width,input_height)
    vertex_source =  new_vertex_code if changed_v else None
    
    imgui.separator()
    changed_f,new_vertex_code = imgui.input_text_multiline("", fragment_source, 2048,input_width, input_height)
    fragment_source =  new_vertex_code if changed_f else None
    
    imgui.separator()
    if imgui.button("Compile Shaders"):
        mesh.material.compile_shaders(vertex_source, fragment_source)
    # imgui.text("Edit the shaders here...")

    # Add your shader editing UI here
    imgui.end()

    return vertex_source, fragment_source


def draw_mesh_property_editor(mesh):

    # display the mesh material properties
    imgui.separator()
    open_header, _ = imgui.collapsing_header(mesh.material.material_type + " Material Properties")
    if open_header:
        for key, value in mesh.material.uniforms.items():
            if key in ("model_matrix", "view_matrix", "projection_matrix"):
                continue
            if key == "use_vertex_colors":
                changed, new_value = imgui.checkbox("Use Vertex Color", value.data)
                imgui.same_line()
                if changed:
                    mesh.material.uniforms[key].data = new_value
            if key == "wire_frame":
                changed, new_value = imgui.checkbox("Wire Frame", value.data)
                imgui.same_line()
                if changed:
                    mesh.material.uniforms[key].data = new_value
            if key == "base_color":
                changed, new_color = imgui.color_edit4("Base Color", value.data[0], value.data[1], value.data[2], 1.0)
                if changed:
                    mesh.material.set_properties({"base_color": new_color})

        for key, value in mesh.material.settings.items():
            if key == "wire_frame":
                changed, new_value = imgui.checkbox("Wire Frame", value)
                imgui.same_line()
                if changed:
                    mesh.material.settings[key] = new_value
            if mesh.material.settings.get('wire_frame', False) and key == "line_width":
                changed, new_value = imgui.slider_float("Line Width", value, 0.1, 10.0)
                if changed:
                    mesh.material.settings[key] = new_value
            if key == "double_sided":
                changed, new_value = imgui.checkbox("Double Sided", value)
                imgui.same_line()
                if changed:
                    mesh.material.settings[key] = new_value


def draw_position_editor(mesh):
     # Display the mesh's current position and allow the user to edit it
    imgui.separator()
    open_header, _ = imgui.collapsing_header("Position transform")
    if open_header:
        changed_x, new_x_pos = imgui.input_int("X Position##pos", mesh.global_position[0])
        changed_y, new_y_pos = imgui.input_int("Y Position##pos", mesh.global_position[1])
        changed_z, new_z_pos = imgui.input_int("Z Position##pos", mesh.global_position[2])
        if changed_x or changed_y or changed_z:
            mesh.set_position([new_x_pos, new_y_pos, new_z_pos])

def draw_rotation_editor(mesh,range =(-math.pi, math.pi)):
    imgui.separator()
    open_header, _ = imgui.collapsing_header("Rotation transform")
    if open_header:
        x_rot_changed, new_x_rot = imgui.slider_float("X Rotation", mesh.ueler_angles[0], range[0], range[1])
        y_rot_changed, new_y_rot = imgui.slider_float("Y Rotation", mesh.ueler_angles[1], range[0], range[1])
        z_rot_changed, new_z_rot = imgui.slider_float("Z Rotation", mesh.ueler_angles[2], range[0], range[1])
        if x_rot_changed or y_rot_changed or z_rot_changed:
            mesh.set_euler_rotation([new_x_rot*360, new_y_rot*360, new_z_rot*360])
    
def mesh_editor(mesh):
    global EDIT_SHADERS

    imgui.begin("Mesh Editor")  # Start a new ImGui window for the mesh editor
    imgui.text("{}".format(mesh.geometry.object_type))

    # Display the mesh's current position and allow the user to edit it
    draw_position_editor(mesh)

    # Display the mesh's current rotation and allow the user to edit it
    draw_rotation_editor(mesh)
   
    draw_mesh_property_editor(mesh)

    imgui.separator()
    if imgui.button("Edit Mesh"):
        EDIT_SHADERS = not EDIT_SHADERS

    imgui.end()  # End the mesh editor window

    if EDIT_SHADERS:
        # Open the shader editor window
        shader_editor(mesh)

class Test(BaseApp):
    def __init__(self, width=800, height=600):
        super().__init__(title="Testing Spawning Meshing", display_grid=True,static_camera=False, width=width, height=height)
        self._is_targetting_object = False
        self.selected_mesh= None
        self._geometry_type = None
        self._material_type = None


    def update(self):
        # Example: Add ImGui UI elements
        imgui.begin("Mesh Spawning")
        if imgui.button("Span Mesh"):
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
            mesh_editor(self.selected_mesh)


    def render(self):
        # clock delta time so all objects can be updated with the same delta time
        self._tick()
        # Update the input handler
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
            # print(" left clicked mouse at position",self.input_handler.mouse_position)
            
            mesh_picked = self.scene.pick_object(self.input_handler.mouse_position, self.camera,width=self.window_width, height=self.window_height)
            
            if mesh_picked:
                self.selected_mesh = mesh_picked
                self._is_targetting_object = True

            if not mesh_picked and self.input_handler.right_click():
                self._is_targetting_object = False
                self.selected_mesh = None
                

            if self.input_handler.left_click() and self.input_handler.mouse_held and mesh_picked:
                drag_object(mouse_position=self.input_handler.mouse_position, mesh=self.selected_mesh, camera=self.camera, 
                            width=self.window_width, height=self.window_height, input_handler=self.input_handler)


# Run the application
if __name__ == "__main__":
                
    app = Test( width=800, height=600)
    app.run()
