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

class AttributeTestWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vertex_source_code = """
        
        in vec3 position;
        void main(){
            gl_Position = vec4(position.x, position.y, position.z, 1.0); // Draw point at location specified by position
        }
        """

        self.framgent_source_code = """
        
        out vec4 frag_color;
        void main(){
            frag_color = vec4(1.0, 1.0, 0.0, 1.0); // color to be used
        }
        """

        self.position_data = np.array([
            [0.8, 0.0, 0.0],
            [0.4, 0.6, 0.0],
            [-0.4, 0.6, 0.0],
            [-0.8, 0.0, 0.0],
            [-0.4, -0.6, 0.0],
            [0.4, -0.6, 0.0]
        ], dtype=np.float32)

        self.vertex_count = len(self.position_data)

    def initializeGL(self):
        self.makeCurrent()
        # self.vs_code = GlUtils.initialize_shader(self.vertex_source_code, QOpenGLShader.Vertex)
        # self.framgent_code = GlUtils.initialize_shader(self.framgent_source_code, QOpenGLShader.Fragment)

        # Compile and link the shader program
        self.program = GlUtils.InitializeProgram(self.vertex_source_code, self.framgent_source_code,
                                                is_qt=True)

        position_attribute = Attribute("vec3", self.position_data)

        position_attribute.associate_variable(self.program, "position")
        
        gl.glEnableVertexAttribArray(gl.glGetAttribLocation(self.program, "position"))
  

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        # Use the shader program
        gl.glUseProgram(self.program)

        # Draw the hexagon
        gl.glDrawArrays(gl.GL_TRIANGLE_FAN, 0, self.vertex_count)



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setMouseTracking(True)

        self._gl_widget = AttributeTestWidget(self)
        self._gl_widget._show_fps = True
        self.setCentralWidget(self._gl_widget)
        
        self._running = True
        self._title = "Attribute Test"
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