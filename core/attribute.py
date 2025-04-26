from OpenGL.GL import *
import glfw
import numpy as np


class Attribute:
    def __init__(self,datatype:str,data:object):
        self.data_type = datatype
        self.data = data

        self.bufferRef = glGenBuffers(1)

        self.uploadData()

    # upload data to GPU
    # this method should be called after the buffer is bound
    # in the OpenGL context
    def uploadData(self):
        data = np.array(self.data,dtype=np.float32)
        glBindBuffer(GL_ARRAY_BUFFER,self.bufferRef)

        # allocate memory for the buffer
        glBufferData(GL_ARRAY_BUFFER,data.nbytes,data,GL_STATIC_DRAW)
        # check for errors
        error = glGetError()
        if error != GL_NO_ERROR:
            raise RuntimeError(f"Error uploading data to GPU: {error}")

    #associate the buffer with the shader program
    def associateVariable(self,program_ref:int,variable_name:str) -> None:
        # create a reference to a variable with the given name
        variable_ref = glGetAttribLocation(program_ref,variable_name)

        # check that the variable is valid
        if variable_ref == -1:
            raise RuntimeError(f"Variable {variable_name} not found in shader program")
        
        glBindBuffer(GL_ARRAY_BUFFER,self.bufferRef)

        if self.data_type == "int":
            glVertexAttribIPointer(variable_ref,1,GL_INT,False,0,None)
        elif self.data_type == "float":
            glVertexAttribPointer(variable_ref,1,GL_FLOAT,False,0,None)
        elif self.data_type == "vec2":
            glVertexAttribPointer(variable_ref,2,GL_FLOAT,False,0,None)
        elif self.data_type == "vec3":
            glVertexAttribPointer(variable_ref,3,GL_FLOAT,False,0,None)
        elif self.data_type == "vec4":
            glVertexAttribPointer(variable_ref,4,GL_FLOAT,False,0,None)
        else:
            raise RuntimeError(f"Unknown data type {self.data_type}")
        
        # enable the variable
        glEnableVertexAttribArray(variable_ref)