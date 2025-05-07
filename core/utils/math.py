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
            # Convert points to numpy arrays for easier calculations
            p0 = np.array(p0)
            p1 = np.array(p1)
            p2 = np.array(p2)

            # Calculate two edges of the triangle
            edge1 = p1 - p0
            edge2 = p2 - p0

            # Calculate the normal vector using the cross product
            normal_vector = np.cross(edge1, edge2)

            # Normalize the normal vector
            normal_vector /= np.linalg.norm(normal_vector)

            return normal_vector.tolist()