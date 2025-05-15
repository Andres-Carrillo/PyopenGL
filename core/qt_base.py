from PyQt5 import QtWidgets,QtOpenGL,QtGui
from PyQt5.QtOpenGL import QGLFormat
from PyQt5 import QtCore
import OpenGL.GL as gl
from OpenGL import GLU as glu
import glfw
from core.utils.timer import Timer
from core.utils.fps import FPS
from config import SCREEN_WIDTH, SCREEN_HEIGHT
# from geometry.simple3D.sphere import Sphere
# from core.light.ambient import AmbientLight
# from core.light.directional import DirectionalLight
# from core.light.point import PointLight
# from material.lighted.phong import PhongMaterial
# from material.lighted.lambert import LambertMaterial
# from material.lighted.flat import FlatMaterial
# from core.textures.texture import Texture
# from meshes.mesh import Mesh

# from config import SCREEN_WIDTH, SCREEN_HEIGHT
# class GlWidget(QtOpenGL.QGLWidget):
    # def __init__(self,parent:QtWidgets.QWidget=None,title:str="Test App",resolution:list=[800,600],
    #              show_fps:bool=True,major_version:int=3,minor_version:int=3):
    #     super().__init__(parent)
    #     self._title = title        
    #     self._major_version = major_version
    #     self._minor_version = minor_version
    #     self._fps_counter = FPS()
    #     self._resolution = resolution
    #     self._timer = Timer()
    #     self._show_fps = show_fps
    #     self._qtimer = QtCore.QTimer(self)
    #     self._qtimer.timeout.connect(self.updateGL)
    #     self._qtimer.start(16) #~60fps

    #     format = QGLFormat()
    #     format.setVersion(self._major_version, self._minor_version)
    #     format.setProfile(QGLFormat.CoreProfile)
    #     format.setSampleBuffers(True)
        
      
    #     self.setWindowTitle(title)

    #     self.setMinimumSize(800, 600)
    #     self.setMouseTracking(True)

    # @property
    # def resolution(self) -> list:
    #     return self._resolution
    
    # @property
    # def aspect_ratio(self) -> float:
    #     return self._resolution[0] / self._resolution[1]

    # @property
    # def title(self) -> str:
    #     return self._title
    
    # @property
    # def major_version(self) -> int:
    #     return self._major_version
    
    # @property
    # def minor_version(self) -> int:
    #     return self._minor_version

    # @property
    # def fps_counter(self) -> FPS:
    #     return self._fps_counter
    
    # @property
    # def timer(self) -> Timer:
    #     return self._timer
    
    # def initializeGL(self):
    #     gl.glClearColor(0.0, 0.0, 0.0, 1.0)



    # def piantGl(self) -> None:
    #     gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    #     gl.glBegin(gl.GL_TRIANGLES)
    #     gl.glColor3f(1.0, 0.0, 0.0)
    #     gl.glVertex3f(0.0, 1.0, 0.0)
    #     gl.glColor3f(0.0, 1.0, 0.0)
    #     gl.glVertex3f(-1.0, -1.0, 0.0)
    #     gl.glColor3f(0.0, 0.0, 1.0)
    #     gl.glVertex3f(1.0, -1.0, 0.0)
    #     gl.glEnd()


    # def resizeGL(self, w:int, h:int) -> None:
    #     gl.glViewport(0, 0, w, h)
from core.rendering.renderer import Renderer
from core.rendering.scene import Scene
from core.rendering.camera import Camera
from core.rendering.render_target import RenderTarget
from threading import Lock
from tools.movement_rig import MovementRig
from tools.grid import GridTool
from math import pi
from core.utils.qt_input import Input
# main GL Context
class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self,parent:QtWidgets.QWidget=None,resolution:list=[800,600],
                 background_color:list= [0.0,0.0,0.0],show_fps:bool=False,
                 display_grid:bool = False,static_camera:bool = False,major_version:int=4,minor_version:int=5) -> None:
        
        super().__init__(parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        

        self._fps_counter = FPS()
        self._background_color = background_color
        self._display_grid = display_grid
        self._static_camera = static_camera
        self._show_fps = show_fps
        self._resolution = resolution
        self._major_version = major_version
        self._minor_version = minor_version
        self._camera = Camera(aspect_ratio=self._resolution[0] / self._resolution[1])
        self._camera.set_position([0, 0, 2])
        self._scene = Scene()
        self._renderer = Renderer(clear_color=self._background_color,window_width=self._resolution[0],window_height=self._resolution[1])
        self._input_handler = Input()
        self._timer = Timer()
    
        self.rig = None

       
    @property
    def title(self) -> str:
        return self._title

    def initializeGL(self):
        gl.glClearColor(self._background_color[0], self._background_color[1], self._background_color[2], 1.0)
        gl.glEnable(gl.GL_DEPTH_TEST)

        if not self._static_camera:
            self.rig = MovementRig()
            self.rig.add(self._camera)
            self.rig.set_position([0.5, 1, 5])
            self._scene.add(self.rig)

        if self._display_grid:
            grid = GridTool(size=self._camera.far, division=self._camera.far, grid_color=[1, 1, 1],
                            center_color=[1, 1, 0])
            grid.rotate_x(-pi / 2)
            self._scene.add(grid)
    
    def paintGL(self):
        self._update()

    def _update(self):
         # show fps
        if self._show_fps:
            self._fps_counter.update()
            self.parent().setWindowTitle(f"{self.parent()._title} - FPS: {self._fps_counter._fps:.2f}")

        # make this the current context
        self.makeCurrent()

        # if the camera is not static, update the camera position if needed
        if not self._static_camera:
            self.rig.update(self._input_handler, self._timer.delta_time())

        # render the scene
        self._renderer.render(self._scene, self._camera)

    def resizeGL(self, w, h):
        # update viewport
        gl.glViewport(0, 0, w, h)
        
        # update the resolution
        self._resolution[0] = w
        self._resolution[1] = h

        # update the renderer window size
        self._renderer.update_window_size(self._resolution[0], self._resolution[1])
        
        # update the camera aspect ratio to avoid distortion
        self._camera.update_aspect_ratio(self._resolution[0] / self._resolution[1])

    def update_frame(self):
        self.update()

    def keyPressEvent(self, event):
        self._input_handler.key_press_event(event)
        if event.key() == QtCore.Qt.Key_Escape:
            self._input_handler.quit = True
            self.parent().close()

    def keyReleaseEvent(self, event):
        """Handle key release events."""
        self._input_handler.key_release_event(event)


class QGLApp(QtWidgets.QMainWindow):
    def __init__(self,clear_color:list=[0.0, 0.0, 0.0], title:str="QGLApp",display_grid:bool=True,static_camera:bool=False,frame_limit:int=180)-> None:
        super().__init__()
        self.setMinimumSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setMouseTracking(True)
        self.gl_widget = GLWidget(self,background_color=clear_color,display_grid=display_grid,static_camera=static_camera,show_fps=True)
        self.setCentralWidget(self.gl_widget)
        self._running = True
        self._title = title
        self._frame_limit = frame_limit

        self.setWindowTitle(self._title)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(int((1/self._frame_limit) * 1000)) # convert to milliseconds
        self.timer.timeout.connect(self.update_gl)


    def run(self):
        self.timer.start() #~60fps

                # break
    def update_gl(self):
        self.gl_widget.update()