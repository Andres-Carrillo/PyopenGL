from PyQt5 import QtWidgets
from PyQt5 import QtCore
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from core.custom_widgets.gl_widget import GLWidget,TestWidget

class QGLApp(QtWidgets.QMainWindow):
    def __init__(self,clear_color:list=[0.0, 0.0, 0.0], title:str="QGLApp",display_grid:bool=True,static_camera:bool=False,frame_limit:int=180)-> None:
        super().__init__()
        self.setMinimumSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setMouseTracking(True)

        self._gl_widget = GLWidget(self,background_color=clear_color,display_grid=display_grid,static_camera=static_camera,show_fps=True)
        
        self.setCentralWidget(self._gl_widget)
        
        self._running = True
        self._title = title
        self._frame_limit = frame_limit

        self.setWindowTitle(self._title)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(int((1/self._frame_limit) * 1000)) # convert to milliseconds
        self.timer.timeout.connect(self.update_gl)

    @property
    def gl_widget(self):
        return self._gl_widget
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        self._title = title
        self.setWindowTitle(self._title)
    
    @property
    def running(self):
        return self._running
    
    @running.setter
    def running(self, running):
        self._running = running
        if not self._running:
            self.timer.stop()
        else:
            self.timer.start()

    def run(self):
        self.timer.start() #~60fps

                # break
    def update_gl(self):
        self.gl_widget.update()