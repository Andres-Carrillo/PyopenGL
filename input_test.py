from core.app_base import Base
from core.openGLUtils import GlUtils
import glfw.GLFW as GLFW_CONSTANTS

class InputTest(Base):
    def __init__(self, title = "My App", major_version = 3, minor_version = 3):
        super().__init__(title, major_version, minor_version)


    def update(self):

        if(self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_A)):
            print("A key pressed")


        if (self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_B)):
            print("B key pressed")



if __name__ == "__main__":
    my_app = InputTest()
    my_app.run()
    my_app.quit()