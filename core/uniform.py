import OpenGL.GL as gl
import numpy as np

class Uniform(object):

    def __init__(self,data_type,data):
        self.data_type = data_type
        self.data = data

        self.var_ref = None

    
    def locateVariable(self,program_ref,var_name):
        self.var_ref = gl.glGetUniformLocation(program_ref,var_name)

        if self.var_ref == -1:
            raise RuntimeError(f"Could not locate uniform variable {var_name}")
        
    def uploadData(self):
            
        if self.var_ref == -1:
            raise RuntimeError(f"Variablw was not correctly located.")
        
        if self.var_ref is None:
            raise RuntimeError(f"Need to link variable to program.")
            
        if self.data_type == "int":
                gl.glUniform1i(self.var_ref,self.data)
        elif self.data_type == "bool":
            gl.glUniform1i(self.var_ref,self.data)
        elif self.data_type == "float":
            gl.glUniform1f(self.var_ref,self.data)
        elif self.data_type == "vec2":
            gl.glUniform2f(self.var_ref,self.data[0],self.data[1])
        elif self.data_type == "vec3":
            gl.glUniform3f(self.var_ref,self.data[0],self.data[1],self.data[2])
        elif self.data_type == "vec4":
            gl.glUniform4f(self.var_ref,self.data[0],self.data[1],self.data[2],self.data[3])
        elif self.data_type == "mat4":
            gl.glUniformMatrix4fv(self.var_ref, 1, gl.GL_TRUE, np.array(self.data, dtype=np.float32))
        elif self.data_type == "sampler2D":
            # split the data into 2 parts the texture object and the texture unit reference
            texture_obj_ref,texture_unit_ref = self.data

            # activate the texture unit
            gl.glActiveTexture(gl.GL_TEXTURE0 + texture_unit_ref)   

            #associate the texture object with the texture unit
            gl.glBindTexture(gl.GL_TEXTURE_2D,texture_obj_ref)

            # upload texture  unit number 0-15 to the uniform variable in the shader
            gl.glUniform1i(self.var_ref,texture_unit_ref)

        else:
                raise RuntimeError(f"Unsupported data type {self.data_type}")
