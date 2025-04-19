import glfw
import glfw.GLFW as GLFW_CONSTANTS
import OpenGL.GL as gl
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from mesh_factory import build_triangle_mesh2,build_quad_mesh
import ctypes
from core.openGLUtils import GlUtils
from core.app_base import Base


if __name__ == "__main__":
    my_app = Base()
    my_app.run()
    my_app.quit()


# class App:
#     def __init__(self,title:str = "App",major_version:int = 3,minor_version:int = 3):
#         self.cur_time = 0.0
#         self.last_time = 0.0
#         self.title = title

#         self.show_fps = True
        
#         self.__init_glfw(major_version,minor_version)
#         self.__init__opengl()

#     def __init_glfw(self,major_version:int,minor_version:int) -> None:
#         glfw.init()
#         glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_PROFILE,GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE)
#         glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, major_version)
#         glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, minor_version)
#         glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE)

#         self.window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, self.title, None, None)

#         glfw.make_context_current(self.window)


#     def __init__opengl(self) -> None:
#         gl.glClearColor(0.1,0.2,0.4,1.0)


#         #dummy mesh
#         self.triangle_VBO,self.triangle_VAO = build_triangle_mesh2()
#         self.quad_ebo,self.quad_VBO,self.quad_VAO = build_quad_mesh()
#         self.shader = GlUtils.create_shader_program("shaders/vertex.txt","shaders/fragment.txt")

#     def run(self):
#         while not glfw.window_should_close(self.window):
#             if self.show_fps:
#                 # Display FPS in window title
#                 self._display_fps()
            
#             if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
#                 break

#             glfw.poll_events()
#             gl.glClear(gl.GL_COLOR_BUFFER_BIT)
#             gl.glUseProgram(self.shader)
#             # gl.glBindVertexArray(self.triangle_VAO)
#             # gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
#             gl.glBindVertexArray(self.quad_VAO)
#             gl.glDrawElements(gl.GL_TRIANGLES,6,gl.GL_UNSIGNED_BYTE,ctypes.c_void_p(0))
#             glfw.swap_buffers(self.window)
        
#     def quit(self):
#         # # gl.glDeleteBuffers(len(self.triangle_buffers), (self.triangle_buffers))
#         # gl.glDeleteVertexArrays(1, (self.triangle_VBO))
#         # gl.glDeleteVertexArrays(1, (self.triangle_VAO))

#         gl.glDeleteBuffers(3,(self.triangle_VBO,self.quad_ebo,self.quad_VBO))
#         gl.glDeleteVertexArrays(2,(self.triangle_VAO,self.quad_VAO))
#         gl.glDeleteProgram(self.shader)
#         glfw.destroy_window(self.window)
#         glfw.terminate()

    
#     def _display_fps(self):
#         self.cur_time = glfw.get_time()
        
#         if self.last_time == 0.0:
#             self.last_time = self.cur_time
#         else:
#             # Calculate delta time and FPS
#             self.delta_time = self.cur_time - self.last_time
#             self.last_time = self.cur_time
#             self.fps = 1.0 / self.delta_time
#             glfw.set_window_title(self.window, self.title + f" - FPS: {self.fps:.1f}")
    



