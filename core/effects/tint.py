from material.basic.material import Material


class TintEffect(Material):
    def __init__(self,tint_color=[1, 0, 0]):
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
                                uniform vec3 tint_color;
                                uniform sampler2D texture_sampler;
                                out vec4 frag_color;

                                void main(){
                                    vec4 color = texture(texture_sampler, uv);
                                    float gray = (color.r + color.g + color.b) / 3.0;
                                    frag_color = vec4(gray * tint_color,1.0);
                                }
                                """
        
        super().__init__(vertex_shader_code, framgent_shader_code)

        self.add_uniform("texture_sampler", [None, 1], "sampler2D")
        self.add_uniform("tint_color", tint_color, "vec3")
        self.locate_uniforms()