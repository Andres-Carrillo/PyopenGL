from material.light import LightMaterial
from core.textures.texture import Texture
import OpenGL.GL as gl

class FlatMaterial(LightMaterial):
    def __init__(self,texture:Texture=None, properties:dict={},number_of_lights:int = 1) -> None:
        vertex_shader_code = """
                                // ========= Base Light Struct =========:
                                struct Light{
                                    int light_type;
                                    vec3 color;
                                    vec3 direction;
                                    vec3 position;
                                    vec3 attenuation;
                                };

                                vec3 calculate_light(Light light, vec3 point_pos,vec3 point_normal){
                                    float ambient = 0.0;
                                    float diffuse = 0.0;
                                    float specular = 0.0;
                                    float attenuation = 0.0;
                                    vec3 light_dir = vec3(0.0,0.0,0.0);

                                    // ========= setup variables based on type of light =========:
                                        // ambient light:
                                    if (light.light_type == 0){ 
                                        ambient = 1.0;
                                    }   // directional light:
                                    else if (light.light_type == 1){ 
                                        light_dir = normalize(light.direction);
                                    }   // point light:
                                    else if (light.light_type == 2){ 
                                        light_dir = normalize(point_pos - light.position);
                                        float distance = length(light.position - point_pos);
                                        attenuation = 1.0 / (light.attenuation[0] + 
                                                                light.attenuation[1] * distance +
                                                                    light.attenuation[2] * distance * distance);
                                    }

                                    // ========= calculate the diffuse  values for directional and point lights =========:
                                    if (light.light_type > 1){
                                        point_normal = normalize(point_normal);
                                        diffuse = max(dot(point_normal, -light_dir), 0.0);
                                        diffuse = diffuse * attenuation;
                                    }

                                    return light.color * (ambient + diffuse + specular);
                                }
                             """ + LightMaterial.generate_light_uniform_list(number_of_lights) + """ \n """ + """
                                    uniform mat4 projection_matrix;
                                    uniform mat4 view_matrix;
                                    uniform mat4 model_matrix;
                                    in vec3 vertex_position;
                                    in vec3 face_normal;
                                    in vec2 vertex_uv;
                                    out vec2 uv;
                                    out vec3 light;

                                    void main(){
                                        gl_Position = projection_matrix * view_matrix * model_matrix * vec4(vertex_position,1.0);
                                        uv  = vertex_uv;
                                        vec3 position = vec3(model_matrix * vec4(vertex_position,1.0)); 
                                        vec3 normal = normalize(vec3(model_matrix * vec4(face_normal,0.0)));
                                        light = vec3(0.0,0.0,0.0); 
                                        """ + LightMaterial.generate_light_sum(number_of_lights) + """ \n """ + """

                                    }

                                 """
            
        fragment_shader_code = """
                                uniform vec3 base_color;
                                uniform bool use_texture;
                                uniform sampler2D texture_sampler;
                                in vec2 uv;
                                in vec3 light;
                                out vec4 frag_color;
                                void main(){
                                    // set the color to the base color with full alpha
                                    vec4 color = vec4(base_color,1.0);
                                    
                                    // if texture is used, use the texture color
                                    if (use_texture){
                                        color *= texture(texture_sampler,uv);
                                    }

                                    // apply lighting to color
                                    color *= vec4(light,1.0);

                                    // set the fragment color
                                    frag_color = color;
                                }
                                """
        
        # handles creating the shader program and linking the shaders to the program
        # also handles setting up light uniforms based on the number of lights
        super().__init__(number_of_lights,vertex_shader_code,fragment_shader_code)

        self.add_uniform("base_color", [1.0, 1.0, 1.0], "vec3")
        if texture is None:
            self.add_uniform("use_texture", False, "bool")
        else:
            self.add_uniform("use_texture", True, "bool")
            self.add_uniform("texture_sampler", [texture.texture_reference,1], "sampler2D")

        self.locate_uniforms()

        self.settings['double_sided'] = True
        self.settings['wire_frame'] = False
        self.settings['line_width'] = 1.0

        self.set_properties(properties)



    def update_render_settings(self):
        if self.settings["double_sided"]:
            gl.glDisable(gl.GL_CULL_FACE)
        else:
            gl.glEnable(gl.GL_CULL_FACE)
    

        if self.settings["wire_frame"]:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        else:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
        
        gl.glLineWidth(self.settings["line_width"])