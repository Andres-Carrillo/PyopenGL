import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)


from core.utils.matrix import Matrix
from core.base import Base
from core.utils.openGLUtils import GlUtils
from core.glsl.attribute import Attribute
from core.glsl.uniform import Uniform
from core.utils.timer import Timer
import glfw.GLFW as GLFW_CONSTANTS
import OpenGL.GL as gl
from math import pi
import glfw

class TransformationTest(Base):
    def __init__(self, title = "Transformation Test"):
        super().__init__(title=title)
        self._init_program()

    

    def _init_program(self) -> None:
        self.program_ref = GlUtils.InitializeProgram(self._init_vertex_shader(), self._init_fragment_shader())
        self.vao_ref = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao_ref)
        position_data = [[0.0,   0.2,  0.0], [0.1,  -0.2,  0.0], [-0.1, -0.2,  0.0]]
        
        self.vertex_count = len(position_data)

        # Associate the vertex data with the shader program
        position_attribute = Attribute("vec3", position_data)
        position_attribute.associate_variable(self.program_ref, "position")

        # Create uniforms
        self.model = Uniform("mat4", Matrix.mat4_translation(0.0, 0.0, -1.0))
        self.model.locate_variable(self.program_ref, "model_matrix")

        self.projection = Uniform("mat4", Matrix.mat4_perspective())
        self.projection.locate_variable(self.program_ref, "projection_matrix")

        self.move_speed = 0.01
        self.rotation_speed = 90 * (pi / 180)



    def _init_vertex_shader(self)->str:
        vertex_shader_code = """
                                  in vec3 position;
                                  uniform mat4 projection_matrix;
                                  uniform mat4 model_matrix;
                                  void main()
                                  {
                                     gl_Position = projection_matrix * model_matrix * vec4(position.x,position.y,position.z, 1.0);
                                  }"""
        
        return vertex_shader_code
    
    def _init_fragment_shader(self)->str:
        fragment_shader_code = """
                                out vec4 color;
                                void main()
                                {
                                    color = vec4(1.0,0.0,0.0, 1.0);
                                }"""
        
        return fragment_shader_code
    
    def update(self):
        # Timer.sleep(0.016)

        move_amount = self.move_speed * self.timer.delta_time()
        turn_amount = self.rotation_speed * self.timer.delta_time()

        # Apply transformations based on input
        # global positional transformations
        if self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_W):
            transform = Matrix.mat4_translation(0.0, move_amount, 0.0)
            self.model.data = transform @ self.model.data
        if self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_S):
            transform = Matrix.mat4_translation(0.0, -move_amount, 0.0)
            self.model.data = transform @ self.model.data
        if self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_A):
            transform = Matrix.mat4_translation(-move_amount, 0.0, 0.0)
            self.model.data = transform @ self.model.data
        if self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_D):
            transform = Matrix.mat4_translation(move_amount, 0.0, 0.0)
            self.model.data = transform @ self.model.data
        if self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_Z):
            transform = Matrix.mat4_translation(0.0, 0.0, move_amount)
            self.model.data = transform @ self.model.data
        if self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_X):
            transform = Matrix.mat4_translation(0.0, 0.0, -move_amount)
            self.model.data = transform @ self.model.data
        # Global rotation transformations
        if self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_Q):
            transform = Matrix.mat4_rotate_y(turn_amount)
            self.model.data = transform @ self.model.data
        if self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_E):
            transform = Matrix.mat4_rotate_y(-turn_amount)
            self.model.data = transform @ self.model.data

        # Local Positional transformations
        if self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_UP):
            transform = Matrix.mat4_translation(0.0, move_amount, 0.0)
            self.model.data = self.model.data @ transform
        if self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_DOWN):
            transform = Matrix.mat4_translation(0.0, -move_amount, 0.0)
            self.model.data = self.model.data @ transform
        if self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_LEFT):
            transform = Matrix.mat4_translation(-move_amount, 0.0, 0.0)
            self.model.data = self.model.data @ transform
        if self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_RIGHT):
            transform = Matrix.mat4_translation(move_amount, 0.0, 0.0)
            self.model.data = self.model.data @ transform
        if self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_PAGE_UP):
            transform = Matrix.mat4_translation(0.0, 0.0, move_amount)
            self.model.data = self.model.data @ transform
        if self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_PAGE_DOWN):
            transform = Matrix.mat4_translation(0.0, 0.0, -move_amount)
            self.model.data = self.model.data @ transform

        # Local rotation transformations
        if self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_LEFT_BRACKET):
            transform = Matrix.mat4_rotate_z(turn_amount)
            self.model.data = self.model.data @ transform
        if self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_RIGHT_BRACKET):
            transform = Matrix.mat4_rotate_z(-turn_amount)
            self.model.data = self.model.data @ transform


        gl.glUseProgram(self.program_ref)
        self.projection.upload_data()
        self.model.upload_data()
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.vertex_count)





if __name__ == "__main__":
    app = TransformationTest()
    app.run()
    app.quit()

