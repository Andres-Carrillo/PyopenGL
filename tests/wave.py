import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[1])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)


from core.mesh import Mesh
from geometry.box import Geometry
from material.point_material import PointMaterial
from material.line_material import LineMaterial
from math import sin
from numpy import arange
from tests.template import Test


class WaveTest(Test):
    def __init__(self):
        super().__init__(title="Wave Test")
        self.camera.set_pos([0, 0, 5])
        geometry = Geometry()
        point_material = PointMaterial(
            {"base_color": [1, 1, 0],
             "point_size":10}
        )
        
        pos_data = []
        for x in arange(-3.2,3.2,0.3):
            pos_data.append([x,sin(x),0])
        
        geometry.addAttribute("vertex_position", pos_data, "vec3")
        geometry.countVertices()

        point_mesh = Mesh(geometry, point_material)

        line_material = LineMaterial(
            {"base_color": [1, 0, 1],
             "line_width": 2}
        )

        line_mesh = Mesh(geometry, line_material)
        
        self.scene.add(point_mesh)
        self.scene.add(line_mesh)
       
        

if __name__ == "__main__":
    test = WaveTest()
    test.run()
    test.quit()