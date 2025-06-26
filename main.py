import glfw
import glfw.GLFW as GLFW_CONSTANTS
import OpenGL.GL as gl
from config import SCREEN_WIDTH, SCREEN_HEIGHT
import ctypes
from core.utils.openGLUtils import GlUtils
from core.base import Base


if __name__ == "__main__":
    my_app = Base()
    my_app.run()
    my_app.quit()
