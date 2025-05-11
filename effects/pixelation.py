from material.basic.material import Material


class PixelationEffect(Material):
    def __init__(self,pixel_size:int = 8,resolution = (512,512)) -> None:
        vertex_shader_code = """
                                in vec2 vertex_position;
                                in vec2 vertex_uv;
                                out vec2 uv;
                                void main(){
                                    gl_Position = vec4(vertex_position, 0.0, 1.0);
                                    uv = vertex_uv;
                                }
                             """
        
        fragment_shader_code = """ 
                                in vec2 uv;
                                uniform sampler2D texture_sampler;
                                uniform vec2 resolution;
                                uniform float pixel_size;
                                out vec4 frag_color;
                                void main(){
                                    vec2 pixel_factor = resolution / pixel_size;
                                    vec2 pixelated_uv = floor(uv * pixel_factor) / pixel_factor;
                                    vec4 color = texture(texture_sampler, pixelated_uv);
                                    frag_color = color;
                                }
                                """
        
        super().__init__(vertex_shader_code, fragment_shader_code)

        self.add_uniform("texture_sampler", [None, 1], "sampler2D")
        self.add_uniform("pixel_size", pixel_size, "float")
        self.add_uniform("resolution", resolution, "vec2")

        self.locate_uniforms()