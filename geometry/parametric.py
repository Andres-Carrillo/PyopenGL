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
        texture_uvs = []
        texture_uv_data = []

        for u_index in range(int(u_resolution + 1)):
            v_array = []
            texture__uv_array = []
            for v_index in range(int(v_resolution + 1)):
                # generate the position of the vertex
                u = u_start + u_index * delta_u
                v = v_start +  v_index * delta_v
                position = surface_functions(u, v)
                v_array.append(position)

                # generate the texture coordinates
                texture_u = u_index/u_resolution
                texture_v = v_index/v_resolution
                texture__uv_array.append([texture_u, texture_v])

            positions.append(v_array)
            texture_uvs.append(texture__uv_array)

        position_data = []
        color_data = []
        # color data
        c1 = [1,0,0]
        c2 = [0,1,1]
        c3 = [0,0,1]
        c4 = [0,1,1]
        c5 = [1,0,1]
        c6 = [1,1,0]

        for i_index in range(int(u_resolution)):
            for j_index in range(int(v_resolution)):
                # The vertices in groups of each square
                p_a = positions[i_index + 0][j_index + 0]
                p_b = positions[i_index + 1][j_index + 0]
                p_c = positions[i_index + 1][j_index + 1]
                p_d = positions[i_index + 0][j_index + 1]

                # group the vertices in triangles to draw the square
                position_data += [p_a.copy(), p_b.copy(), p_c.copy(), # first triangle
                                  p_a.copy(), p_c.copy(), p_d.copy()] # second triangle
                # color data also in groups of each triangle
                color_data += [c1, c2, c3,
                               c4, c5, c6]
                
                # texture coordinates
                t_a = texture_uvs[i_index + 0][j_index + 0]
                t_b = texture_uvs[i_index + 1][j_index + 0]
                t_c = texture_uvs[i_index + 1][j_index + 1]
                t_d = texture_uvs[i_index + 0][j_index + 1]
                # group the texture coordinates in triangles 
                texture_uv_data += [t_a.copy(), t_b.copy(), t_c.copy(),
                                    t_a.copy(), t_c.copy(), t_d.copy()]
                

        self.addAttribute("vertex_position", position_data, "vec3")
        self.addAttribute("vertex_color", color_data, "vec3")
        self.addAttribute("vertex_uv", texture_uv_data, "vec2")
        self.countVertices()
