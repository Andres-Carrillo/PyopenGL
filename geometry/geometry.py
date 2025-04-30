from core.attribute import Attribute


class Geometry(object):
    def __init__(self):
        self.attributes = {}
        self.vertex_count = None

    
    def addAttribute(self, name:str, data:object,datatype:str):
        attribute = Attribute(datatype,data)
        self.attributes[name] = attribute
        
        if name == "vertex_position":
            self.vertex_count = len(data)

    def countVertices(self):
        attribute = list(self.attributes.values())[0]
        self.vertex_count = len(attribute.data)

    def get_vertex_count(self):
        if self.vertex_count is None:
            self.countVertices()
            
        return self.vertex_count


    def applyTransform(self,matrix,var_name:str = "vertex_position"):
        old_position = self.attributes[var_name].data
        new_position = []

        for prev_pos in old_position:
            new_pos = prev_pos.copy()

            new_pos.append(1)

            new_pos = matrix @ new_pos

            new_pos = list(new_pos[:3])

            new_position.append(new_pos)

        self.attributes[var_name].data = new_position
        self.attributes[var_name].uploadData()


    def merge(self,other_geometry):
        for var_name, attrib_obj in self.attributes.items():
            attrib_obj.data += other_geometry.attributes[var_name].data
            attrib_obj.uploadData()
        
        self.countVertices()
           