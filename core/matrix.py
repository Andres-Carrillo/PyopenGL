import numpy as np
from math import sin,cos,tan,pi

class Matrix(object):

    # Construct a 2D matrix of dimension size x size
    @staticmethod
    def identity(size:int)->np.ndarray:
        return np.identity(size,dtype=np.float32)

    # Construct 4x4 identity matrix for basis of 3D Transformations
    @staticmethod
    def mat4_identity()->np.ndarray:
        return Matrix.identity(4)
    
    # Construct 4x4 translation matrix for 3D Transformations
    @staticmethod
    def mat4_translation(x,y,z)->np.ndarray:
        mat = Matrix.mat4_identity()
        
        mat[0][3] = x
        mat[1][3] = y
        mat[2][3] = z

        return mat
    
    # Construct 4x4 rotation matrix for 3D rotations about the x axis
    @staticmethod
    def mat4_rotate_x(angle:float)->np.ndarray:
        mat = Matrix.mat4_identity()
        
        c = cos(angle)
        s = sin(angle)

        mat[1][1] = c
        mat[1][2] = -s
        mat[2][1] = s
        mat[2][2] = c

        return mat
    
    @staticmethod
    def mat4_rotate_y(angle:float)->np.ndarray:
        mat = Matrix.mat4_identity()
        
        c = cos(angle)
        s = sin(angle)

        mat[0][0] = c
        mat[0][2] = s
        mat[2][0] = -s
        mat[2][2] = c

        return mat
    

    @staticmethod
    def mat4_rotate_z(angle:float)->np.ndarray:
        mat = Matrix.mat4_identity()
        
        c = cos(angle)
        s = sin(angle)

        mat[0][0] = c
        mat[0][1] = -s
        mat[1][0] = s
        mat[1][1] = c

        return mat
    
    # construct 4x4 scaling matrix for 3D scaling
    @staticmethod
    def mat4_scale_uniform(scale_val:float)->np.ndarray:
        mat = Matrix.mat4_identity()
        
        mat[0][0] = scale_val
        mat[1][1] = scale_val
        mat[2][2] = scale_val

        return mat
    
    def mat4_scale(x:float,y:float,z:float)->np.ndarray:
        mat = Matrix.mat4_identity()
        
        mat[0][0] = x
        mat[1][1] = y
        mat[2][2] = z

        return mat
    

    
    # construct 4x4 perspective projection matrix
    @staticmethod
    def mat4_perspective(angle_of_view:float = 60.0, aspect:float=1.0, near:float = 0.1, far:float =1000)->np.ndarray:
        mat = Matrix.mat4_identity()
        a = angle_of_view * pi / 180.0
        d = 1.0 / tan(a/2.0)
        r = aspect
        b = (far + near) / (near - far)
        c = (2*far*near) / (near - far)

        mat[0][0] = d/r
        mat[1][1] = d
        mat[2][2] = b
        mat[3][2] = c
        mat[2][3] = -1.0
        mat[3][3] = 0.0

        return mat
    
