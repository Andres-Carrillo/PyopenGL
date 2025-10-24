from core.geometry.geometry import Geometry

class LineSegment(Geometry):
    def __init__(self, start=(0, 0, 0), end=(1, 0, 0), color_start=(1, 1, 1), color_end=(1, 1, 1)):
        super().__init__()
        positions = [list(start), list(end)]
        colors = [list(color_start), list(color_end)]
        normals = [[0, 0, 1], [0, 0, 1]]  # Facing Z+ by default
        uvs = [[0, 0], [1, 0]]

        self.add_attribute("vertex_position", positions, "vec3")
        self.add_attribute("vertex_color", colors, "vec3")
        self.add_attribute("vertex_uv", uvs, "vec2")
        self.add_attribute("vertex_normal", normals, "vec3")
        self.add_attribute("face_normal", normals, "vec3")
        self.count_vertices()