import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

print("dir: " ,package_dir)
# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from core.utils.openGLUtils import GlUtils
from core.base import Base
from core.utils.input import Input
import OpenGL.GL as gl
import glfw

class DrawPoint(Base):
    def __init__(self, title: str = "Draw Point", major_version: int = 3, minor_version: int = 3):
        super().__init__(title, major_version, minor_version)

        self.point_size = 10.0
        self.input_handler = Input()
        self._init_shaders()
        

    def update(self):
        while not glfw.window_should_close(self.window):

            # Draw the point
            gl.glUseProgram(self.program)
          
            gl.glDrawArrays(gl.GL_POINTS, 0, 1)

            # Swap buffers
            glfw.swap_buffers(self.window)

            # Poll for and process events
            self.input_handler.update(self.window) 

            if self.input_handler.quit:
                break           

            # update fps
            self._display_fps()


    def _init_shaders(self):
        vertex_shader_source = """
        void main() {
                gl_Position = vec4(0.0, 0.0, 0.0, 1.0);  // Draw point at the center
        }
        """

        fragment_shader_source = """
        out vec4 frag_color;
        void main() {
                frag_color = vec4(1.0, 1.0, 0.0, 1.0);  // Yellow color
        }
        """

        self.program = GlUtils.InitializeProgram(vertex_shader_source, fragment_shader_source)
        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)
        gl.glPointSize(self.point_size)


    def quit(self):
        gl.glDeleteProgram(self.program)
        gl.glDeleteVertexArrays(1, [self.vao])    

        if self.window:
            glfw.destroy_window(self.window)
        glfw.terminate()


if __name__ == "__main__":
    my_app = DrawPoint()
    my_app.run()
    my_app.quit()