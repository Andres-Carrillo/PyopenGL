import OpenGL.GL as gl
from OpenGL.GL.shaders import compileProgram, compileShader
from PyQt5.QtGui import QOpenGLShaderProgram,QOpenGLShader

class GlUtils(object):
    
    IS_QT = False
    
    @staticmethod
    def InitializeShader(code:str, shader_type:int) -> int:
        # add header to shader code
        shader_code = '#version 330 core' + code

        # if shader_type is QOpenGLShader.ShaderTypeBit:
        if isinstance(shader_type, QOpenGLShader.ShaderTypeBit):
                    # create dummy shader
            shader = QOpenGLShader(shader_type)
            
            # store shader code in shader & check for compile errors
            if not shader.compileSourceCode(shader_code):
                raise RuntimeError(f"Shader compilation failed: {shader.log()}")
            
            return shader
        
        else:
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
       
        # handle the case where the shader is a QOpenGLShader
        if GlUtils.IS_QT:
            print("Using QOpenGLShader")
            vertex_shader_ref = GlUtils.InitializeShader(vertex_shader_code, QOpenGLShader.Vertex)
            fragment_shader_ref = GlUtils.InitializeShader(fragment_shader_code, QOpenGLShader.Fragment)
            # create program
            program = QOpenGLShaderProgram()
            
            # attach shaders to program
            if not program.addShader(vertex_shader_ref):
                raise RuntimeError(f"Vertex shader compilation failed: {program.log()}")
            
            if not program.addShader(fragment_shader_ref):
                raise RuntimeError(f"Fragment shader compilation failed: {program.log()}")
            
            # link program
            if not program.link():
                raise RuntimeError(f"Program linking failed: {program.log()}")
            
            # bind program
            program.bind()
            
            return program.programId()
        else:
            vertex_shader_ref = GlUtils.InitializeShader(vertex_shader_code, gl.GL_VERTEX_SHADER)
            fragment_shader_ref = GlUtils.InitializeShader(fragment_shader_code, gl.GL_FRAGMENT_SHADER)

            # check for shader compilation errors
            GlUtils.check_shader_compilation(vertex_shader_ref)
            GlUtils.check_shader_compilation(fragment_shader_ref)
            
            # create program
            program = gl.glCreateProgram()

            #attach shaders to program
            gl.glAttachShader(program,vertex_shader_ref)
            gl.glAttachShader(program,fragment_shader_ref)

            # link program
            gl.glLinkProgram(program)

            # check for link errors
            GlUtils.check_program_linking(program)
            
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

    @staticmethod
    def check_shader_compilation(shader_ref):
        status = gl.glGetShaderiv(shader_ref, gl.GL_COMPILE_STATUS)
        if status != gl.GL_TRUE:
            info_log = gl.glGetShaderInfoLog(shader_ref)
            raise RuntimeError(f"Shader compilation failed: {info_log.decode()}")
        

    @staticmethod
    def check_program_linking(program_ref):
        status = gl.glGetProgramiv(program_ref, gl.GL_LINK_STATUS)
        if status != gl.GL_TRUE:
            info_log = gl.glGetProgramInfoLog(program_ref)
            print("log: ",info_log)
            raise RuntimeError(f"Program linking failed: {info_log}")