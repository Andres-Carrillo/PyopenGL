import glfw
import glfw.GLFW as GLFW_CONSTANTS
import OpenGL.GL as gl
from config import SCREEN_WIDTH, SCREEN_HEIGHT
import ctypes
from core.utils.openGLUtils import GlUtils
from core.base import Base


from core.base import SceneEditor
        
# Run the application
if __name__ == "__main__":

    app = SceneEditor( width=1280, height=720,static_camera=False,generate_terrain__at_start=False)
    app.run()
