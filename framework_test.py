from core.app_base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.box import BoxGeometry
from material.surface_material import SurfaceMaterial

import OpenGL.GL as gl


class Test(Base):

    def __init__(self):
        super().__init__()
        self.renderer = Renderer(clear_color=[1, 1, 1])
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.camera.set_pos([0, 0, 4])
        
        geometry = BoxGeometry()
        material = SurfaceMaterial(
            {'use_vertex_colors':False}
        )


        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)



    def update(self):
        self.mesh.rotate_y(0.00514)
        self.mesh.rotate_x(0.00337)

        self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    test = Test()
    test.run()
    test.quit()

    # Test_2(screen_size=[800,600]).run()



