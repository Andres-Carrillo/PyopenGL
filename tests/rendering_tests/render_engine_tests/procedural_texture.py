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
from core.geometry.simple3D.sphere import Sphere
from rendering_tests.template import Test
from core.meshes.mesh import Mesh
from core.material.basic.material import Material


class ProceduralTextureTest(Test):
    def __init__(self):
        super().__init__(title="Noise Texture Test",display_grid = False,static_camera=True)
        self.camera.set_position([0, 0, 1.5])

        vertex_shader_code = """
                                uniform mat4 projection_matrix;
                                uniform mat4 view_matrix;
                                uniform mat4 model_matrix;
                                
                                in vec3 vertex_position;
                                in vec2 vertex_uv;
                                out vec2 uv;
                                void main(){
                                    vec4 pos = vec4(vertex_position,1.0);
                                    gl_Position = projection_matrix * view_matrix * model_matrix * pos;
                                    uv = vertex_uv;
                                }"""

        fragment_shader_code = """

                                float random(vec2 uv){
                                    return fract(235711.0 * sin(14.337 *uv.x + 42.428 * uv.y));
                                }


                                float box_random(vec2 uv, float scale){
                                    vec2 uv_scaled = floor(uv * scale);
                                    return random(uv_scaled);
                                }

                                float smooth_random(vec2 uv, float scale){
                                    vec2 integer_part = floor(uv * scale);
                                    vec2 fractional_part = fract(uv * scale);

                                    float a = random(integer_part);
                                    float b = random(integer_part + vec2(1.0, 0.0));
                                    float c = random(integer_part + vec2(0.0, 1.0));
                                    float d = random(integer_part + vec2(1.0, 1.0));

                                    return mix(
                                                mix(a, b, fractional_part.x),
                                                mix(c, d, fractional_part.x),
                                                fractional_part.y);
                                }


                                float fractal_random(vec2 uv, float scale){
                                    float val = 0.0;
                                    float amp = 0.5;

                                    for (int i = 0; i < 6; i++){
                                        val += amp * smooth_random(uv, scale);
                                        scale *= 2.0;
                                        amp *= 0.5;
                                    }

                                    return val;
                                
                                }

                                // cloud generator
                                vec4 cloud_gen(vec2 uv, float scale){
                                    float r = fractal_random(uv, scale);
                                    vec4 color1 = vec4(0.5,0.7,1.0,1.0);
                                    vec4 color2 = vec4(1.0,1.0,1.0,1.0);
                                    
                                    return mix(color1, color2, r);
                                }

                                // lava generator
                                vec4 lava_gen(vec2 uv, float scale){
                                    float r = fractal_random(uv, scale);
                                    vec4 color1 = vec4(1.0,0.8,0.0,1.0);
                                    vec4 color2 = vec4(0.8,0.0,0.0,1.0);

                                    return mix(color1, color2, r);  
                                }

                                // marble generator
                                vec4 marble_gen(vec2 uv, float scale){
                                    float t = fractal_random(uv, scale);
                                    float r = abs(sin(20*t));
                                    
                                    vec4 color1 = vec4(0.0,0.2,0.0,1.0);
                                    vec4 color2 = vec4(1.0,1.0,1.0,1.0);

                                    return mix(color1,color2,r);
                                }

                                //wood grain generator
                                vec4 grain_gen(vec2 uv, float scale){
                                    float t = 80 * uv.y + 20 * fractal_random(uv, scale);
                                    float r = clamp(2 * abs(sin(t)),0,1);
                                    vec4 color1 = vec4(0.3,0.2,0.0,1.0);
                                    vec4 color2 = vec4(0.6,0.4,0.2,1.0);

                                    return mix(color1,color2,r);
                                }

                                in vec2 uv;
                                out vec4 frag_color;
                                void main(){
                                    //frag_color = cloud_gen(uv, 4.0);
                                    frag_color = lava_gen(uv, 40.0);
                                    //frag_color = marble_gen(uv, 4.0);

                                    //frag_color = grain_gen(uv, 2.0);
                                }"""
    
        
        self.mat = Material(vertex_shader_code, fragment_shader_code)

        self.mat.locate_uniforms()


        geometry = Sphere(radius=0.5,seg_height=64)

        self.mesh = Mesh(geometry, self.mat)
        self.scene.add(self.mesh)


    def update(self):
        self.mesh.rotate_x(0.5 * self.timer.delta_time())

        super().update()



if __name__ == "__main__":
    test = ProceduralTextureTest()
    test.run()
    # test.timer = Timer()