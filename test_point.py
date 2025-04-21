from core.openGLUtils import GlUtils
from core.app_base import Base
from core.input import Input
import OpenGL.GL as gl
import glfw

class DrawPoint(Base):
    def __init__(self, title: str = "Draw Point", major_version: int = 3, minor_version: int = 3):
        super().__init__(title, major_version, minor_version)
        self._cur_time = 0.0
        self._last_time = 0.0
        self._delta_time = 0.0
        self._fps = 0.0
        self.show_fps = True
        self.point_size = 10.0
        self.input_handler = Input()
        self._init_shaders()
        

    def run(self):
        while not glfw.window_should_close(self.window):
            gl.glClearColor(0.0, 0.0, 0.0, 1.0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            gl.glUseProgram(self.program)
            gl.glBindVertexArray(self.vao)
            gl.glDrawArrays(gl.GL_POINTS, 0, 1)
            glfw.swap_buffers(self.window)

            self._display_fps()
            self.input_handler.update(self.window) 

            if self.input_handler.quit:
                break           

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

    def _display_fps(self):
        if self.show_fps:
                self._cur_time = glfw.get_time()

                if self._last_time != 0.0:
                        self._delta_time = self._cur_time - self._last_time
                        self._fps = 1.0 / self._delta_time
                        glfw.set_window_title(self.window, self.title + f"- FPS: {self._fps:.2f}")

                self._last_time = self._cur_time



if __name__ == "__main__":
    my_app = DrawPoint()
    my_app.run()
    my_app.quit()