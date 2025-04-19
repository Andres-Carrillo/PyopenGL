import glfw
import glfw.GLFW as GLFW_CONSTANTS
import OpenGL.GL as gl


class Input(object):
    def __init__(self) -> None:
        self.quit = False
        self.keys = {}
        self.mouse_buttons = {}


    def update(self,window) -> None:
        glfw.poll_events()
        if glfw.get_key(window, GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS:
                self.quit = True

        