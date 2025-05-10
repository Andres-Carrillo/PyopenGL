import numpy as np
from math import sin,cos,tan,pi
# from pyglm import glm ## want to use glm but not necessarily right now as performance is currently not an issue
class Matrix(object):

    # Construct a 2D matrix of dimension size x size
    @staticmethod
    def identity(size:int)->np.ndarray:
        return np.array(
            [[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, 1]]
        ).astype(float)
    
    # Construct 4x4 identity matrix for basis of 3D Transformations
    @staticmethod
    def mat4_identity()->np.ndarray:
        return Matrix.identity(4)
    
    # Construct 4x4 translation matrix for 3D Transformations
    @staticmethod
    def mat4_translation(x,y,z)->np.ndarray:
        return np.array(
                    [[1, 0, 0, x],
                    [0, 1, 0, y],
                    [0, 0, 1, z],
                    [0, 0, 0, 1]]
                ).astype(float)
    
    # Construct 4x4 rotation matrix for 3D rotations about the x axis
    @staticmethod
    def mat4_rotate_x(angle:float)->np.ndarray:
        c = cos(angle)
        s = sin(angle)
        return np.array(
            [[1,  0,  0,  0],
             [0,  c, -s,  0],
             [0,  s,  c,  0],
             [0,  0,  0,  1]]
        ).astype(float)
    
    @staticmethod
    def mat4_rotate_y(angle:float)->np.ndarray:
        c = cos(angle)
        s = sin(angle)
        return np.array(
            [[c,  0,  s,  0],
             [0,  1,  0,  0],
             [-s, 0,  c,  0],
             [0,  0,  0,  1]]
        ).astype(float)
    

    @staticmethod
    def mat4_rotate_z(angle:float)->np.ndarray:
        c = cos(angle)
        s = sin(angle)
        return np.array(
            [[c, -s,  0,  0],
             [s,  c,  0,  0],
             [0,  0,  1,  0],
             [0,  0,  0,  1]]
        ).astype(float)
    
    # construct 4x4 scaling matrix for 3D scaling
    @staticmethod
    def mat4_scale_uniform(scale_val:float)->np.ndarray:
        return np.array(
            [[scale_val, 0, 0, 0],
             [0, scale_val, 0, 0],
             [0, 0, scale_val, 0],
             [0, 0, 0, 1]]
        ).astype(float)
        
    @staticmethod
    def mat4_scale(x:float,y:float,z:float)->np.ndarray:
        mat = Matrix.mat4_identity()
        
        mat[0][0] = x
        mat[1][1] = y
        mat[2][2] = z

        return mat
    

    
    # construct 4x4 perspective projection matrix
    @staticmethod
    def mat4_perspective(angle_of_view:float = 60.0, aspect_ratio:float=1.0, near:float = 0.1, far:float =1000)->np.ndarray:
        a = angle_of_view * pi / 180.0
        d = 1.0 / tan(a / 2)
        b = (far + near) / (near - far)
        c = 2 * far * near / (near - far)
        return np.array(
            [[d / aspect_ratio, 0, 0, 0],
             [0, d, 0, 0],
             [0, 0, b, c],
             [0, 0, -1, 0]]
        ).astype(np.float32)
    
    @staticmethod
    def make_orthographic(left=-1, right=1, bottom=-1, top=1, near=-1, far=1):
        return np.array(
            [[2 / (right - left), 0, 0, -(right + left) / (right - left)],
             [0, 2 / (top - bottom), 0, -(top + bottom) / (top - bottom)],
             [0, 0, -2 / (far - near), -(far + near) / (far - near)],
             [0, 0, 0, 1]]
        ).astype(float)

    @staticmethod
    def make_look_at(position, target):
        world_up = [0, 1, 0]
        forward = np.subtract(target, position)
        right = np.cross(forward, world_up)
        # If forward and world_up vectors are parallel,
        # the right vector is zero.
        # Fix this by perturbing the world_up vector a bit
        if np.linalg.norm(right) < 1e-6:
            offset = np.array([0, 0, -1e-3])
            right = np.cross(forward, world_up + offset)
        up = np.cross(right, forward)
        # All vectors should have length 1
        forward = np.divide(forward, np.linalg.norm(forward))
        right = np.divide(right, np.linalg.norm(right))
        up = np.divide(up, np.linalg.norm(up))
        return np.array(
            [[right[0], up[0], -forward[0], position[0]],
             [right[1], up[1], -forward[1], position[1]],
             [right[2], up[2], -forward[2], position[2]],
             [0, 0, 0, 1]]
        ).astype(float)
    



