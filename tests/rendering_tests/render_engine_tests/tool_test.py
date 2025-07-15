import pathlib
import sys

# Get the package directorya
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

print(package_dir)

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from tools.axes_tool import AxesAid
from tools.grid import GridTool
from tools.movement_rig import MovementRig
from math import pi
from rendering_tests.template import Test

class ToolTest(Test):
    def __init__(self):
        super().__init__(title="Tool Test")
        
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0.5, 1, 5])

        self.scene.add(self.rig)

        axes = AxesAid(axis_len=1)

        self.scene.add(axes)

        grid = GridTool(size = self.camera.far,division=self.camera.far,grid_color=[1,1,1],center_color=[1,1,0])

        grid.rotate_x(-pi/2)
        self.scene.add(grid)


    def update(self):
        self.rig.update(self.input_handler,self.timer.delta_time())
        super().update()


if __name__ == "__main__":
    test = ToolTest()
    test.run()