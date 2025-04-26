from geometry.parametric import Parametric
from math import pi, sin, cos

class Ellipsoid(Parametric):
    def __init__(self,width:float = 1.0,height:float = 1.0,depth:float = 1.0,seg_radius:float= 32.0,seg_height:float= 16) -> None:
        
        def parametric_equation(u:float,v:float) -> tuple[float,float,float]:
            x = (width/2) * sin(u) * cos(v)
            y = (height/2) * sin(v)
            z = (depth/2) * cos(u) * cos(v)

            return (x,y,z)

        super().__init__(0,2*pi,seg_radius,-pi/2,pi/2,seg_height,parametric_equation)


        