from material.material import Material


class HBlurEffect(Material):
    def __init__(self,texture_size:list = [512,512],blur_radius:int = 20) -> None:
        vertex_shader_code = """
                                in vec2 vertex_position;
                                in vec2 vertex_uv;
                                out vec2 uv;
                                void main(){
                                    gl_Position = vec4(vertex_position,0.0,1.0);
                                    uv = vertex_uv;
                                }
                             """
        
        fragment_shader_code = """ 
                                in vec2 uv;
                                uniform sampler2D texture_sampler;
                                uniform vec2 texture_size;
                                uniform int blur_radius;
                                out vec4 frag_color;
                                
                                void main()
                                {
                                    vec2 pixel_to_texture = 1/texture_size;
                                    vec4 avg_color = vec4(0.0);
                                    for(int x_offset = -blur_radius; x_offset <= blur_radius; x_offset++)
                                    {
                                        float wieght = blur_radius - abs(x_offset) + 1;
                                        vec2 uv_offset = vec2(x_offset,0) * pixel_to_texture;
                                        avg_color += texture2D(texture_sampler, uv + uv_offset) * wieght;
                                    }
                                    avg_color /= avg_color.a;
                                    frag_color = avg_color;
                                }
                                """
        
        super().__init__(vertex_shader_code, fragment_shader_code)

        self.add_uniform("texture_sampler", [None, 1], "sampler2D")
        self.add_uniform("texture_size", texture_size, "vec2")
        self.add_uniform("blur_radius", blur_radius, "int")
        self.locate_uniforms()