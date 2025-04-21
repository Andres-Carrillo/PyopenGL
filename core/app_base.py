import glfw
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Base:
    def __init__(self, title:str = "My App", major_version:int = 3, minor_version:int =3) -> None:
        self._init_glfw(major_version, minor_version)
        self._init_window(title)

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

        # Set GLFW window hints for OpenGL version
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, major_version)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, minor_version)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)


    # to be overridden in derived classes
    def run(self):
        pass

    def quit(self):
        if self.window:
            glfw.destroy_window(self.window)
        glfw.terminate()

    def __del__(self):
        # Clean up GLFW resources
        if self.window:
            glfw.destroy_window(self.window)
        glfw.terminate()