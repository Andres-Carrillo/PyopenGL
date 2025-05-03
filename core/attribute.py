from OpenGL.GL import *
import glfw
import numpy as np

"""
This class is used to create and manage OpenGL vertex buffer objects (VBOs) for
storing vertex attributes. It handles the creation of the buffer, uploading data
to the GPU, and associating the buffer with a shader program."""

class Attribute:
    def __init__(self,datatype:str,data:object):
        self.data_type = datatype
        self.data = data

        self.bufferRef = glGenBuffers(1)

        self.uploadData()

    """
        This method is used to upload the data to the GPU. It creates a buffer object
        and uploads the data to the GPU. The data is converted to a numpy array of
        the appropriate data type before being uploaded. The buffer is created with
        the GL_STATIC_DRAW usage hint, which indicates that the data will not be changed
        frequently. 
            Raises:
                RuntimeError: If there is an error uploading the data to the GPU.
    """
    def uploadData(self):
        data = np.array(self.data,dtype=np.float32)
        glBindBuffer(GL_ARRAY_BUFFER,self.bufferRef)

        # allocate memory for the buffer
        glBufferData(GL_ARRAY_BUFFER,data.nbytes,data,GL_STATIC_DRAW)
        # check for errors
        error = glGetError()
        if error != GL_NO_ERROR:
            raise RuntimeError(f"Error uploading data to GPU: {error}")
        
    """
        This method is used to associate the buffer with a shader program. It creates
        a reference to a variable with the given name in the shader program and binds
        the buffer to the program. The method checks that the variable is valid and
        not -1 before associating it with the buffer. It also sets the appropriate
        pointer for the variable based on its data type. The method raises an exception
        if the data type is unknown.
            Args:
                program_ref (int): The reference to the shader program.
                variable_name (str): The name of the variable in the shader program.
            Raises:
             RuntimeError: If the variable is not valid or if the data type is unknown.
    """
    def associateVariable(self,program_ref:int,variable_name:str) -> None:
        # create a reference to a variable with the given name
        self.variable_ref = glGetAttribLocation(program_ref,variable_name)

        # check that the variable is valid is not skip associating
        if self.variable_ref == -1:
            return
        
        glBindBuffer(GL_ARRAY_BUFFER,self.bufferRef)

        if self.data_type == "int":
            glVertexAttribIPointer(self.variable_ref,1,GL_INT,False,0,None)
        elif self.data_type == "float":
            glVertexAttribPointer(self.variable_ref,1,GL_FLOAT,False,0,None)
        elif self.data_type == "vec2":
            glVertexAttribPointer(self.variable_ref,2,GL_FLOAT,False,0,None)
        elif self.data_type == "vec3":
            glVertexAttribPointer(self.variable_ref,3,GL_FLOAT,False,0,None)
        elif self.data_type == "vec4":
            glVertexAttribPointer(self.variable_ref,4,GL_FLOAT,False,0,None)
        else:
            raise RuntimeError(f"Unknown data type {self.data_type}")
        
        # enable the variable
        glEnableVertexAttribArray(self.variable_ref)