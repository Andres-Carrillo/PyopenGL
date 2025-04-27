from material.material import Material
from core.uniform import Uniform
import OpenGL.GL as gl
class BasicMaterial(Material):

    def __init__(self):
        vertex_shader_code = """
                            uniform mat4 projection_matrix;
                            uniform mat4 view_matrix;
                            uniform mat4 model_matrix;
                            in vec3 vertex_position;
                            in vec3 vertex_color;
                            out vec3 color;

                            void main(){
                                gl_Position = projection_matrix * view_matrix * model_matrix * vec4(vertex_position,1.0);
                                color = vertex_color;
                            }
                            """
        
        fragment_shader_code = """
                            uniform vec3 base_color;
                            uniform bool use_vertex_colors;
                            in vec3 color;
                            out vec4 frag_color;
                            
                            void main(){
                                vec4 temp_color = vec4(base_color,1.0);
                                
                                if (use_vertex_colors){
                                    temp_color = vec4(color,1.0);
                                }

                                frag_color = temp_color;
                            }
            """
        
        super().__init__(vertex_shader_code, fragment_shader_code)
        self.add_uniform("base_color", (1.0, 0.0, 0.0), "vec3")
        self.add_uniform("use_vertex_colors", False, "bool")
        self.locate_uniforms()
