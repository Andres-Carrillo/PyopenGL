import enum

from core.entity import Components
from core.object3D import Object3D
from core.entity import Entity

class CollisionType(enum.IntFlag):
    NONE = 0
    SPHERE = 1
    BOX = 2




class ColliderComponent:
    def __init__(self, collision_type=CollisionType.NONE, data:dict=None):
        self.collision_type = collision_type
        
        if data is None:
            data = {}



class CollisionSystem:
    @staticmethod
    def check_collisions(entities:list):
        collidable = [e for e in entities if e.has_component(Components.COLLIDER)]

        collisions = []

        for i in range(len(collidable)):
            for j in range(i + 1, len(collidable)):
                ent_a = collidable[i]
                ent_b = collidable[j]
                collider_a = ent_a.get_component_data(Components.COLLIDER) # gets dictionary with collider info
                collider_b = ent_b.get_component_data(Components.COLLIDER) # gets dictionary with collider info

                if CollisionSystem.check_collision((ent_a, collider_a), (ent_b, collider_b)):
                    collisions.append((ent_a, ent_b))

        return collisions
    

    @staticmethod
    def reslove_collisions(collisions:list):
        for ent_a,ent_b in collisions:
            # simple resolution: just stop their movement
            physics_a = ent_a.get_component_data(Components.RIGIDBODY)
            physics_b = ent_b.get_component_data(Components.RIGIDBODY)
            if physics_a:
                physics_a.velocity = [0,0,0]
            if physics_b:
                physics_b.velocity = [0,0,0]
    

    @staticmethod
    def chcek_collision(entity_a_tuple, entity_b_tuple):
        entity_a, collider_a = entity_a_tuple
        entity_b, collider_b = entity_b_tuple

        # Simple example for sphere-sphere collision
        if collider_a.collision_type == CollisionType.SPHERE and collider_b.collision_type == CollisionType.SPHERE:
            position_a = entity_a.object3d.global_position
            position_b = entity_b.object3d.global_position
            collider_a_data = collider_a.data
            collider_b_data = collider_b.data

            central_distance = sum((a - b) ** 2 for a, b in zip(position_a, position_b)) ** 0.5 # get the distance between the centers of the spheres
            radius_sum = collider_a_data.get('radius', 0) + collider_b_data.get('radius', 0) # get the sum of the radii of the spheres

            if central_distance < radius_sum:
                return True

        # Add more collision type checks as needed

        return False