from core.attribute import Attribute
import numpy as np

class Geometry(object):
    def __init__(self):
        self.attributes = {}
        self.vertex_count = None

    
    def add_attribute(self, name:str, data:object,datatype:str):
        attribute = Attribute(datatype,data)
        self.attributes[name] = attribute
        
        if name == "vertex_position":
            self.vertex_count = len(data)

    def count_vertices(self):
        attribute = list(self.attributes.values())[0]
        self.vertex_count = len(attribute.data)

    def get_vertex_count(self):
        if self.vertex_count is None:
            self.count_vertices()
            
        return self.vertex_count


    def apply_transform(self,matrix,var_name:str = "vertex_position"):
        rotational_matrix = np.array([matrix[0][0:3],
                                      matrix[1][0:3],
                                      matrix[2][0:3]])
        
        old_position = self.attributes[var_name].data
        old_vertex_normal_data = self.attributes["vertex_normal"].data
        old_face_normal_data = self.attributes["face_normal"].data
        new_position = []
        new_vertex_normal = []
        new_face_normal = []

        #apply the transformation to all the old positions
        for prev_pos in old_position:
            # get the position of the vertex
            new_pos = prev_pos.copy()
            # transform to vec4 for matrix multiplication
            new_pos.append(1)
            # apply the transformation
            new_pos = matrix @ new_pos
            # remove the last element to get back to vec3
            new_pos = list(new_pos[:3])
            # add the new position to the list
            new_position.append(new_pos)


        # apply transformation to the vertex normals
        for old_normal in old_vertex_normal_data:
            new_normal = old_normal.copy()
            new_normal = rotational_matrix @ new_normal
            new_vertex_normal.append(new_normal)
        

        # apply transformation to the face normals
        for old_normal in old_face_normal_data:
            new_normal = old_normal.copy()
            new_normal = rotational_matrix @ new_normal
            new_face_normal.append(new_normal)

        # update data and upload it
        self.attributes[var_name].data = new_position
        self.attributes["vertex_normal"].data = new_vertex_normal
        self.attributes["face_normal"].data = new_face_normal
        self.attributes[var_name].upload_data()


    def merge(self,other_geometry):
        for var_name, attrib_obj in self.attributes.items():
            attrib_obj.data += other_geometry.attributes[var_name].data
            attrib_obj.upload_data()
        
        self.count_ertices()
           