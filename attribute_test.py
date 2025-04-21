from core.app_base import Base
from core.openGLUtils import GlUtils
from core.attribute import Attribute
from core.input import Input
import OpenGL.GL as gl
import glfw


class DrawHex(Base):
    def __init__(self):
        super().__init__()
        self._init_program()
        self.input_handler = Input()

    def _init_program(self) -> None:
        self._init_vertex_shader()
        self._init_fragment_shader()
  
        
        self.program_ref = GlUtils.InitializeProgram(self.vs_code, self.framgent_code)


        self.vao_ref = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao_ref)
        gl.glLineWidth(14)
        gl.glPointSize(14)

        position_data = [
            [0.8, 0.0, 0.0],
            [0.4, 0.6, 0.0],
            [-0.4, 0.6, 0.0],
            [-0.8, 0.0, 0.0],
            [-0.4, -0.6, 0.0],
            [0.4, -0.6, 0.0]
        ]
        
        self.vertex_count = len(position_data)

        position_attribute = Attribute("vec3", position_data)
        position_attribute.associateVariable(self.program_ref, "position")

        # Enable the vertex attribute array
        gl.glEnableVertexAttribArray(gl.glGetAttribLocation(self.program_ref, "position"))

    def update(self) -> None:
        while not glfw.window_should_close(self.window):
            print("updating")
            gl.glClearColor(0.0, 0.0, 0.0, 1.0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            # Use the shader program
            gl.glUseProgram(self.program_ref)

            # Bind the VAO
            # gl.glBindVertexArray(self.vao_ref)

            # Enable the vertex attribute array (if necessary)
            # gl.glEnableVertexAttribArray(gl.glGetAttribLocation(self.program_ref, "position"))

            # Draw the hexagon
            print("vertex count", self.vertex_count)
            gl.glDrawArrays(gl.GL_LINE_LOOP, 0, self.vertex_count)

            # Swap buffers and poll for events
            glfw.swap_buffers(self.window)


            self.input_handler.update(self.window)

            if self.input_handler.quit:
                break

            self._display_fps()

    def _init_vertex_shader(self) -> None:
        self.vs_code = """
        in vec3 position;
        void main(){
            gl_Position = vec4(position.x, position.y, position.z, 1.0); // Draw point at location specified by position
        }
        """

    def _init_fragment_shader(self) -> None:
        self.framgent_code = """
        out vec4 frag_color;
        void main(){
            frag_color = vec4(1.0, 1.0, 0.0, 1.0); // color to be used
        }
        """

    def quit(self):
        gl.glDeleteProgram(self.program_ref)
        gl.glDeleteVertexArrays(1, [self.vao_ref]) 
        return super().quit()


if __name__ == "__main__":
    my_app = DrawHex()
    my_app.run()
    my_app.quit()