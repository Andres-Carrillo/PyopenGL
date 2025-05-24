from core.object3D import Object3D
from meshes.mesh import Mesh
import numpy as np
from tools.grid import GridTool
from core.utils.math import Math
from tools.directional_light_tool import DirectionalLightTool


class Scene(Object3D):
    """"Scene class meant to be the root of the scene graph"""
    def __init__(self):
        super().__init__()


    def pick_object(self, mouse_position, camera, width, height):

        normalized_ray = Math.ray_cast(mouse_position, camera, width, height)    
        # Now we have a ray in world coordinates
        # print(f"Ray in world coordinates: {normalized_ray}")
        descendant_list = self.descendant_list
        mesh_filter = lambda x: isinstance(x, Mesh)
        mesh_list = list(filter(mesh_filter, descendant_list))

        for mesh in mesh_list:
            
            if not mesh.visible or isinstance(mesh,GridTool):
                # directional tool is a discendant of grid tool so this check is needed
                if not isinstance(mesh,DirectionalLightTool) :
                    continue
                
            
            
            if mesh.geometry.intersection_test(normalized_ray,camera.global_position,mesh.global_matrix):
                return mesh
            
        return None

           
            
         

            

        