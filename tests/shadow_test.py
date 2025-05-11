import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[1])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)



from tests.template import Test
from geometry.simple3D.sphere import Sphere
from geometry.simple2D.rectangle import Rectangle
from core.light.ambient import AmbientLight
from core.light.directional import DirectionalLight
from core.light.point import PointLight
from material.lighted.phong import PhongMaterial
from material.lighted.lambert import LambertMaterial
from tools.directional_light_tool import DirectionalLightTool
from core.textures.texture import Texture
from material.basic.texture import TextureMaterial
from meshes.mesh import Mesh
from math import sin,cos,pi

class ShadowTest(Test):
    def __init__(self):
        super().__init__(title="shadow Test", display_grid=False)
        self.camera.set_position([0, 0, 2])

        ambient_light = AmbientLight(color=[0.2, 0.2, 0.2])
        self.scene.add(ambient_light)

        self.directional_light = DirectionalLight(color=[0.9,0.9,0.9],direction=[-1, -1,0])
        self.directional_light.set_position([2, 4, 0])
        self.scene.add(self.directional_light)

        self.directional_light_tool = DirectionalLightTool(self.directional_light)
        self.directional_light.add(self.directional_light_tool)


        sphere_geo = Sphere()
        phong_material = LambertMaterial(texture=Texture("images/grid.jpg"),number_of_lights=2,use_shadow=True)

        self.renderer.enable_shadows(shadow_light=self.directional_light,resolution=[self.window_width, self.window_height])

        self.sphere_1 = Mesh(geometry=sphere_geo, material=phong_material)

        self.sphere_1.set_position([-2, 1, 0])
        self.scene.add(self.sphere_1)

        self.sphere_2 = Mesh(geometry=sphere_geo, material=phong_material)
        self.sphere_2.set_position([1, 2.2, -0.5])
        self.scene.add(self.sphere_2)

        floor = Mesh(Rectangle(width=20, height=20), phong_material)
        floor.rotate_x(-pi / 2)
        self.scene.add(floor)
        

        
        # depth_texture = self.renderer.shadow_object.render_target.texture
        # shadow_display = Mesh(Rectangle(), TextureMaterial(depth_texture))
        # shadow_display.set_position([-1, 3, 0])
        # self.scene.add(shadow_display)

    def update(self):
        self.timer.sleep(0.016)
        self.directional_light.rotate_y(0.01337,False)
        shadow_camera = self.renderer.shadow_object.camera
       
        # self.sphere_1.rotate_y(0.01337,True)
        super().update()
        # self.renderer.render(self.scene, shadow_camera)
        # self.renderer.shadow_object.render_target.uni



        


if __name__ == "__main__":
    shadow_test = ShadowTest()
    shadow_test.run()