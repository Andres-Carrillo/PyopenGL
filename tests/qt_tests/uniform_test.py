import pathlib
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")
# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtGui import QOpenGLShader
import OpenGL.GL as gl
from PyQt5.QtWidgets import QOpenGLWidget
import numpy as np
from core.utils.openGLUtils import GlUtils
from core.glsl.attribute import Attribute
from core.glsl.uniform import Uniform
import math
from core.utils.timer import Timer

GlUtils.IS_QT = True


class UniformTestWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = Timer()


    def initializeGL(self):
        
        vertex_shader_code = """
                        
                                 in vec3 position;
                                 uniform vec3 translation;
                                 void main()
                                 {
                                    vec3 pos  = position + translation;
                                    gl_Position = vec4(pos.x,pos.y,pos.z,1.0);
                                 }"""
        
        fragment_shader_code = """
                                uniform vec3 base_color;
                                out vec4 frag_color;
                                void main()
                                {
                                    frag_color = vec4(base_color.x,base_color.y,base_color.z,1.0);
                                }
                              """
        self.makeCurrent()
        
        self.program = GlUtils.InitializeProgram(vertex_shader_code, fragment_shader_code)
        
        self.vao_ref = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao_ref)

        position_data = [
            [0.0,0.2,0.0],
            [0.2,-0.2,0.0],
            [-0.2,-0.2,0.0]
        ]

        self.vertex_count = len(position_data)

        position_attrib = Attribute("vec3",position_data)

        position_attrib.associate_variable(self.program,"position")

        self.translation_1 = Uniform("vec3",[-0.5,0.0,0.0])


        self.translation_2 = Uniform("vec3",[0.5,0.0,0.0])

        self.base_color_1 = Uniform("vec3",[0.0,1.0,0.0])

        self._base_color_2 = Uniform("vec3",[1.0,0.0,0.0])

        self.translation_1.locate_variable(self.program,"translation")
        self.translation_2.locate_variable(self.program,"translation")
        self.base_color_1.locate_variable(self.program,"base_color")
        self._base_color_2.locate_variable(self.program,"base_color")


    def paintGL(self):
        Timer.sleep(0.016)
        elapsed_time = self.timer.elapsed_time()
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        # Use the shader program
        gl.glUseProgram(self.program)

        self.translation_1.data[0] = 0.75*math.cos(elapsed_time)
        self.translation_1.data[1] = 0.75*math.sin(elapsed_time)

        self.base_color_1.data[0] = 0.5*math.cos(elapsed_time)
        self.base_color_1.data[2] = 0.5*math.sin(elapsed_time)


        self.translation_1.upload_data()
        self.base_color_1.upload_data()
        gl.glDrawArrays(gl.GL_TRIANGLES,0,self.vertex_count)

        self.translation_2.upload_data()
        self._base_color_2.upload_data()
        gl.glDrawArrays(gl.GL_TRIANGLES,0,self.vertex_count)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setMouseTracking(True)

        self._gl_widget = UniformTestWidget(self)
        self._gl_widget._show_fps = True
        self.setCentralWidget(self._gl_widget)
        
        self._running = True
        self._title = "Uniform Test"
        self._frame_limit = 60
        self._refresh_timer = QtCore.QTimer(self)
        self._refresh_timer.setInterval(int((1/self._frame_limit) * 1000))
        self._refresh_timer.timeout.connect(self.update_gl)
        self._refresh_timer.start()

        self.setWindowTitle(self._title)

    def update_gl(self):
        self._gl_widget.update()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()