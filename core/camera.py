from core.object3D import Object3D
from core.matrix import Matrix
from numpy.linalg import inv


class Camera(Object3D):
    def __init__(self,angle_of_view:float = 60.0, aspect:float=1.0, near:float = 0.1, far:float =1000):
        super().__init__()
        self.angle_of_view = angle_of_view
        self.aspect = aspect
        self.near = near
        self.far = far
        self.projection_matrix = Matrix.mat4_perspective(angle_of_view,aspect,near,far)
        self.view_matrix = Matrix.mat4_identity()

    def update_view_matrix(self):
        """Update the view matrix based on the camera's position and orientation"""
        self.view_matrix = inv(self.get_world_matrix())