from core.geometry.simple2D.polygon import Polygon

class Octagon(Polygon):
    def __init__(self, radius: float = 1) -> None:
        super().__init__(radius, 8)