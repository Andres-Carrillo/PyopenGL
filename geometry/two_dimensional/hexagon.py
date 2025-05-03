from geometry.two_dimensional import Polygon

class Hexagon(Polygon):
    def __init__(self,raduis:float = 1) -> None:
        super().__init__(raduis, 6)
    