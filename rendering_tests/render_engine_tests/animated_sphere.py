import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)


from rendering_tests.template import Test

from core.geometry.simple3D.sphere import Sphere
from material.basic.material import Material
from meshes.mesh import Mesh
from core.utils.timer import Timer



class AnimationTest(Test):
    def __init__(self):
        super().__init__(title="Animation Test")
        self.camera.set_position([0, 0, 7])

        geometry = Sphere(radius=3,seg_radius=128,seg_height=128)

        vertex_shader = """
                        uniform mat4 model_matrix;
                        uniform mat4 view_matrix;
                        uniform mat4 projection_matrix;
                        in vec3 vertex_position;
                        in vec3 vertex_color;
                        out vec3 color;
                        out vec3 position;
                        uniform float time;
                        void main(){
                            float offset = 0.2* sin(8.0*vertex_position.x + time);
                            vec3 pos = vertex_position + vec3(0, offset, 0);
                            gl_Position = projection_matrix * view_matrix * model_matrix * vec4(pos, 1.0);
                            color = vertex_color;
                            position = vertex_position;
                        }"""


        fragment_shader = """
                        in vec3 color;
                        in vec3 position;
                        uniform float time;
                        out vec4 frag_color;
                        void main(){
                            float r = abs(sin(time));
                            vec4 c = vec4(0.5*r, 0.25*r, 0.75*r, 0.0);
                            //vec3 color = mod(position, 1.0);
                            frag_color = vec4(color, 1.0) + c;
                        }"""

        material = Material(vertex_shader, fragment_shader)
        material.add_uniform("time", 0.0, "float")
        material.locate_uniforms()
        self.time = 0

        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)


    def update(self):
        self.renderer.update_window_size(self.window_width, self.window_height)
        # print("the delta time is: ", self.timer.delta_time())
        # Timer.sleep(0.016)
        self.time += self.timer.delta_time()
        self.mesh.material.uniforms["time"].data = self.time
        # self.mesh.rotate_x(0.00337)
        # self.mesh.rotate_y(0.00514)
        self.renderer.render(self.scene, self.camera)


if __name__ == "__main__":
    animation_test = AnimationTest()
    animation_test.run()
