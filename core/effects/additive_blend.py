from core.material.basic.material import Material
from core.textures.texture import Texture

class AdditiveBlendEffect(Material):
    def __init__(self,blend_texture:Texture = None,src_strength:float = 1.0,blend_strength:float = 1.0 ) -> None:
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
                                uniform sampler2D blend_texture;
                                uniform float src_strength;
                                uniform float blend_strength;
                                out vec4 frag_color;
                                void main(){
                                    vec4 og_color = texture2D(texture_sampler, uv);
                                    vec4 blend_color = texture2D(blend_texture, uv);
                                    vec4 color = src_strength * og_color + blend_strength * blend_color;
                                    frag_color = color;
                                }
                                """
        
        super().__init__(vertex_shader_code, fragment_shader_code)

        self.add_uniform("texture_sampler", [None, 1], "sampler2D")
        self.add_uniform("blend_texture", [blend_texture.texture_reference, 2], "sampler2D")
        self.add_uniform("src_strength", src_strength, "float")
        self.add_uniform("blend_strength", blend_strength, "float")
        self.locate_uniforms()