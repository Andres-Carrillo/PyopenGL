from geometry.geometry import Geometry


class BoxGeometry(Geometry):
    def __init__(self, width: float, height: float, depth: float) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.depth = depth
        self._create_box()

    def _create_box(self) -> None:
        p0 = [-self.width/2, -self.height/2, -self.depth/2]
        p1 = [self.width/2, -self.height/2, -self.depth/2]
        p2 = [-self.width/2,self.height/2.-self.depth/2]
        p3 = [self.width/2, self.height/2, -self.depth/2]
        p4 = [-self.width/2,-self.height/2, self.depth/2]
        p5 = [self.width/2,-self.height/2, self.depth/2]
        p6 = [-self.width/2, self.height/2, self.depth/2]
        p7 = [self.width/2, self.height/2, self.depth/2]


        # define default colors:
        c1 = [1,0.5,0.5]
        c2 = [0.5,0,0]
        c3 = [0.5,1,0.5]
        c4 = [0,0.5,0]
        c5 = [0.5,0.5,1]
        c6 = [0,0,0.5]


        position_orders = [p5,p1,p3, p5,p3,p7,
                           p0,p4,p6, p0,p6,p2,
                           p6,p7,p3, p6,p3,p2,
                           p0,p1,p5, p0,p5,p4,
                           p4,p5,p7, p4,p7,p6,
                           p1,p0,p2, p1,p2,p3]
        
        color_data = [c1]*6 + [c2]*6 + [c3]*6 + [c4]*6 + [c5]*6 + [c6]*6

        self.addAttribute("vertex_position", position_orders, "vec3")
        self.addAttribute("vertex_color", color_data, "vec3")
        self.countVertices()

