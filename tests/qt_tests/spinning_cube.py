
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
GlUtils.IS_QT = True
from core.rendering.renderer import Renderer
from core.rendering.camera import Camera
from meshes.mesh import Mesh
from core.rendering.scene import Scene
from geometry.simple3D.box import BoxGeometry
from material.basic.surface import SurfaceMaterial
from core.glsl.uniform import Uniform
from core.utils.timer import Timer


class AnimationTestWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = Timer()

    def initializeGL(self):
        self.makeCurrent()
        gl.glEnable(gl.GL_DEPTH_TEST)  # Enable depth testing
        gl.glEnable(gl.GL_MULTISAMPLE)  # Enable anti-aliasing
        gl.glEnable(gl.GL_BLEND)  # Enable blending
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)  # Set blending function

        # Initialize renderer, scene, and camera
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera()
        self.camera.set_position([0, 0, 4])  # Position the camera 4 units away from the origin
        self.camera.look_at([0, 0, 0])  # Make the camera look at the origin

        # Create a cube geometry and material
        geometry = BoxGeometry()
        material = SurfaceMaterial(
            {'use_vertex_colors': True, "wire_frame": False}
        )
        self.mesh = Mesh(geometry, material)

        # Add the cube to the scene
        self.scene.add(self.mesh)

    def paintGL(self):
        self.makeCurrent()
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)  # Clear the screen

        # Rotate the cube
        self.mesh.rotate_y(0.021)
        self.mesh.rotate_x(0.013)

        # Use the shader program
        gl.glUseProgram(self.mesh.material.program)

        # Bind the VAO for the mesh
        gl.glBindVertexArray(self.mesh.vao_ref)

        # Update the camera's view matrix
        self.camera.update_view_matrix()

        # Update the uniforms for the mesh
        self.mesh.material.uniforms["model_matrix"].data = self.mesh.global_matrix
        self.mesh.material.uniforms["view_matrix"].data = self.camera.view_matrix
        self.mesh.material.uniforms["projection_matrix"].data = self.camera.projection_matrix

        # Upload uniform data to the GPU
        for var_name, uniform_obj in self.mesh.material.uniforms.items():
            uniform_obj.upload_data()

        # Update render settings for the material
        self.mesh.material.update_render_settings()

        # Draw the cube
        gl.glDrawArrays(self.mesh.material.settings["draw_mode"], 0, self.mesh.geometry.get_vertex_count())

    def resizeGL(self, width, height):
        # Update the viewport and projection matrix when the window is resized
        gl.glViewport(0, 0, width, height)
        aspect_ratio = width / height if height > 0 else 1
        self.camera.set_perspective(45, aspect_ratio, 0.1, 100)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setMouseTracking(True)

        self._gl_widget = AnimationTestWidget(self)
        self.setCentralWidget(self._gl_widget)

        self._title = "Spinning Cube"
        self._frame_limit = 60
        self._refresh_timer = QtCore.QTimer(self)
        self._refresh_timer.setInterval(int((1 / self._frame_limit) * 1000))
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