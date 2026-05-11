from engine.ecs.components.types import COMPTYPE
import numpy as np
from numpy.linalg import inv
from engine.utils.matrix import Matrix

class CameraSystem:
    def __init__(self,window_width:int,window_height:int):
        self.window_width = window_width
        self.window_height = window_height

    def on_resize(self,width:int,height:int) -> None:
        self.window_width = width
        self.window_height = height

    def update(self,entities:list,dt:float) -> None:
        for entity in entities:
            if not entity.has_component(COMPTYPE.CAMERA):
                continue

            cam = entity.get_component(COMPTYPE.CAMERA)

            aspect = self.window_width / self.window_height

            if cam.aspect_ratio != aspect:
                cam.aspect_ratio = aspect
                cam.projection_matrix = Matrix.mat4_perspective(
                    cam.angle_of_view, aspect, cam.near, cam.far
                )

            cam.view_matrix = inv(entity.global_matrix)


