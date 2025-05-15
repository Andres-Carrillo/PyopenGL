import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[1])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from core.base import Base
from core.utils.openGLUtils import GlUtils
import glfw.GLFW as GLFW_CONSTANTS

class InputTest(Base):
    def __init__(self):
        super().__init__()


    def update(self):

        if(self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_A)):
            print("A key pressed")


        if (self.input_handler.is_key_pressed(GLFW_CONSTANTS.GLFW_KEY_B)):
            print("B key pressed")



if __name__ == "__main__":
    my_app = InputTest()
    my_app.run()
    my_app.quit()