import pathlib
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")
# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)


from core.geometry.simple3D.sphere import Sphere

from rendering_tests.template import Test
from core.light.ambient import AmbientLight
from core.light.directional import DirectionalLight
from core.light.point import PointLight
from core.material.lighted.phong import PhongMaterial
from core.material.lighted.lambert import LambertMaterial
from core.material.lighted.flat import FlatMaterial
from core.textures.texture import Texture
from meshes.mesh import Mesh
from tools.directional_light_tool import DirectionalLightTool
from tools.point_light_tool import PointLightTool
from math import sin,cos,pi
from core.material.basic.material import Material
from core.geometry.simple2D.rectangle import Rectangle

class LightTest(Test):
    def __init__(self):
        super().__init__(title="Light Test", display_grid=False)

     
        

        noise_texture = Texture("images/rgb-noise.jpg")
        water_texture = Texture("images/pool_water.jpg")   

        self.distort_mat = PhongMaterial(texture=water_texture,noise=noise_texture,number_of_lights=3,use_shadow=True)



       

        self.camera.set_position([0, 0, 6])

        grid_texture = Texture(image_path="images/grid.jpg")

        self.ambient_light = AmbientLight(color=[0.1, 0.1, 0.1])
        self.scene.add(self.ambient_light)

        self.directional_light = DirectionalLight(color=[0.8, 0.8, 0.8], direction=[-1, -1, 0])
        self.scene.add(self.directional_light)

        self.point_light = PointLight(color=[0.9, 0, 0], position=[1, 1, 0.8])
        self.scene.add(self.point_light)


        # add the light tools to the scene
        directional_visualizer = DirectionalLightTool(self.directional_light)
        self.directional_light.set_position([3, 4, 0])
        self.directional_light.add(directional_visualizer)

        point_visualizer = PointLightTool(self.point_light)
        self.point_light.add(point_visualizer)

        # geometry of all the objects
        sphere_geo = Sphere()
        
        #flat material type
        flat_material = FlatMaterial(properties={"base_color":[0.2, 0.5, 0.5]},number_of_lights=3)

        #lambert material type  
        lambert_mat = LambertMaterial(properties={"base_color":[0.2, 0.5, 0.5]},number_of_lights=3,use_shadow=True)

        #phong material type
        phong_mat = PhongMaterial(properties={"base_color":[0.2, 0.5, 0.5]},number_of_lights=3,use_shadow=True)

        #create flat lighting sphere:
        self.flat_sphere = Mesh(geometry=sphere_geo, material=flat_material)
        self.flat_sphere.set_position([-2.2, 1, 0])

        # create lambert lighting sphere:
        self.lambert_sphere = Mesh(geometry=sphere_geo, material=lambert_mat)
        self.lambert_sphere.set_position([0, 1, 0])


        # # create phong lighting sphere:
        self.phong_sphere = Mesh(geometry=sphere_geo, material=phong_mat)
        self.phong_sphere.set_position([2.2, 1, 0])


        floor = Mesh(Rectangle(width=20, height=20), phong_mat)
        floor.set_position([0, 0, -1])
        floor.rotate_x(-pi / 2)

        #water sphere
        self.water_sphere = Mesh(geometry=sphere_geo, material=self.distort_mat)
        self.water_sphere.set_position([0, 4.2, 0])

        # add the spheres to the scene
        self.scene.add(self.flat_sphere)
        self.scene.add(self.lambert_sphere)
        self.scene.add(self.phong_sphere)
        self.scene.add(floor)
        self.scene.add(self.water_sphere)
        self.renderer.toggle_lights()
        self.renderer.enable_shadows(self.directional_light)
       


    def update(self):
            self._base_update()
            # self.directional_light.set_direction([-1, sin(0.5*self.timer.elapsed_time()), 0])
            # super().update()
            time_delta = self.timer.delta_time()
            self.point_light.set_position([cos(self.timer.elapsed_time()), sin(self.timer.elapsed_time()), 1])

            self.directional_light.set_direction([sin(self.timer.elapsed_time()), sin(self.timer.elapsed_time()), -2])
            self.directional_light.rotate_y(0.0137,True)

            
           
            # self.flat_sphere.material.uniforms["time"].data += time_delta
            # self.lambert_sphere.material.uniforms["time"].data += time_delta
            self.water_sphere.material.uniforms["time"].data += time_delta * 2

            self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    test = LightTest()
    test.run()