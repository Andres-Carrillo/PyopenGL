from PyQt5 import QtWidgets,QtOpenGL
from PyQt5.QtGui import QSurfaceFormat
from PyQt5 import QtCore
import OpenGL.GL as gl
from PyQt5.QtWidgets import QOpenGLWidget
from core.utils.timer import Timer
from core.utils.fps import FPS
from core.rendering.renderer import Renderer,QtRenderer
from core.rendering.scene import Scene
from core.rendering.camera import Camera
from tools.movement_rig import MovementRig
from tools.grid import GridTool
from math import pi
from core.utils.qt_input import Input



class TestWidget(QOpenGLWidget):
    def __init__(self,parent:QtWidgets.QWidget=None,resolution:list=[800,600],
                 background_color:list= [0.0,0.0,0.0],show_fps:bool=False,
                 display_grid:bool = True,static_camera:bool = False) -> None:
        
        super(TestWidget, self).__init__(parent)
        # super().__init__(parent)
        
        self.makeCurrent()
        format = QSurfaceFormat()
        format.setDepthBufferSize(24)
        format.setSamples(4)
        format.setVersion(3, 3)
        format.setProfile(QSurfaceFormat.CoreProfile)
        format.setStencilBufferSize(8)
        format.setSwapBehavior(QSurfaceFormat.DoubleBuffer)
        self.setFormat(format)
        
       

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        

        self._fps_counter = FPS()
        self._background_color = background_color
        self._display_grid = display_grid
        self._static_camera = static_camera
        self._show_fps = show_fps
        self._resolution = resolution
        self._camera = Camera(aspect_ratio=self._resolution[0] / self._resolution[1])
        self._camera.set_position([0, 0, 4])
        self._scene = Scene()
        self._renderer = Renderer(clear_color=self._background_color,window_width=self._resolution[0],window_height=self._resolution[1])
        self._input_handler = Input()
        self._timer = Timer()
    
        self.rig = None
 

       
    @property
    def camera(self):
        return self._camera


    @property
    def scene(self):
        return self._scene
    
    @property
    def renderer(self):
        return self._renderer
    
    @property
    def input_handler(self):
        return self._input_handler
    
    @property
    def timer(self):
        return self._timer
    
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
        # print("updating")
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
        # print("rendering")

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

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self,parent:QtWidgets.QWidget=None,resolution:list=[800,600],
                 background_color:list= [0.0,0.0,0.0],show_fps:bool=False,
                 display_grid:bool = False,static_camera:bool = False) -> None:
        
        super().__init__(parent)
        self.makeCurrent()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        

        self._fps_counter = FPS()
        self._background_color = background_color
        self._display_grid = display_grid
        self._static_camera = static_camera
        self._show_fps = show_fps
        self._resolution = resolution
        self._camera = Camera(aspect_ratio=self._resolution[0] / self._resolution[1])
        self._camera.set_position([0, 0, 0])
        self._scene = Scene()
        self._renderer = Renderer(clear_color=self._background_color,window_width=self._resolution[0],window_height=self._resolution[1])
        self._input_handler = Input()
        self._timer = Timer()
    
        self.rig = None

       
    @property
    def camera(self):
        return self._camera


    @property
    def scene(self):
        return self._scene
    
    @property
    def renderer(self):
        return self._renderer
    
    @property
    def input_handler(self):
        return self._input_handler
    
    @property
    def timer(self):
        return self._timer
    
    def initializeGL(self):
        print("opengle initialized")
        self.makeCurrent()
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