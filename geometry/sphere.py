from geometry.ellipsoid import Ellipsoid
from math import pi, sin, cos

class Sphere(Ellipsoid):

    def __init__(self,radius:float = 1.0,seg_radius:float=32.0,seg_height:float=16) -> None:
        
        def parametric_equation(u:float,v:float) -> tuple[float,float,float]:
            x = radius * sin(u) * cos(v)
            y = radius * sin(v)
            z = radius * cos(u) * cos(v)

            return (x,y,z)

        super().__init__(radius,radius,radius,seg_radius,seg_height,parametric_equation)