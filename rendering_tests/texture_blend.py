import pathlib
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")
# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[1])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from rendering_tests.template import Test
from core.textures.texture import Texture
from geometry.simple2D.rectangle import  Rectangle
from meshes.mesh import Mesh
from material.material import Material
from core.utils.timer import Timer


class AnimatedTextureTest(Test):
    def __init__(self):
        super().__init__(title="Blending Texture Test",display_grid = False,static_camera=True)
        self.camera.set_pos([0, 0, 4])

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
                                uniform sampler2D texture1;
                                uniform sampler2D texture2;
                                in vec2 uv;
                                uniform float time;
                                out vec4 frag_color;
                                void main(){
                                    //vec2 shift_uv = uv + vec2(0,0.2 * sin(6*uv.x + time));
                                    vec4 color1 = texture2D(texture1, uv);
                                    vec4 color2 = texture2D(texture2, uv);
                                    float s = abs(sin(time));
                                    frag_color = s * color1 + (1.0 - s) * color2;
                                }"""
        

        gid_texture = Texture("images/grid.jpg")
        crate_texture = Texture("images/crate.jpg")

        self.blend_mat = Material(vertex_shader_code, fragment_shader_code)

        self.blend_mat.add_uniform("texture1", [gid_texture.texture_reference, 1], "sampler2D")
        self.blend_mat.add_uniform("texture2", [crate_texture.texture_reference, 2], "sampler2D")
        self.blend_mat.add_uniform("time", 0.0, "float")
        self.blend_mat.locate_uniforms()

        geometry = Rectangle(width=2, height=2)

        self.mesh = Mesh(geometry, self.blend_mat)
        self.scene.add(self.mesh)




    def update(self):
        # Timer.sleep(0.016)
        self.blend_mat.uniforms["time"].data += self.timer.delta_time()
        super().update()





if __name__ == "__main__":
    test = AnimatedTextureTest()
    test.run()
    # test.quit()