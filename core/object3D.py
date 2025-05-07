from core.matrix import Matrix
import numpy as np

class Object3D(object):
    """"Base for 3d Objects"""
    def __init__(self,parent=None):
        self.matrix = Matrix.mat4_identity()
        self.parent = parent
        self.children = []

    def add(self,child:'Object3D') -> None:
        self.children.append(child)
        child.parent = self

    def remove(self,child:'Object3D') -> None:
        self.children.remove(child)
        child.parent = None

    @property
    def global_matrix(self):
        """
        Calculate the transformation of this Object3D
        relative to the root Object3D of the scene graph
        """
        if self.parent is None:
            return self.matrix
        else:
            return self.parent.global_matrix @ self.matrix

    @property
    def global_position(self):
        """ Return the global or world position of the object """
        return [self.global_matrix.item((0, 3)),
                self.global_matrix.item((1, 3)),
                self.global_matrix.item((2, 3))]


    def get_world_matrix(self):
        if self.parent is not None:
            return self.parent.get_world_matrix() @ self.matrix
        else:
            return self.matrix
        
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
            self.matrix = self.matrix @ transfor_mat
        else:
            self.matrix = transfor_mat @ self.matrix


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
        return [self.matrix[0][3],self.matrix[1][3],self.matrix[2][3]]
    
    def get_global_pos(self):
        global_matrix = self.get_world_matrix()

        return [global_matrix[0][3],global_matrix[1][3],global_matrix[2][3]]

    def set_pos(self,pos:np.ndarray)->None:
        self.matrix[0][3] = pos[0]
        self.matrix[1][3] = pos[1]
        self.matrix[2][3] = pos[2]


    def look_at(self,target:np.ndarray) -> None:
        self.matrix = Matrix.make_look_at(self.global_position,target)
    
    def get_rotation(self) -> np.ndarray:
        return np.array([self.matrix[0][0:3],
                         self.matrix[1][0:3],
                         self.matrix[2][0:3]])
    
    def get_direction(self) -> list:
        forward = np.array([0,0,-1])
        return list(self.get_rotation() @ forward)
    

    def set_direction(self,direction:np.ndarray)-> None:
        position = self.get_pos()
        
        target = [position[0] + direction[0],
                 position[1] + direction[1],
                 position[2] + direction[2]]
        
        self.look_at(target)

        




