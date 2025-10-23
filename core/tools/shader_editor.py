from core.meshes.mesh import Mesh
import imgui
from core.utils.openGLUtils import GlUtils
from core.glsl.uniform import UNIFORM_TYPE

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

    imgui.separator()

    return new_uniform_name, new_uniform_type, new_uniform_data, make

class ShaderEditorModel:
    def __init__(self, mesh: Mesh = None):
        self.mesh = mesh
        self.window_width = 1000
        self.window_height = 300
        self.show_editor = False
        self.compile_error = False
        self.edit_uniforms = False
        self.creating_uniform = False
        self.compile_shaders = False
        self.error_message = ""
        self.temp_uniform_type = 0
        self.temp_uniform_name = ""
        self.temp_uniform_data = ""
        self.menu_bbox = [0, 0, 0, 0]   



class ShaderEditorView:
    def __init__(self, model:ShaderEditorModel):
        self.model = model


    def render(self):
        open_header, _ = imgui.collapsing_header("Shader Editor")
        if open_header: 
            imgui.separator()
            if self.model.edit_uniforms:
                imgui.text("Edit Uniforms:")
                imgui.separator()
                draw_mesh_uniform_editor(self.model.mesh)
                imgui.separator()

                
                # handle adding a new uniform to the mesh material
                if imgui.button("Add a new Uniform"):
                    self.model.creating_uniform = True

                if self.model.creating_uniform:
                    self.model.temp_uniform_name,self.model.temp_uniform_type, self.model.temp_uniform_data,add_uniform = draw_uniform_maker(uniform_name=self.model.temp_uniform_name, uniform_type=self.model.temp_uniform_type, uniform_data=self.model.temp_uniform_data)

                    if add_uniform:
                        uniform_data =  GlUtils.make_uniform_data( UNIFORM_TYPE(self.model.temp_uniform_type), self.model.temp_uniform_data)
                        self.model.mesh.material.add_uniform(self.model.temp_uniform_name,  uniform_data,str(UNIFORM_TYPE(self.model.temp_uniform_type)))
                        self.model.mesh.material.locate_uniforms()

                        # reset the buffers
                        self.model.creating_uniform = False
                        self.model.temp_uniform_name = ""
                        self.model.temp_uniform_data = ""
                        self.model.temp_uniform_type = 0

                imgui.separator()
               
                if imgui.button("Done"):
                    self.edit_uniforms = False


            open_vertex_shader, _ = imgui.collapsing_header("Vertex Shader")
            if open_vertex_shader and self.model.mesh is not None:
                imgui.text("Vertex Shader Editor:")
                imgui.separator()
                _, self.model.mesh.material.vertex_shader = imgui.input_text_multiline("##vertex shader", self.model.mesh.material.vertex_shader, 1024 * 16, self.model.window_width, self.model.window_height)

            imgui.separator()

            open_fragment_shader, _ = imgui.collapsing_header("Fragment Shader")
            if open_fragment_shader and self.model.mesh is not None:
                imgui.text("Fragment Shader Editor:")
                imgui.separator()
                _, self.model.mesh.material.fragment_shader = imgui.input_text_multiline("##fragment shader", self.model.mesh.material.fragment_shader, 1024 * 16, self.model.window_width, self.model.window_height)

            imgui.separator()
            
            if self.model.compile_error:
                imgui.separator()
                imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.0, 0.0, 1.0)
                imgui.text("Error compiling shaders:")
                imgui.text(self.model.error_message)
                imgui.pop_style_color()
                imgui.separator()
                imgui.text("Please check the shader code and try again.")

            imgui.separator() 
            if(imgui.button("Compile")):
                self.model.compile_shaders = True

            imgui.same_line()   
            if(imgui.button("Edit Uniforms")):
                self.model.edit_uniforms = not self.model.edit_uniforms

class ShaderEditorController:
    def __init__(self, shader_view:ShaderEditorView):
        self.model = shader_view.model
        self.view = shader_view

    def render(self):
        self.view.render()

    
    def run(self):
        self.render()
        
        if self.model.compile_shaders:
            self.compile_shaders()

        if self.model.compile_error:
            print("Shader compile error:", self.model.error_message)
            self.model.error_message = ""
            self.model.compile_error = False


    # for setting a new mesh without having to recompile the shaders or create a new editor
    def change_mesh(self, mesh: Mesh = None):
        self.mesh = mesh
        if mesh:
            self.vertex_shader = self.mesh.material.vertex_shader
            self.fragment_shader = self.mesh.material.fragment_shader
        else:
            self.vertex_shader = """"""
            self.fragment_shader = """"""
      
    def compile_shaders(self):
        try:
            self.mesh.material.compile_shaders(self.vertex_shader, self.fragment_shader)
            self.model.compile_error = False
            self.model.error_message = ""
        except Exception as e:
            self.model.error_message = str(e)
            self.model.compile_error = True