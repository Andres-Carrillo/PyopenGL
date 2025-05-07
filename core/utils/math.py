import numpy as np

class Math:
 
        @staticmethod
        def clamp(value, min_value, max_value):
            """Clamp a value between a minimum and maximum value."""
            return max(min(value, max_value), min_value)
    
        @staticmethod
        def lerp(start, end, t):
            """Linearly interpolate between two values."""
            return start + (end - start) * t
        

        @staticmethod
        def calclulate_normal(p0, p1, p2):
            """
            Calculate the normal vector of a triangle defined by three points.
            The normal vector is calculated using the cross product of two edges of the triangle.
            """
            v1 = np.array(p1) - np.array(p0)
            v2 = np.array(p2) - np.array(p0)
            orthogonal_vector = np.cross(v1, v2)
            norm = np.linalg.norm(orthogonal_vector)

            # protect against division by zero
            # if the normal vector is too small, return a default value
            normal_vector = orthogonal_vector / norm if norm > 1e-6 else np.array(p0) / np.linalg.norm(p0)

            return normal_vector