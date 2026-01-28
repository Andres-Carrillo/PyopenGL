import numpy as np


class Vector(object):

    @staticmethod
    def vec3(x:float, y:float, z:float)->np.ndarray:
        return np.array([x,y,z]).astype(float)
    
    @staticmethod
    def vec4(x:float, y:float, z:float, w:float)->np.ndarray:
        return np.array([x,y,z,w]).astype(float)
    

    @staticmethod
    def normalize(v:np.ndarray)->np.ndarray:
        norm = np.linalg.norm(v)
        if norm == 0: 
           return v
        return v / norm
    
    @staticmethod
    def direction(from_point:np.ndarray, to_point:np.ndarray)->np.ndarray:
        dir_vector = to_point - from_point
        return Vector.normalize(dir_vector)
    

    @staticmethod
    def magnitude(v:np.ndarray)->float:
        return np.linalg.norm(v)
    

    @staticmethod
    def distance(point1:np.ndarray, point2:np.ndarray)->float:
        return np.linalg.norm(point2 - point1)
    


    @staticmethod
    def lerp(start:np.ndarray, end:np.ndarray, t:float)->np.ndarray:
        """Linearly interpolate between two vectors."""
        return start + (end - start) * t