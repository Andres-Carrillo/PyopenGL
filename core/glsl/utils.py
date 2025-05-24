import enum

class ShaderType(enum.Enum):
    VERTEX = 0
    FRAGMENT = 1
    GEOMETRY = 2
    COMPUTE = 3
    TESSELLATION_CONTROL = 4
    TESSELLATION_EVALUATION = 5

    def __str__(self):
        return self.name.lower()

def edit_light_list(material:object,number_of_lights:int,shader:ShaderType = ShaderType.FRAGMENT) -> None:
        """
        Given a material and a number of lights,
        find the ##LIGHT_LIST##  tag in the shader code 
        and replace it with the light uniforms
        :return: str
        """
        light_list = ""
        code = material.vertex_shader if shader == ShaderType.VERTEX else material.fragment_shader
        start, end = find_tag(code,"##LIGHT_LIST##")
        
        #if the tag is not found, return False for debugging
        if start == -1 or end == -1:
            return False
        
        # generate the light uniforms
        for i in range(number_of_lights):
            light_list += f"   \t\t\t\tuniform Light light_{i};\n"

        # replace the tag with the light uniforms
        code = code[:start] + light_list + code[end:]

        print("the updated shader code is: ",code)

        # update the shader code
        if shader == ShaderType.VERTEX:
            material.vertex_shader = code
        else:
            material.fragment_shader = code

        # if the shader code is valid, return True
        return True


def find_tag(shader_code:str,tag:str) -> str:
    """
    Given a shader code and a tag,
    find the tag in the shader code 
    and return the code before and after the tag
    :return: str
    """
    # find the tag in the shader code
    start = shader_code.find(tag)
    end = shader_code.find(":",start) + 1

    # if the tag is not found, return None
    if start == -1 or end == -1:
        return None

    # return the code before and after the tag
    return start, end