import OpenGL.GL as gl
from OpenGL.GL.shaders import compileProgram, compileShader

class GlUtils(object):

    @staticmethod
    def InitializeShader(code:str, shader_type:int) -> int:
        # add header to shader code
        shader_code = '#version 330 core' + code
        # create dummy shader
        shader = gl.glCreateShader(shader_type)

        # store shader code in shader
        gl.glShaderSource(shader, shader_code)
        # compile shader
        gl.glCompileShader(shader)

        # check for compile errors
        compile_status = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)
        if compile_status != gl.GL_TRUE:
            info_log = gl.glGetShaderInfoLog(shader)
            gl.glDeleteShader(shader)
            raise RuntimeError(f"Shader compilation failed: {info_log.decode()}")
        
        return shader
    
     
    @staticmethod
    def create_shader_module(filepath:str,module_type: int) -> int:
        source_code = ""

        with open(filepath, 'r') as file:
            source_code = file.readlines()

        return compileShader(source_code, module_type)

    @staticmethod
    def create_shader_program(vertex_filepath:str,fragment_filepath:str) ->int:
        vertex_module = GlUtils.create_shader_module(vertex_filepath,gl.GL_VERTEX_SHADER)
        fragment_module = GlUtils.create_shader_module(fragment_filepath,gl.GL_FRAGMENT_SHADER)
        
        shader_program = compileProgram(vertex_module, fragment_module)
        
        gl.glDeleteShader(vertex_module)
        gl.glDeleteShader(fragment_module)

        return shader_program
   