from material.basic.material import Material


class TemplateEffect(Material):
    def __init__(self):
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
                                out vec4 frag_color;
                                void main(){
                                    vec4 color = texture2D(texture_sampler, uv);
                                    frag_color = color;
                                }
                                """
        
        super().__init__(vertex_shader_code, fragment_shader_code)

        self.add_uniform("texture_sampler", [None, 1], "sampler2D")
        self.locate_uniforms()