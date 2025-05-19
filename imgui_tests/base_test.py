import pathlib
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")
# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[1])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer
import OpenGL.GL as gl
from core.base import ImGuiBase
import numpy as np

from core.utils.openGLUtils import GlUtils
from core.attribute import Attribute
from core.uniform import Uniform
import math
from material.phong import PhongMaterial

class MyApp(ImGuiBase):

    def __init__(self, title = "My App",width = 800, height = 600, major_version = 3, minor_version = 3):
        super().__init__(title, width, height)
        self._init_program()
        self.material = PhongMaterial(number_of_lights=0)

    def _init_program(self) -> None:
        self.program_ref = GlUtils.InitializeProgram(self._init_vertex_shader(), self._init_fragment_shader())

        self.vao_ref = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao_ref)

        position_data = [
            [0.0,0.2,0.0],
            [0.2,-0.2,0.0],
            [-0.2,-0.2,0.0]
        ]

        self.vertex_count = len(position_data)

        position_attrib = Attribute("vec3",position_data)

        position_attrib.associate_variable(self.program_ref,"position")

        self.translation_1 = Uniform("vec3",[-0.5,0.0,0.0])

        self.translation_2 = Uniform("vec3",[0.5,0.0,0.0])

        self.base_color_1 = Uniform("vec3",[0.0,1.0,0.0])

        self._base_color_2 = Uniform("vec3",[1.0,0.0,0.0])

        self.translation_1.locate_variable(self.program_ref,"translation")
        self.translation_2.locate_variable(self.program_ref,"translation")
        self.base_color_1.locate_variable(self.program_ref,"base_color")
        self._base_color_2.locate_variable(self.program_ref,"base_color")

    def _init_vertex_shader(self)->str:
        vertex_shader_code = """
                                 in vec3 position;
                                 uniform vec3 translation;
                                 void main()
                                 {
                                    vec3 pos  = position + translation;
                                    gl_Position = vec4(pos.x,pos.y,pos.z,1.0);
                                 }"""
        
        return vertex_shader_code

    def _init_fragment_shader(self)->str:
        fragment_shader_code = """
                                uniform vec3 base_color;
                                out vec4 frag_color;
                                void main()
                                {
                                    frag_color = vec4(base_color.x,base_color.y,base_color.z,1.0);
                                }
                              """
        
        return fragment_shader_code
    

    def update(self):
        # Example: Add ImGui UI elements
        imgui.begin("Example Window")
        imgui.text("Hello, ImGui!")
        if imgui.button("Click Me!"):
            print("Button clicked!")
        imgui.end()

    def render(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)
        gl.glUseProgram(self.program_ref)
        
        self.translation_1.data[0] = 0.75*math.cos(self.timer.elapsed_time())
        self.translation_1.data[1] = 0.75*math.sin(self.timer.elapsed_time())

        self.base_color_1.data[0] = 0.5*math.cos(self.timer.elapsed_time())
        
        self.base_color_1.data[2] = 0.5*math.sin(self.timer.elapsed_time())

        self.translation_1.upload_data()
        self.base_color_1.upload_data()
        gl.glDrawArrays(gl.GL_TRIANGLES,0,self.vertex_count)

        self.translation_2.upload_data()
        self._base_color_2.upload_data()
        gl.glDrawArrays(gl.GL_TRIANGLES,0,self.vertex_count)


# Run the application
if __name__ == "__main__":
    app = MyApp(title="ImGui with GLFW", width=800, height=600)
    app.run()
