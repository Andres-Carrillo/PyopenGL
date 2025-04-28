from core.matrix import Matrix
import numpy as np

class Object3D(object):
    """"Base for 3d Objects"""
    def __init__(self,parent=None):
        self.transform = Matrix.mat4_identity()
        self.parent = parent
        self.children = []

    def add(self,child:'Object3D') -> None:
        self.children.append(child)
        child.parent = self

    def remove(self,child:'Object3D') -> None:
        self.children.remove(child)
        child.parent = None

    def get_world_matrix(self):
        if self.parent is not None:
            return self.parent.get_world_matrix() @ self.transform
        else:
            return self.transform
        
    def get_children(self):
        kids = []
        nodes = [self]

        # BFS to get all children
        # This is a simple BFS implementation
        # that uses a queue to traverse the tree
        # and collect all nodes. Can be optimized 
        while len(nodes) > 0:
            node = nodes.pop(0)
            kids.append(node)
            nodes = node.children + nodes

        return kids


    def apply_transformation(self,transfor_mat:Matrix,local=True) -> None:

        if local:
            self.transform = self.transform @ transfor_mat
        else:
            self.transform = transfor_mat @ self.transform


    def translate(self,x:float,y:float,z:float,local=True) -> None:
        translation_matrix = Matrix.mat4_translation(x,y,z)
        self.apply_transformation(translation_matrix,local)

    def rotate_z(self,angle:float,local=True) -> None:
        rotation_matrix = Matrix.mat4_rotate_z(angle)
        self.apply_transformation(rotation_matrix,local)

    def rotate_x(self,angle:float,local=True) -> None:
        rotation_matrix = Matrix.mat4_rotate_x(angle)
        self.apply_transformation(rotation_matrix,local)

    def rotate_y(self,angle:float,local=True) -> None:
        rotation_matrix = Matrix.mat4_rotate_y(angle)
        self.apply_transformation(rotation_matrix,local)

    def scale(self,scale_value:float,local=True) -> None:
        scaling_matrix = Matrix.mat4_scale_uniform(scale_value)
        self.apply_transformation(scaling_matrix,local)

    def scale(self,x:float,y:float,z:float,local=True) -> None:
        scaling_matrix = Matrix.mat4_scale(x,y,z)
        self.apply_transformation(scaling_matrix,local)

    def get_pos(self):
        return [self.transform[0][3],self.transform[1][3],self.transform[2][3]]
    
    def get_global_pos(self):
        global_transform = self.get_world_matrix()

        return [global_transform[0][3],global_transform[1][3],global_transform[2][3]]

    def set_pos(self,pos:np.ndarray)->None:
        self.transform[0][3] = pos[0]
        self.transform[1][3] = pos[1]
        self.transform[2][3] = pos[2]
    


