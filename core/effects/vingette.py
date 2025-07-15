from material.basic.material import Material


class VignetteEffect(Material):
    def __init__(self,dim_start:float = 0.4,dim_end:float=1.0,dim_color:list=[0, 0, 0]) -> None:
        vertex_shader_code = """
                                in vec2 vertex_position;
                                in vec2 vertex_uv;
                                out vec2 uv;
                                void main(){
                                    gl_Position = vec4(vertex_position,0.0,1.0);
                                    uv = vertex_uv;
                                }
                             """
        
        framgent_shader_code = """ 
                                in vec2 uv;
                                uniform vec3 dim_color;
                                uniform sampler2D texture_sampler;
                                uniform float dim_start;
                                uniform float dim_end;
                                out vec4 frag_color;

                                void main(){
                                    vec4 color = texture(texture_sampler, uv);

                                    // Convert the UV coordinates to a range of -1 to 1
                                    vec2 position = 2* uv - vec2(1,1);

                                    // Calculate the distance from the center of the screen
                                    float dist = length(position);
                                    
                                    // Calculate the brightness based on the distance
                                    float brightness = (dist - dim_end) / (dim_start - dim_end);
                                    
                                    // Clamp the brightness to the range [0, 1] to prevent oversaturation
                                    brightness = clamp(brightness,0.0,1.0);

                                    // apply dimming effect
                                    frag_color = vec4(brightness * color.rgb,1.0);  
                                }
                                """
        
        super().__init__(vertex_shader_code, framgent_shader_code)

        self.add_uniform("texture_sampler", [None, 1], "sampler2D")
        self.add_uniform("tint_color", dim_color, "vec3")
        self.add_uniform("dim_start", dim_start, "float")
        self.add_uniform("dim_end", dim_end, "float")
        self.locate_uniforms()