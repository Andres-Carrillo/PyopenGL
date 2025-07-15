import pathlib
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")
# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from rendering_tests.template import Test
from core.light.ambient import AmbientLight
from core.light.point import PointLight
from core.material.lighted.phong import PhongMaterial
from core.textures.texture import Texture
from meshes.mesh import Mesh
from tools.point_light_tool import PointLightTool
from math import sin,cos
from core.geometry.simple2D.rectangle import Rectangle

class LightTest(Test):
    def __init__(self):
        super().__init__(title="Light Test", display_grid=False)
        
        brick_texture = Texture("images/brick-wall.jpg")
        normal_map = Texture("images/brick-wall-normal-map.jpg") 
        brick_wall_geo = Rectangle(width=2,height=2)

        self.renderer.toggle_lights()


        self.camera.set_position([0, 0, 6])

        self.ambient_light = AmbientLight(color=[0.1, 0.1, 0.1])
        self.scene.add(self.ambient_light)


        self.point_light = PointLight(color=[1.0, 1.0, 1.0], position=[1, 0, 1])
        self.scene.add(self.point_light)


        point_visualizer = PointLightTool(self.point_light)
        self.point_light.add(point_visualizer)


        phong_mat = PhongMaterial(texture=brick_texture,bump_texture=normal_map,properties={"bump_strength":1},number_of_lights=2)

        self.brick_wall = Mesh(geometry=brick_wall_geo,material=phong_mat)
        self.scene.add(self.brick_wall)



    def update(self):
            
            super().update()
  
            self.point_light.set_position([cos(self.timer.elapsed_time()), sin(self.timer.elapsed_time()), 1])




if __name__ == "__main__":
    test = LightTest()
    test.run()