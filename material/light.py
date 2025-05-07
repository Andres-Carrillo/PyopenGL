from material.material import Material

class LightMaterial(Material):
    def __init__(self,number_of_lights:int = 1,vertex_shader_code:str = "",fragment_shader_code:str = "") -> None:
        number_of_lights = number_of_lights    

        super().__init__(vertex_shader_code,fragment_shader_code)

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
        code = "\n\t\t//list of lights\n"

        for i in range(number_of_lights):
            code += f"\t\tuniform Light light_{i};\n"


        code += "\n"

        print("generate light uniforms for shader")
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

        code = "\n\t\t//calculate the effect of all the lights in the scene\n"
        for i in range(number_of_lights):
            code += f"\t\tlight += calculate_light(light_{i}, position, normal);\n"


        code += "\n"

        print("generate light list sum")
        return code
    


