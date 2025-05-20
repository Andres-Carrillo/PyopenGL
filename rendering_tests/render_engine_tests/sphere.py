import pathlib
import sys
# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])
# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from meshes.mesh import Mesh

from core.rendering.camera import Camera
from core.rendering.renderer import Renderer
from core.rendering.scene import Scene
from geometry.simple3D.sphere import Sphere
from material.basic.material import Material

from rendering_tests.template import Test
from core.utils.timer import Timer


class SphereTest(Test):

    """ Render a spinning sphere with gradient colors """
    def __init__(self):
        super().__init__(title="Sphere Test")
        self.camera.set_position([0, 0, 7])
        geometry = Sphere(radius=3)
        vs_code = """
        uniform mat4 model_matrix;
        uniform mat4 view_matrix;
        uniform mat4 projection_matrix;
        in vec3 vertex_position;
        out vec3 position;
        void main()
        {
            vec4 pos = vec4(vertex_position, 1.0);
            gl_Position = projection_matrix * view_matrix * model_matrix * pos;
            position = vertex_position;
        }
        """
        fs_code = """
        in vec3 position;
        out vec4 frag_color;
        void main()
        {
            vec3 color = mod(position, 1.0);
            frag_color = vec4(color, 1.0);
        }
        """
        material = Material(vs_code, fs_code)
        material.locate_uniforms()
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        Timer.sleep(0.016)
        
        self.mesh.rotate_x(0.00337)
        self.mesh.rotate_y(0.00514)
        super().update()
        # self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    test = SphereTest()
    test.run()