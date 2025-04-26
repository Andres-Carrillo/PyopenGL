from geometry.geometry import Geometry

class RectangleGeometry(Geometry):
    def __init__(self, width: float, height: float) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self._create_rectangle()


    def _create_rectangle(self) -> None:
        #Define 4 corners of the rectangle:
        bot_left = [-self.width/2, -self.height/2,0]
        bot_right = [self.width/2, -self.height/2,0]
        top_left = [-self.width/2, self.height/2,0]
        top_right = [self.width/2, self.height/2,0]

        #define default colors:
        color_1 = [1,1,1]
        color_2 = [1,0,0]
        color_3 = [0,1,0]
        color_4 = [0,0,1]

        # define the vertices of the rectangle in counter clockwise order:
        # drawing using triangles so we need to define 2 triangles grouped in 3s for 6 total points, two of which are shared
        # so in total we have 4 points 
        vertex_orders = [bot_left,bot_right,top_right, bot_left,top_right,top_left]
        colors = [color_1,color_2,color_4,color_1,color_4,color_3]

        self.addAttribute("vertex_position", vertex_orders, "vec3")
        self.addAttribute("vertex_color", colors, "vec3")
        self.countVertices()

