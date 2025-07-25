import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from core.base import Base
from core.rendering.renderer import Renderer
from core.rendering.scene import Scene
from core.rendering.camera import Camera
from core.tools.grid import GridTool
from math import pi
from core.tools.movement_rig import MovementRig

class Test(Base):

    def __init__(self,clear_color:list=[0.0, 0.0, 0.0], title:str="Test",display_grid:bool=True,static_camera:bool=False)-> None:

        super().__init__(title=title)
        self.renderer = Renderer(clear_color=clear_color)
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_position([0, 0, 4])
        self.rig = None


        if  not static_camera:
            self.rig = MovementRig()
            self.rig.add(self.camera)
            self.rig.set_position([0.5, 1, 5])

            self.scene.add(self.rig)

        if display_grid:
            grid = GridTool(size = self.camera.far,division=self.camera.far,grid_color=[1,1,1],center_color=[1,1,0])

            grid.rotate_x(-pi/2)
            self.scene.add(grid)
        

    def _base_update(self):
        # set the window size in case the window was resized
        self.renderer.update_window_size(self.window_width, self.window_height)
        
        # update the camera aspect ratio to avoid distortion
        self.camera.update_aspect_ratio(self.window_width / self.window_height)

        # update the input handler
        if self.rig is not None:
            self.rig.update(self.input_handler, self.timer.delta_time())

    def update(self) -> None:
        self._base_update()
        # render the scene        
        self.renderer.render(self.scene, self.camera)


