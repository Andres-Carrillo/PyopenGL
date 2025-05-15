from material.basic.material import Material

class LightMaterial(Material):
    def __init__(self,number_of_lights:int = 0,vertex_shader_code:str = "",fragment_shader_code:str = "") -> None:   

        super().__init__(vertex_shader_code,fragment_shader_code)

        if number_of_lights < 1:
            self.add_uniform("using_lights", False, "bool")
        else:
            self.add_uniform("using_lights", True, "bool")
            # initialize the light uniforms
            # this will be used to store the lights within the shader
            for i in range((number_of_lights)):
                self.add_uniform(f"light_{i}",None,"Light")

        


    # Static method to generate the glsl code for the light uniforms
    @staticmethod
    def generate_light_uniform_list(number_of_lights:int = 1) -> str:
        """
        Generates the light uniforms for the shader
        :return: str
        """
        code = "\n   \t\t\t\t// Generated list of lights:\n"

        for i in range(number_of_lights):
            code += f"   \t\t\t\tuniform Light light_{i};\n"



        return code
    
    # Static method to generate the glsl code for summing the effect of all the lights
    # in the scene
    @staticmethod
    def generate_light_sum(number_of_lights:int = 1) -> str:
        """"
            For calculating the effect of all the lights in the scene.
            This allows the user to add as many lights as they want
            and the shader will handle the calculations.
            :return: str
        """

        code = "\n\t\t\t\t\t//calculate the effect of all the lights in the scene\n"
        for i in range(number_of_lights):
            code += f"\t\t\t\t\tlight += calculate_light(light_{i}, position, calculated_normal);\n"


        code += "\n"
        return code
    


