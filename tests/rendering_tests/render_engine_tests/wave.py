import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)


from meshes.mesh import Mesh
from core.geometry.geometry import Geometry
from material.basic.point import PointMaterial
from material.basic.line import LineMaterial
from math import sin
from numpy import arange
from rendering_tests.template import Test


class WaveTest(Test):
    def __init__(self):
        super().__init__(title="Wave Test",display_grid=False)
        self.camera.set_position([0, 0, 5])
        geometry = Geometry()
        point_material = PointMaterial(
            properties={"base_color": [1, 1, 1],
             "point_size":10}
        )
        
        pos_data = []
        for x in arange(-3.2,3.2,0.3):
            pos_data.append([x,sin(x),0])
        
        geometry.add_attribute("vertex_position", pos_data, "vec3")
        geometry.count_vertices()

        point_mesh = Mesh(geometry, point_material)

        line_material = LineMaterial(
            properties={"base_color": [1, 1, 1],
             "line_width": 2}
        )

        line_mesh = Mesh(geometry, line_material)
        
        self.scene.add(point_mesh)
        self.scene.add(line_mesh)
        
    def update(self) -> None:
        self._base_update()
        # render the scene        
        self.renderer.render(self.scene, self.camera)
       
        

if __name__ == "__main__":
    test = WaveTest()
    test.run()
    test.quit()