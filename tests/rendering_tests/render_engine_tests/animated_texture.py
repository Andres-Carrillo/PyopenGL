import pathlib
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")
# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from rendering_tests.template import Test
from core.textures.texture import Texture
from core.geometry.simple2D.rectangle import  Rectangle
from core.meshes.mesh import Mesh
from core.material.basic.material import Material


class AnimatedTextureTest(Test):
    def __init__(self):
        super().__init__(title="Animated Texture Test",display_grid = False,static_camera=True)
        self.camera.set_position([0, 0, 4])

        vertex_shader_code = """
                                uniform mat4 projection_matrix;
                                uniform mat4 view_matrix;
                                uniform mat4 model_matrix;
                                
                                in vec3 vertex_position;
                                in vec2 vertex_uv;
                                out vec2 uv;
                                void main(){
                                    gl_Position = projection_matrix * view_matrix * model_matrix * vec4(vertex_position,1.0);
                                    uv = vertex_uv;
                                }"""
        

        fragment_shader_code = """
                                uniform sampler2D texture;
                                in vec2 uv;
                                uniform float time;
                                out vec4 frag_color;
                                void main(){
                                    vec2 shift_uv = uv + vec2(0,0.2 * sin(6*uv.x + time));
                                    frag_color = texture2D(texture, shift_uv);
                                }"""
        

        gidTexture = Texture("images/grid.jpg")

        self.wave_mat = Material(vertex_shader_code, fragment_shader_code)
        self.wave_mat.add_uniform("texture", [gidTexture.texture_reference, 1], "sampler2D")
        self.wave_mat.add_uniform("time", 0.0, "float")
        self.wave_mat.locate_uniforms()

        geometry = Rectangle(width=2, height=2)

        self.mesh = Mesh(geometry, self.wave_mat)
        self.scene.add(self.mesh)




    def update(self):
        self.wave_mat.uniforms["time"].data += self.timer.delta_time()
        super().update()





if __name__ == "__main__":
    test = AnimatedTextureTest()
    test.run()
    # test.quit()