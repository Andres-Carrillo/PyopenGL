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
    def InitializeProgram(vertex_shader_code:str, fragment_shader_code:str) -> int:
        vertex_shader_ref = GlUtils.InitializeShader(vertex_shader_code, gl.GL_VERTEX_SHADER)
        fragment_shader_ref = GlUtils.InitializeShader(fragment_shader_code, gl.GL_FRAGMENT_SHADER)
        
        # create program
        program = gl.glCreateProgram()

        #attach shaders to program
        gl.glAttachShader(program,vertex_shader_ref)
        gl.glAttachShader(program,fragment_shader_ref)

        # link program
        gl.glLinkProgram(program)

        # check for link errors
        link_status = gl.glGetProgramiv(program, gl.GL_LINK_STATUS)

        if not link_status:
            info_log = gl.glGetProgramInfoLog(program)
            gl.glDeleteProgram(program)
            raise RuntimeError(f"Program linking failed: {info_log.decode()}")
        

        return program

     
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
   
    @staticmethod
    def printSystemInfo():
        print("OpenGL Version:", gl.glGetString(gl.GL_VERSION).decode())
        print("GLSL Version:", gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION).decode())
        print("Vendor:", gl.glGetString(gl.GL_VENDOR).decode())
        print("Renderer:", gl.glGetString(gl.GL_RENDERER).decode())
        print("Extensions:", gl.glGetString(gl.GL_EXTENSIONS).decode())
