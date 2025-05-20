import imgui
from meshes.mesh import Mesh
import math
from core.utils.openGLUtils import GlUtils
from core.glsl.uniform import UNIFORM_TYPE
from core.glsl.uniform import Uniform

def draw_mesh_uniform_editor(mesh):
    # display the mesh's current uniforms and allow the user to edit them
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
    # display the mesh's current material settings and allow the user to edit them
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

def draw_uniform_maker(uniform_name:str = "", uniform_type:int = 0, uniform_data:str = ""):
    # draw a window to create a new uniform
    make = False
    imgui.text("Create a new uniform:")
    imgui.separator()
    _,new_uniform_data = imgui.input_text("Uniform Data", uniform_data)
    _,new_uniform_name = imgui.input_text("Uniform Name", uniform_name)
    _, new_uniform_type = imgui.combo("Uniform Type", uniform_type, [str(type) for type in UNIFORM_TYPE])
    if imgui.button("Create"):
        make = True
        # self.mesh.material.add_uniform(uniform_name, uniform_type)
        # print("create a new uniform")
        # draw_uniform_maker()
    imgui.separator()

    return new_uniform_name, new_uniform_type, new_uniform_data, make


class ShaderEditor:
    def __init__(self, mesh: Mesh = None,window_width:int = 800, window_height:int = 300,embedded:bool = False):
        self.embedded = embedded
        self.window_width = window_width
        self.window_height = window_height
        self.show_editor = False
        self.compile_error = False
        self.edit_uniforms = False
        self.creating_uniform = False
        self.temp_uniform_type = 0
        self.temp_uniform_name = ""
        self.temp_uniform_data = ""
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
            
            imgui.separator()
            if self.edit_uniforms:
                imgui.text("Edit Uniforms:")
                imgui.separator()
                draw_mesh_uniform_editor(self.mesh)
                imgui.separator()

                
                # handle adding a new uniform to the mesh material
                if imgui.button("Add a new Uniform"):
                    self.creating_uniform = True

                if self.creating_uniform:
                    self.temp_uniform_name,self.temp_uniform_type, self.temp_uniform_data,add_uniform = draw_uniform_maker(uniform_name=self.temp_uniform_name, uniform_type=self.temp_uniform_type, uniform_data=self.temp_uniform_data)
                
                    if add_uniform:
                        uniform_data =  GlUtils.make_uniform_data( UNIFORM_TYPE(self.temp_uniform_type), self.temp_uniform_data)
                        self.mesh.material.add_uniform(self.temp_uniform_name,  uniform_data,str(UNIFORM_TYPE(self.temp_uniform_type)))
                        self.mesh.material.locate_uniforms()    
                        
                        # reset the buffers
                        self.creating_uniform = False
                        self.temp_uniform_name = ""
                        self.temp_uniform_data = ""
                        self.temp_uniform_type = 0

                imgui.separator()
                # imgui.same_line()
                if imgui.button("Done"):
                    self.edit_uniforms = False



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
                self.edit_uniforms = not self.edit_uniforms
                # print("Edit Uniforms")

            window_pos = imgui.get_window_position()
            window_size = imgui.get_window_size()
            self.menu_bbox = [window_pos[0], window_pos[1], window_pos[0] + window_size[0], window_pos[1] + window_size[1]]
    
    
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
        self.shader_editor = ShaderEditor(mesh,embedded=True)
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
