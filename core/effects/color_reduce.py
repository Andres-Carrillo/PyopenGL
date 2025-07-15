from core.material.basic.material import Material


class ColorReduceEffect(Material):
    def __init__(self,levels:int = 4) -> None:
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
                                uniform sampler2D texture_sampler;
                                uniform int levels;
                                out vec4 frag_color;
                                void main(){
                                    vec4 color = texture(texture_sampler, uv);
                                    vec4 reduced_color = round(color * levels) / levels;
                                    reduced_color.a = 1.0; // Set alpha to 1.0
                                    frag_color = reduced_color;
                                }
                                """
        
        super().__init__(vertex_shader_code, framgent_shader_code)

        self.add_uniform("texture_sampler", [None, 1], "sampler2D")
        self.add_uniform("levels", levels, "int")
        self.locate_uniforms()