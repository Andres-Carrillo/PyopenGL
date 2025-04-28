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

class Test(Base):

    def __init__(self,clear_color=[0.2, 0.2, 0.2], title="Test"):
        super().__init__(title=title)
        self.renderer = Renderer(clear_color=clear_color)
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_pos([0, 0, 4])
        


    def update(self):
        self.renderer.render(self.scene, self.camera)