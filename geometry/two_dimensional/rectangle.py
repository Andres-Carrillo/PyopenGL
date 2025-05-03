from geometry.geometry import Geometry

class Rectangle(Geometry):
    def __init__(self, width: float = 1.0, height: float = 1.0,position:list = [0,0],alignment:list = [0.5,0.5]) -> None:
        super().__init__()
        self.width = width
        self.height = height

        self._create_rectangle(position=position,alignment=alignment,width=width,height=height)


    def _create_rectangle(self,position,alignment,width,height) -> None:
        x, y = position
        a, b = alignment
        p0 = [x + (-a) * width, y + (-b) * height, 0]
        p1 = [x + (1 - a) * width, y + (-b) * height, 0]
        p2 = [x + (-a) * width, y + (1 - b) * height, 0]
        p3 = [x + (1 - a) * width, y + (1 - b) * height, 0]

        c0, c1, c2, c3 = [1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1]
        t0, t1, t2, t3 = [0, 0], [1, 0], [0, 1], [1, 1]

        # define the vertices of the rectangle in counter clockwise order:
        # drawing using triangles so we need to define 2 triangles grouped in 3s for 6 total points, two of which are shared
        # so in total we have 4 points 
        position_data = [p0, p1, p3, p0, p3, p2]
        color_data = [c0, c1, c3, c0, c3, c2]
        # color_data = [c0, c0, c0, c1, c1, c1]
        uv_data = [t0, t1, t3, t0, t3, t2]

        self.addAttribute("vertex_position", position_data, "vec3")
        self.addAttribute("vertex_color", color_data, "vec3")
        self.addAttribute("vertex_uv", uv_data, "vec2")
        self.countVertices()


