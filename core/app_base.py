import glfw
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from core.input import Input
from core.timer import Timer
from core.fps import FPS
import OpenGL.GL as gl

class Base:
    def __init__(self, title:str = "My App", major_version:int = 3, minor_version:int =3) -> None:
        self._init_glfw(major_version, minor_version)
        self._init_window(title)
        self.timer = Timer()
        self.fps_counter = FPS() 
        self.show_fps = True
        self.input_handler = Input()
        self.input_handler.set_callbacks(self.window)
        glfw.set_framebuffer_size_callback(self.window, self._on_resize)

        gl.glEnable(gl.GL_DEPTH_TEST)
        # gl.glClearColor(0.0, 0.0, 0.0, 1.0)  # Set clear color to black
        gl.glClearColor(0.2, 0.2, 0.2, 1.0)  

    def _init_window(self, title):
        self.window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, title, None, None)
        self.title = title
        if not self.window:
            glfw.terminate()
            raise Exception("GLFW window could not be created!")

        # Make the OpenGL context current
        glfw.make_context_current(self.window)

        # Enable V-Sync
        glfw.swap_interval(1)

    def _init_glfw(self,minor_version:int,major_version:int) -> None:
        # Initialize GLFW
        if not glfw.init():
            raise Exception("GLFW could not be initialized!")
        else:
            print("GLFW initialized successfully")

        # Set GLFW window hints for OpenGL version
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, major_version)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, minor_version)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)


    def run(self):
        # main loop for all applications
        while not glfw.window_should_close(self.window):

            
            gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)
            # update to be implemented in derived classes
            self.update()
           
            glfw.swap_buffers(self.window)

            self.input_handler.update()
            if self.input_handler.quit:
                break
 
            self._display_fps()

    def _display_fps(self):
        if self.show_fps:
            glfw.set_window_title(self.window, self.title + f"- FPS: {self.fps_counter.update():.2f}")

    def update(self):
        pass

    def quit(self):
        if self.window:
            glfw.destroy_window(self.window)
            self.window = None
        
        if glfw:
            glfw.terminate()
       

    def __del__(self):
        self.quit()

    def _on_resize(self, window, width, height):
        # Adjust the OpenGL viewport to match the new window size
        gl.glViewport(0, 0, width, height)
     