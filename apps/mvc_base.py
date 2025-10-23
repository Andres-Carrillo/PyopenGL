import imgui
from core.utils.input import Input
from core.utils.timer import Timer
from core.rendering.scene import Scene
from core.rendering.renderer import Renderer
from core.tools.grid import GridTool
from core.rendering.camera import Camera
from core.tools.movement_rig import MovementRig
from math import pi
from apps.base import ImGuiBase
import OpenGL.GL as gl

class AppModel:
    def __init__(self,width= 800,height=600,static_camera=True,display_grid=True):
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=width / height)
        self.renderer = Renderer()
        self.window_width = width
        self.window_height = height
        self.static_camera = static_camera
        self.display_grid = display_grid
        self.camera_rig = None
        self.grid_tool = None   

        self._init_scene()

    def _init_scene(self): 
        if not self.static_camera:
            self.camera_rig = MovementRig()
            self.camera_rig.add(self.camera)
            self.camera_rig.set_position([0.5, 1, 5])
            self.scene.add(self.camera_rig)
        else:
            self.camera.set_position([0, 1, 1])

        if self.display_grid:
            self.grid_tool = GridTool(size = self.camera.far,division=int(self.camera.far*2),grid_color=[1,1,1],center_color=[1,1,0])
            self.grid_tool.rotate_x(-pi/2)
            self.scene.add(self.grid_tool)

class AppView:
    def __init__(self,model:AppModel,imgui_renderer):
        self.model = model
        self.imgui_renderer = imgui_renderer

    def render_imgui(self):
        imgui.begin("Example Window")
        imgui.text("Hello, ImGui!")
        if imgui.button("Click Me!"):
            print("Button clicked!")
        imgui.end()

    def render_scene(self):
        self.model.renderer.update_window_size(self.model.window_width, self.model.window_height)
        self.model.camera.update_aspect_ratio(self.model.window_width / self.model.window_height)
        self.model.renderer.render(self.model.scene, self.model.camera)

class AppController:
    def __init__(self,view:AppView,input_handler:Input,timer:Timer):
        self.model = view.model
        self.view = view
        self.input_handler = input_handler
        self.timer = timer
        self._time_delta = 0

    def update(self):
        self._tick()
        self._handle_input()
        self.model.renderer.update_window_size(self.model.window_width, self.model.window_height)

        # update the camera aspect ratio to avoid distortion
        self.model.camera.update_aspect_ratio(self.model.window_width / self.model.window_height)

    def render(self):
        self.model.camera.update_aspect_ratio(self.model.window_width / self.model.window_height)
        self.view.render_imgui()
        self.view.render_scene()

    def _tick(self):
        self._time_delta = self.timer.delta_time()

    def _handle_input(self):
        self.input_handler.update()
        if self.model.camera_rig is not None:
            self.model.camera_rig.update(self.input_handler, self._time_delta)

class MVCApp(ImGuiBase):
    def __init__(self,title:str="MVC App",width:int=800,height:int=600,
                 major_version:int=3,minor_version:int=3,display_fps:bool=True,display_grid:bool=True,static_camera:bool=True):
        
        super().__init__(title,width,height,show_fps=display_fps,major_version=major_version,minor_version=minor_version)
        
        self.model = AppModel(width,height,static_camera,display_grid)
        self.view = AppView(self.model,self.imgui_renderer)
        self.controller = AppController(self.view,self.input_handler,self.timer) 

    def update(self):
        self.controller.update()

    def render(self):
        self.controller.render()

    def _on_resize(self, window, width, height) -> None:
        """
        Callback function for window resize events.
        Adjusts the OpenGL viewport to match the new window size.
        """
        self.window_width = width
        self.window_height = height
        gl.glViewport(0, 0, width, height)
        # --- Add this if using MVCApp ---
        if hasattr(self, "model"):
            self.model.window_width = width
            self.model.window_height = height