import imgui
from meshes.mesh import Mesh
import math

def draw_mesh_uniform_editor(mesh):

    # display the mesh material properties
    imgui.separator()
    open_header, _ = imgui.collapsing_header(mesh.material.material_type + " Uniforms")
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


def draw_material_settings(mesh):
    imgui.separator()
    open_header, _ = imgui.collapsing_header(mesh.material.material_type + " Settings")
    if open_header:
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

class ShaderEditor:
    def __init__(self, mesh: Mesh = None,window_width:int = 800, window_height:int = 300):
        self.window_width = window_width
        self.window_height = window_height
        self.show_editor = False
        self.compile_error = False
        self.mesh = mesh
        self.menu_bbox = [0, 0, 0, 0]
        self.error_message = ""

        if mesh:
            self.vertex_shader = self.mesh.materia.vertex_shader
            self.fragment_shader = self.mesh.material.fragment_shader
        else:
            self.vertex_shader = """"""
            self.fragment_shader = """"""

    # for setting a new mesh without having to recompile the shaders or create a new editor
    def change_mesh(self, mesh: Mesh = None):
        self.mesh = mesh
        if mesh:
            self.vertex_shader = self.mesh.material.vertex_shader
            self.fragment_shader = self.mesh.material.fragment_shader
        else:
            self.vertex_shader = """"""
            self.fragment_shader = """"""

    def show(self):
        if self.show_editor:
            imgui.begin("Shader Editor", imgui.WINDOW_ALWAYS_AUTO_RESIZE)
            imgui.separator()
            imgui.text("Vertex Shader Editor:")
            imgui.separator()
            _, self.vertex_shader = imgui.input_text_multiline("", self.vertex_shader, 1024 * 16, self.window_width, self.window_height)
            
            imgui.separator()
            imgui.text("Fragment Shader Editor:")
            imgui.separator()
            _, self.fragment_shader = imgui.input_text_multiline(" ", self.fragment_shader, 1024 * 16, self.window_width, self.window_height)

            if self.compile_error:
                imgui.separator()
                imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.0, 0.0, 1.0)
                imgui.text("Error compiling shaders:")
                imgui.text(self.error_message)
                imgui.pop_style_color()
                imgui.separator()
                imgui.text("Please check the shader code and try again.")
                
            if(imgui.button("Compile")):
                self.compile_shaders()

            imgui.same_line()   
            if(imgui.button("Edit Uniforms")):
                print("Edit Uniforms")

            window_pos = imgui.get_window_position()
            window_size = imgui.get_window_size()
            self.menu_bbox = [window_pos[0], window_pos[1], window_pos[0] + window_size[0], window_pos[1] + window_size[1]]

            imgui.end()

    def compile_shaders(self):
        try:
            self.mesh.material.compile_shaders(self.vertex_shader, self.fragment_shader)
            self.compile_error = False
            self.error_message = ""
        except Exception as e:
            self.error_message = str(e)
            print("Error compiling shaders:", e)
            self.compile_error = True


    def get_menu_deadzones(self):
        return self.menu_bbox

class MeshEditor:
    def __init__(self, mesh: Mesh = None):
        self.mesh = mesh
        self.shader_editor = ShaderEditor(mesh)
        self.menu_bbox = [0, 0, 0, 0]

    def change_mesh(self, mesh: Mesh = None):
        self.mesh = mesh
        self.shader_editor.change_mesh(mesh)

    def show(self):
        imgui.begin("Mesh Editor")  # Start a new ImGui window for the mesh editor
        imgui.text("{}".format(self.mesh.geometry.object_type))

        # Display the mesh's current position and allow the user to edit it
        draw_position_editor(self.mesh)

        # Display the mesh's current rotation and allow the user to edit it
        draw_rotation_editor(self.mesh)

        draw_mesh_uniform_editor(self.mesh)

        draw_material_settings(self.mesh)

        imgui.separator()
        if imgui.button("Edit Shaders"):
            self.shader_editor.show_editor = not self.shader_editor.show_editor

        window_pos = imgui.get_window_position()
        window_size = imgui.get_window_size()
        self.menu_bbox = [window_pos[0], window_pos[1], window_pos[0] + window_size[0], window_pos[1] + window_size[1]]

        imgui.end()  # End the mesh editor window

        if self.shader_editor.show_editor:
            # Open the shader editor window
            self.shader_editor.show()


    def get_menu_deadzones(self):
        # return the menu bounding box for the mesh editor and shader editor
        return [self.menu_bbox, self.shader_editor.menu_bbox]    
