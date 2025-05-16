from core.object3D import Object3D
from meshes.mesh import Mesh
import numpy as np

class Scene(Object3D):
    """"Scene class meant to be the root of the scene graph"""
    def __init__(self):
        super().__init__()


    def pick_object(self, mouse_position, camera, width, height):

        x_normalized = (2.0*mouse_position[0]) / width - 1.0
        y_normalized = 1.0 - (2.0*mouse_position[1]) / height
        z = 1.0
        # Create a ray in normalized device coordinates
        ray_nds = [x_normalized, y_normalized, z]
        # Convert to world coordinates
        ray_clip = [ray_nds[0], ray_nds[1], -1.0, 1.0]
        ray_eye = np.linalg.inv(camera.projection_matrix)  @ ray_clip
        ray_eye = [ray_eye[0], ray_eye[1], -1.0, 0.0]
        ray_wor = np.linalg.inv(camera.view_matrix) @ ray_eye
        notmalized_ray = [ray_wor[0], ray_wor[1], ray_wor[2]]
        # Normalize the ray
        length = (notmalized_ray[0]**2 + notmalized_ray[1]**2 + notmalized_ray[2]**2)**0.5
        notmalized_ray = [notmalized_ray[0]/length, notmalized_ray[1]/length, notmalized_ray[2]/length]
        # Now we have a ray in world coordinates
        # print(f"Ray in world coordinates: {notmalized_ray}")
        # descendant_list = self.descendant_list
        # mesh_filter = lambda x: isinstance(x, Mesh)
        # mesh_list = list(filter(mesh_filter, descendant_list))

        # for mesh in mesh_list:
        #     if not mesh.visible:
        #         continue
        #     # Check if the mouse position is within the bounds of the mesh
        #     # This is a placeholder for the actual picking logic
        #     # You would typically use ray casting or similar techniques to determine if the mesh is under the mouse
        #     # For now, we will just print the mesh name
        #     print(f"Picking object: {mesh.name} at mouse position: {mouse_position}")
        # """ Pick an object in the scene using the mouse position and camera """


        