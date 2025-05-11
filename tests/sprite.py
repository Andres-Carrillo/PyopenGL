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
from geometry.simple2D.rectangle import Rectangle
from meshes.mesh import Mesh
from core.textures.texture import Texture
from material.basic.sprite import Sprite
from math import floor


class SpriteTest(Test):

    def __init__(self):
        super().__init__(title="Sprite Test", display_grid=True)
        self.rig.set_pos([0, 0.5, 3])

        geometry = Rectangle(width=1, height=1)
        tile_set = Texture("images/cloud.jpg")
        tile_set.set_wrap_mode("CLAMP_TO_EDGE")
        sprite_material = Sprite(texture=tile_set,properties={
            "billboard": True,
            "tile_count": [3,4],
            "tile_number": 0.0,
        })

        self.tilesPerSecond= 4

        self.sprite = Mesh(geometry, sprite_material)
        self.sprite.set_pos([0, 0.5, 0])
        self.scene.add(self.sprite)

    def update(self):
        self._base_update()
    
        tile_number = floor(self.timer.elapsed_time() * self.tilesPerSecond)
        self.sprite.material.uniforms["tile_number"].data = tile_number
        self.sprite.look_at(self.camera.get_global_pos())
        # Update the scene with the texture applied
        self.renderer.render(self.scene, self.camera)



if __name__ == "__main__":
    test = SpriteTest()
    test.run()
    # test.quit()