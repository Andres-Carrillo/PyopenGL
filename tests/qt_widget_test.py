import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[1])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from core.qt_base import GLWidget,QGLTestWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
import sys

# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self,title:str="GLWidget Test",show_fps:bool=True):
#         super().__init__()
#         self.setWindowTitle("GLWidget Test")
#         self.setGeometry(100, 100, 800, 600)

#         # Create an instance of the GlWidget
#         self.gl_widget = GLWidget(parent=self)
#         self.setCentralWidget(self.gl_widget)

#         # Show the window
#         self.show()

#     def update_gl(self):
#         self.gl_widget.update()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     main_window = MainWindow()
#     main_window.show()

#     sys.exit(app.exec_())

from PyQt5 import QtWidgets, QtOpenGL
from OpenGL import GL

# class GLWidget(QtOpenGL.QGLWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#     def initializeGL(self):
#         GL.glClearColor(0.0, 0.0, 0.0, 1.0)

#     def paintGL(self):
#          GL.glClear(GL.GL_COLOR_BUFFER_BIT)
#          GL.glBegin(GL.GL_TRIANGLES)
#          GL.glColor3f(1.0, 0.0, 0.0)
#          GL.glVertex3f(0.0, 1.0, 0.0)
#          GL.glColor3f(0.0, 1.0, 0.0)
#          GL.glVertex3f(-1.0, -1.0, 0.0)
#          GL.glColor3f(0.0, 0.0, 1.0)
#          GL.glVertex3f(1.0, -1.0, 0.0)
#          GL.glEnd()

#     def resizeGL(self, w, h):
#         GL.glViewport(0, 0, w, h)


# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.gl_widget = GLWidget(self)
#         self.setCentralWidget(self.gl_widget)
#         self._running = True
#         self.timer = QtCore.QTimer(self)
#         self.timer.timeout.connect(self.update_gl)


#     def run(self):
#         self.timer.start(1) #~60fps


#                 # break
#     def update_gl(self):
#         self.gl_widget.update()

if __name__ == '__main__':
    import sys
    from PyQt5 import QtCore

    app = QtWidgets.QApplication(sys.argv)
    main_window = QGLTestWindow()
    main_window.run()
    main_window.show()
    sys.exit(app.exec_())