from core.attribute import Attribute


class Geometry(object):
    def __init__(self):
        self.attributes = {}
        self.vertex_count = None

    
    def addAttribute(self, name:str, data:object,datatype:str):
        self.attributes[name] = Attribute(datatype,data)


    def countVertices(self):
        attribute = list(self.attributes.values())[0]
        self.vertex_count = len(attribute.data)