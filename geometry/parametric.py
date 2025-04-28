from geometry.geometry import Geometry

class Parametric(Geometry):
    """
    The Parametric class is a base class for creating parametric shapes.
    It inherits from the Geometry class and provides a method to generate
    vertices based on a parametric equation.
    """
    def __init__(self,u_start:float,u_end:float,u_resolution:float,
                 v_start:float,v_end:float,v_resolution:float,surface_functions:object) -> None:
        
        super().__init__()

        delta_u = (u_end - u_start) / u_resolution
        delta_v = (v_end - v_start) / v_resolution

        positions = []

        for u_index in range(int(u_resolution + 1)):
            v_array = []
            for v_index in range(int(v_resolution + 1)):
                u = u_start + u_index * delta_u
                v = v_start +  v_index * delta_v
                position = surface_functions(u, v)
                v_array.append(position)

            positions.append(v_array)

        position_data = []
        color_data = []

        c1 = [1,0,0]
        c2 = [0,1,1]
        c3 = [0,0,1]
        c4 = [0,1,1]
        c5 = [1,0,1]
        c6 = [1,1,0]

        for i_index in range(int(u_resolution)):
            for j_index in range(int(v_resolution)):
                # position data
                p_a = positions[i_index + 0][j_index + 0]
                p_b = positions[i_index + 1][j_index + 0]
                p_c = positions[i_index + 1][j_index + 1]
                p_d = positions[i_index + 0][j_index + 1]

                position_data += [p_a.copy(), p_b.copy(), p_c.copy(),
                                  p_a.copy(), p_c.copy(), p_d.copy()]
                # color data
                color_data += [c1, c2, c3,
                               c4, c5, c6]
        self.addAttribute("vertex_position", position_data, "vec3")
        # self.addAttribute("vertex_color", color_data, "vec3")
        self.countVertices()
