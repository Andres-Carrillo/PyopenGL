import pathlib
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")
# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[1])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from tests.template import Test
from geometry.sphere import Sphere
from core.light.ambient import AmbientLight
from core.light.directional import DirectionalLight
from core.light.point import PointLight
from material.phong import PhongMaterial
from material.lambert import LambertMaterial
from material.flat import FlatMaterial
from core.textures.texture import Texture
from meshes.mesh import Mesh
from math import sin,cos

class LightTest(Test):
    def __init__(self):
        super().__init__(title="Light Test", display_grid=False)
        self.camera.set_pos([0, 0, 6])

        grid_texture = Texture(image_path="images/grid.jpg")

        self.ambient_light = AmbientLight(color=[0.1, 0.1, 0.1])
        self.scene.add(self.ambient_light)

        self.directional_light = DirectionalLight(color=[1, 1, 1], direction=[0, 0, 0])
        self.scene.add(self.directional_light)

        self.point_light = PointLight(color=[1, 0, 0], position=[1, 1, 0.8])
        self.scene.add(self.point_light)

        # geometry of all the objects
        sphere_geo = Sphere()
        
        #flat material type
        flat_material = FlatMaterial(properties={"base_color":[0.6,0.2,0.2]},number_of_lights=3)

        #lambert material type  
        lambert_mat = LambertMaterial(texture=grid_texture,number_of_lights=3)

        #phong material type
        phong_mat = PhongMaterial(properties={"base_color":[0.5,0.5,1.0]},number_of_lights=3)

        #create flat lighting sphere:
        self.flat_sphere = Mesh(geometry=sphere_geo, material=flat_material)
        self.flat_sphere.set_pos([-2.2, 0, 0])

        # create lambert lighting sphere:
        self.lambert_sphere = Mesh(geometry=sphere_geo, material=lambert_mat)
        self.lambert_sphere.set_pos([0, 0, 0])


        # # create phong lighting sphere:
        self.phong_sphere = Mesh(geometry=sphere_geo, material=phong_mat)
        self.phong_sphere.set_pos([2.2, 0, 0])

        # add the spheres to the scene
        self.scene.add(self.flat_sphere)
        self.scene.add(self.lambert_sphere)
        self.scene.add(self.phong_sphere)


    def update(self):
            super().update()
            # self.point_light.set_pos([cos(self.timer.elapsed_time()), sin(self.timer.elapsed_time()), 1])
            # self.point_light.color = ([cos(self.timer.elapsed_time()), sin(self.timer.elapsed_time()), 1])

            # self.directional_light.set_direction([-1, sin(self.timer.elapsed_time()), -2])
            
            # self.lambert_sphere.rotate_y(0.01)
            # self.lambert_sphere.rotate_x(0.01)
            # self.phong_sphere.rotate_y(0.01)
            # self.phong_sphere.rotate_x(0.01)
            # self.flat_sphere.rotate_y(0.01) 
            # self.flat_sphere.rotate_x(0.01)  

if __name__ == "__main__":
    test = LightTest()
    test.run()