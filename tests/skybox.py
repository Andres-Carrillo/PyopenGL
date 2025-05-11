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
from core.textures.texture import Texture
from material.basic.texture import TextureMaterial
from geometry.simple2D.rectangle import  Rectangle
from geometry.simple3D.sphere import Sphere
from meshes.mesh import Mesh  

class SkyboxTest(Test):
    def __init__(self):
        super().__init__(title="Skybox Test")
        sky_geo = Sphere(radius=50)
        sky_mat = TextureMaterial(Texture("images/sky.jpg"))
        sky = Mesh(sky_geo, sky_mat)
        self.scene.add(sky)

        grass_geo = Rectangle(width=self.camera.far, height=self.camera.far)
        grass_mat = TextureMaterial(Texture("images/grass.jpg"))
        grass = Mesh(grass_geo, grass_mat)
        grass.rotate_x(-3.14/2)

        self.scene.add(grass)



if __name__ == "__main__":
    test = SkyboxTest()
    test.run()
    test.quit()