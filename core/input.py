import glfw
import glfw.GLFW as GLFW_CONSTANTS
import OpenGL.GL as gl

class Input(object):
    def __init__(self) -> None:
        self.quit = False
        self.key_queue = []
        # self.key_down_list = []
        self.key_pressed_list = []
        self.key_held_list = []
        self.key_released_list = []
        self.mouse_buttons = []


    def set_callbacks(self,window)->None:
        glfw.set_key_callback(window, self.key_callback)


    def key_callback(self, window, key, scancode, action, mods):
        if action == GLFW_CONSTANTS.GLFW_PRESS: 
            self.key_pressed_list.append(key)
            self.key_queue.append(key)

        elif action == GLFW_CONSTANTS.GLFW_RELEASE:
            self.key_pressed_list.remove(key)   

        if key == GLFW_CONSTANTS.GLFW_KEY_ESCAPE and action == GLFW_CONSTANTS.GLFW_PRESS:
            self.quit = True

    def is_key_pressed(self, key) -> bool:
        return key in self.key_pressed_list
    
    def is_key_held(self, key) -> bool:
        pass

    def is_key_released(self, key) -> bool:
        return key in self.key_released_list

    def update(self) -> None:
        glfw.poll_events()

        