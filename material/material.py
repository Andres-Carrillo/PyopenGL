from core.utils.openGLUtils import GlUtils
from core.uniform import Uniform
import OpenGL.GL as gl

class Material(object):

    def __init__(self,vertex_shader:str,fragment_shader:str) -> None:
        # initialize the material with vertex and fragment shaders and get program reference
        self.program = GlUtils.InitializeProgram(vertex_shader, fragment_shader)
        
        # uniform object dictionary
        # this will be used to store the uniforms
        self.uniforms = {}
        
        # diction for opengl settings
        self.settings = {}

        # initialize the basic uniforms
        # inherited classes should override this method
        # and add their own uniforms
        self._init_uniforms()
        self._init_settings()

        self.material_type = type(self).__name__
        self.material_type = self.material_type.replace("Material","")
        
        

    def _init_uniforms(self) -> None:
        self.uniforms["model_matrix"] = Uniform("mat4", None)
        self.uniforms["view_matrix"] = Uniform("mat4", None)    
        self.uniforms["projection_matrix"] = Uniform("mat4", None)


    def _init_settings(self) -> None:
        self.settings["draw_mode"] = gl.GL_TRIANGLES


    def add_uniform(self,name:str,data:object,datatype:str) -> None:
        self.uniforms[name] = Uniform(datatype, data)

    # initialize the uniforms
    def locate_uniforms(self) -> None:
        # locate the uniforms in the shader program
        for name, uniform in self.uniforms.items():
            uniform.locate_variable(self.program, name)


    def configure_settings(self) -> None:
        pass


    def set_properties(self,properties:dict) -> None:
        for name,data in properties.items():
            if name in self.uniforms.keys():
                self.uniforms[name].data = data
            elif name in self.settings.keys():
                self.settings[name] = data
            else:
                raise RuntimeError(f"Property {name} not found in material")
            


    def update_render_settings(self):
        """ Configure OpenGL with render settings """
        pass