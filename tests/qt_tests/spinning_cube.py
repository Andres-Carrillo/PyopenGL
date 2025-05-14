# import pathlib
# import sys
# import warnings
# warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")
# # Get the package directory
# package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# # Add the package directory into sys.path if necessary
# if package_dir not in sys.path:
#     sys.path.insert(0, package_dir)

# from PyQt5 import QtWidgets
# from PyQt5 import QtCore
# from PyQt5.QtGui import QOpenGLShader
# import OpenGL.GL as gl
# from PyQt5.QtWidgets import QOpenGLWidget
# import numpy as np
# from core.utils.openGLUtils import GlUtils
# GlUtils.IS_QT = True
# from core.rendering.renderer import Renderer
# from core.rendering.camera import Camera
# from meshes.mesh import Mesh
# from core.rendering.scene import Scene
# from geometry.simple3D.box import BoxGeometry
# from material.basic.surface import SurfaceMaterial
# from material.basic.point import PointMaterial
# from core.glsl.attribute import Attribute
# from core.glsl.uniform import Uniform
# import math
# from core.utils.timer import Timer
# from geometry.simple3D.sphere import Sphere



# class AnimationTestWidget(QOpenGLWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.timer = Timer()


#     def initializeGL(self):
#         self.makeCurrent()
#         gl.glEnable(gl.GL_DEPTH_TEST)
#         # enables anti-aliasing
#         gl.glEnable(gl.GL_MULTISAMPLE)

#         # enables blending
#         gl.glEnable(gl.GL_BLEND)
#         # set the blending function
#         # gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

#         self.renderer = Renderer()
#         self.scene = Scene()
#         self.camera = Camera()
#         self.camera.set_position([0, 0, 4])
        
#         geometry = BoxGeometry()
        
        
#         material = SurfaceMaterial(
#             {'use_vertex_colors':True,
#              "wire_frame":False,}
#         )
#         self.mesh = Mesh(geometry, material)
        
#         self.camera.look_at(self.mesh.global_position)
        
#         self.scene.add(self.mesh)
#         # self.releaseContext()

      
#         # s
        
#         # self.program = GlUtils.InitializeProgram(vertex_shader, fragment_shader)
        
#         # self.vao_ref = gl.glGenVertexArrays(1)
#         # gl.glBindVertexArray(self.vao_ref)

#         # position_data = [
#         #     [0.0,0.2,0.0],
#         #     [0.2,-0.2,0.0],
#         #     [-0.2,-0.2,0.0]
#         # ]

#         # self.vertex_count = len(position_data)

#         # position_attrib = Attribute("vec3",position_data)

#         # position_attrib.associate_variable(self.program,"position")

#         # self.translation_1 = Uniform("vec3",[-0.5,0.0,0.0])


#         # self.translation_2 = Uniform("vec3",[0.5,0.0,0.0])

#         # self.base_color_1 = Uniform("vec3",[0.0,1.0,0.0])

#         # self._base_color_2 = Uniform("vec3",[1.0,0.0,0.0])

#         # self.translation_1.locate_variable(self.program,"translation")
#         # self.translation_2.locate_variable(self.program,"translation")
#         # self.base_color_1.locate_variable(self.program,"base_color")
#         # self._base_color_2.locate_variable(self.program,"base_color")


#     def paintGL(self):
#         self.makeCurrent()
#         gl.glEnable(gl.GL_DEPTH_TEST)
#         gl.glDepthFunc(gl.GL_LESS)
#         gl.glDisable(gl.GL_CULL_FACE)
#         self.mesh.rotate_y(0.021)
#         self.mesh.rotate_x(0.013)
#         gl.glBindFramebuffer(gl.GL_FRAMEBUFFER,0)
#         # gl.glViewport(0, 0, self.parent().width(), self.parent().height())


#         gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

   
#         # print("self.mesh.material.program",self.mesh.material.program)

#         # print("mesh vao_ref",self.mesh.vao_ref)
#         # print("View Matrix:", self.camera.view_matrix)
#         # print("camera position",self.camera.global_position)
#         gl.glUseProgram(self.mesh.material.program)
#         # bind vertex array object for the mesh
#         gl.glBindVertexArray(self.mesh.vao_ref)

#          #update camera
#         self.camera.update_view_matrix()
#         # ================== update the uniforms for the mesh not stored in the material ==================
#         #update the model matrix based on the mesh's world matrix
#         self.mesh.material.uniforms["model_matrix"].data = self.mesh.global_matrix
#         # update the view matrix to match the camera
#         self.mesh.material.uniforms["view_matrix"].data = self.camera.view_matrix
#         # update the projection matrix to match the camera
#         self.mesh.material.uniforms["projection_matrix"].data = self.camera.projection_matrix



#         # ================== update the uniforms for the mesh stored in the material ==================
#         for var_name,uniform_obj in self.mesh.material.uniforms.items():
#             # print("uniform_obj",uniform_obj)
#             # print("uniform_obj.data",uniform_obj.data)
#                 # if uniform_obj.data is not None:
#             uniform_obj.upload_data()


#         #update the render settings for the material
#         self.mesh.material.update_render_settings()

#         # print("vertex count",self.mesh.geometry.get_vertex_count())
#             # draw the mesh
#         gl.glDrawArrays(self.mesh.material.settings["draw_mode"],0,self.mesh.geometry.get_vertex_count())


#         # self.renderer.render(self.scene, self.camera)
#         # print("called paintGL")
#     #     Timer.sleep(0.016)
#     #     elapsed_time = self.timer.elapsed_time()
#     #     gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
#     #     # Use the shader program
#     #     gl.glUseProgram(self.program)

#     #     self.translation_1.data[0] = 0.75*math.cos(elapsed_time)
#     #     self.translation_1.data[1] = 0.75*math.sin(elapsed_time)

#     #     self.base_color_1.data[0] = 0.5*math.cos(elapsed_time)
#     #     self.base_color_1.data[2] = 0.5*math.sin(elapsed_time)


#     #     self.translation_1.upload_data()
#     #     self.base_color_1.upload_data()
#     #     gl.glDrawArrays(gl.GL_TRIANGLES,0,self.vertex_count)

#     #     self.translation_2.upload_data()
#     #     self._base_color_2.upload_data()
#     #     gl.glDrawArrays(gl.GL_TRIANGLES,0,self.vertex_count)


# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setMinimumSize(800, 600)
#         self.setMouseTracking(True)

#         self._gl_widget = AnimationTestWidget(self)
#         self._gl_widget._show_fps = True
#         self.setCentralWidget(self._gl_widget)
        
#         self._running = True
#         self._title = "Spinning Cube"
#         self._frame_limit = 60
#         self._refresh_timer = QtCore.QTimer(self)
#         self._refresh_timer.setInterval(int((1/self._frame_limit) * 1000))
#         self._refresh_timer.timeout.connect(self.update_gl)
#         self._refresh_timer.start()

#         self.setWindowTitle(self._title)

#     def update_gl(self):
#         self._gl_widget.update()


# if __name__ == "__main__":
#     app = QtWidgets.QApplication([])
#     window = MainWindow()
#     window.show()
#     app.exec_()

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