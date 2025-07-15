import pathlib
import sys

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from rendering_tests.template import Test
from core.textures.texture import Texture
from core.geometry.simple3D.sphere import Sphere
from meshes.mesh import Mesh
from core.material.basic.material import Material


class AnimatedTextureTest(Test):
    def __init__(self):
        super().__init__(title="Noise Texture Test",display_grid = False,static_camera=True)
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

                                vec4 time_distort(vec2 uv, float time,sampler2D noise, sampler2D image){
                                    vec2 uv_shift = uv + vec2(0.3,0.07) * time;
                                    vec4 noise_vals = texture2D(noise, uv_shift);
                                    vec2 uv_noise = uv + 0.02 * noise_vals.rg;
                                    return texture2D(image, uv_noise);
                                };

                                uniform sampler2D noise;
                                uniform sampler2D image;
                                in vec2 uv;
                                uniform float time;
                                out vec4 frag_color;
                                void main(){
                                    //vec2 uv_shift = uv + vec2(0.3,0.07) * time;
                                    //vec4 noise_vals = texture2D(noise, uv_shift);
                                    //vec2 uv_noise = uv + 0.02 * noise_vals.rg;
                                    frag_color = time_distort(uv,time,noise,image);//texture2D(image, uv_noise);
                                }"""
        
        noise_texture = Texture("images/rgb-noise.jpg")
        image_texture = Texture("images/pool_water.jpg")
        
        self.distort_mat = Material(vertex_shader_code, fragment_shader_code)

        self.distort_mat.add_uniform("noise", [noise_texture.texture_reference, 1], "sampler2D")
        self.distort_mat.add_uniform("image", [image_texture.texture_reference, 2], "sampler2D")
        self.distort_mat.add_uniform("time", 0.0, "float")
        self.distort_mat.locate_uniforms()

        geometry = Sphere(radius=2.0,seg_radius=128,seg_height=128)

        self.mesh = Mesh(geometry, self.distort_mat)
        self.scene.add(self.mesh)



    def update(self):
        # Timer.sleep(0.016)
        
        self.distort_mat.uniforms["time"].data += self.timer.delta_time()
        self.mesh.rotate_x(0.003)
        self.mesh.rotate_y(0.007)
        super().update()


if __name__ == "__main__":
    test = AnimatedTextureTest()
    test.run()