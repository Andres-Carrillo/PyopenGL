import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[1])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)


from meshes.mesh import Mesh
from geometry.box import Geometry
from material.surface import SurfaceMaterial
from rendering_tests.template import Test


class CustomGeoTest(Test):

    def __init__(self):
        super().__init__(title="Custom Geometry Test",display_grid=False)  
        self.camera.set_pos([0, 0, 0.1])
        geometry = Geometry()   
        
        material = SurfaceMaterial(
            {'use_vertex_colors':True,
             "wire_frame":False,}
        )

        p0 = [-0.1,0.1,0.0]
        p1 = [0.0,0.0,0.0]
        p2 = [0.1,0.1,0.0]
        p3 = [-0.2,-0.2,0.0]
        p4 = [0.2,-0.2,0.0]

        pos_data = [p0,p3,p1, p1,p3,p4, p1,p4,p2]



        geometry.add_attribute("vertex_position", pos_data, "vec3")
        
        R = [1,0,0]
        G = [0,0.25,0]
        Y = [1,1,0]
        B = [0,0,1]

        color_data = [R,G,Y, Y,G,G, Y,G,R]
        geometry.add_attribute("vertex_color", color_data, "vec3")
        geometry.count_vertices()
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)




    
    def update(self):
        self.renderer.render(self.scene, self.camera)






if __name__ == "__main__":
    test = CustomGeoTest()
    test.run()
    test.quit()