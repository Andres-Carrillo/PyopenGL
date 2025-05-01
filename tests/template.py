import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[1])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from core.app_base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from tools.grid import GridTool
from math import pi
from tools.movement_rig import MovementRig

class Test(Base):

    def __init__(self,clear_color=[0.2, 0.2, 0.2], title="Test",display_grid=True,static_camera=False):

        super().__init__(title=title)
        self.renderer = Renderer(clear_color=clear_color)
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_pos([0, 0, 4])
        self.rig = None


        if not static_camera:
            self.rig = MovementRig()
            self.rig.add(self.camera)
            self.rig.set_pos([0.5, 1, 5])

            self.scene.add(self.rig)

        if display_grid:
            grid = GridTool(size = self.camera.far,division=self.camera.far,grid_color=[1,1,1],center_color=[1,1,0])

            grid.rotate_x(-pi/2)
            self.scene.add(grid)
        


    def update(self):
        if self.rig is not None:
            self.rig.update(self.input_handler, self.timer.delta_time())
        
        self.renderer.render(self.scene, self.camera)