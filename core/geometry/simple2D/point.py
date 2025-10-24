from core.geometry.geometry import Geometry

class PointGeometry(Geometry):
    def __init__(self, position=(0,0,0), color=(1,1,1), uv=(0.5,0.5), normal=(0,0,1)):
        super().__init__()
        self.add_attribute("vertex_position", [list(position)], "vec3")
        self.add_attribute("vertex_color", [list(color)], "vec3")
        self.add_attribute("vertex_uv", [list(uv)], "vec2")
        self.add_attribute("vertex_normal", [list(normal)], "vec3")
        self.add_attribute("face_normal", [list(normal)], "vec3")
        self.count_vertices()