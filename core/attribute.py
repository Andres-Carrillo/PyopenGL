import OpenGL as gl
import numpy as np


class Attribute:
    def __init__(self,datatype,data):
        self.datatype = datatype
        self.data = data

        self.bufferRef = gl.glGenBuffers(1)

        self.uploadData()

    # upload data to GPU
    # this method should be called after the buffer is bound
    # in the OpenGL context
    def uploadData(self):
        data = np.array(self.data).astype(np.float32)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER,data.ravel(),gl.GL_STATIC_DRAW)

    #associate the buffer with the shader program
    def associatVariable(self,program_ref:int,variable_name:str) -> None:
        # create a reference to a variable with the given name
        variable_ref = gl.glGetAttribLocation(program_ref,variable_name)

        # check that the variable is valid
        if variable_ref == -1:
            raise RuntimeError(f"Variable {variable_name} not found in shader program")
        
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER,self.bufferRef)

        if self.dataType == "int":
            gl.glVertexAttribIPointer(variable_ref,1,gl.GL_INT,0,0)
        elif self.dataType == "float":
            gl.glVertexAttribPointer(variable_ref,1,gl.GL_FLOAT,gl.GL_FALSE,0,0)
        elif self.dataType == "vec2":
            gl.glVertexAttribPointer(variable_ref,2,gl.GL_FLOAT,gl.GL_FALSE,0,0)
        elif self.dataType == "vec3":
            gl.glVertexAttribPointer(variable_ref,3,gl.GL_FLOAT,gl.GL_FALSE,0,0)
        elif self.dataType == "vec4":
            gl.glVertexAttribPointer(variable_ref,4,gl.GL_FLOAT,gl.GL_FALSE,0,0)
        else:
            raise RuntimeError(f"Unknown data type {self.dataType}")
        
        # enable the variable
        gl.glEnableVertexAttribArray(variable_ref)