import glfw
import glfw.GLFW as GLFW_CONSTANTS
import OpenGL.GL as gl
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Base:
    def __init__(self,title:str = "App",width:int = SCREEN_WIDTH,height:int = SCREEN_HEIGHT,major_version:int = 3,minor_version:int = 3):
        self.cur_time = 0.0
        self.last_time = 0.0
        self.title = title
        self.show_fps = True
        self.window_width = width
        self.window_height = height
    
        self.__init_glfw(major_version,minor_version)
        self.__init__opengl()

    def __init_glfw(self,major_version:int,minor_version:int) -> None:
        glfw.init()
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_PROFILE,GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, major_version)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, minor_version)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE)

        self.window = glfw.create_window(self.window_width, self.window_height, self.title, None, None)

        glfw.make_context_current(self.window)


    def __init__opengl(self) -> None:
        gl.glClearColor(0.1,0.2,0.4,1.0)

    def run(self):
        while not glfw.window_should_close(self.window):
            if self.show_fps:
                self._display_fps()
            
            if glfw.get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
                break

            glfw.poll_events()
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            glfw.swap_buffers(self.window)
        
    def quit(self):

        glfw.destroy_window(self.window)
        glfw.terminate()

    
    def _display_fps(self):
        self.cur_time = glfw.get_time()
        
        if self.last_time == 0.0:
            self.last_time = self.cur_time
        else:
            self.delta_time = self.cur_time - self.last_time
            self.last_time = self.cur_time
            self.fps = 1.0 / self.delta_time
            glfw.set_window_title(self.window, self.title + f" - FPS: {self.fps:.1f}")