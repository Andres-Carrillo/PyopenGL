from core.entity import Entity
from core.components.types import COMPTYPE
from core.components.collision import CollisionType
import numpy as np

def sphere_to_sphere(obj_1:Entity, obj_2:Entity) ->  bool:
    obj_1_collider  = obj_1.get_component(COMPTYPE.COLLIDER)
    obj_2_collider = obj_2.get_component(COMPTYPE.COLLIDER)

    pos_1 = obj_1.local_position
    pos_2 = obj_2.local_position

    rad_1 = obj_1_collider.radius
    rad_2 = obj_2_collider.radius

    distance = np.linalg.norm(np.array(pos_1) - np.array(pos_2))

    return distance <= rad_1 + rad_2
    
def response(ent_a:Entity,ent_b:Entity) -> np.array:
    phys_a = ent_a.get_component(COMPTYPE.PHYSICS)
    phys_b = ent_b.get_component(COMPTYPE.PHYSICS)
    mass_1 = phys_a.mass
    mass_2 = phys_b.mass
    u1 = phys_a.velocity
    u2 = phys_b.velocity

    if u1.all() == 0 or u2.all() == 0:
        return np.array([0.0,0.0,0.0])

    norm = np.array(np.array(ent_a.global_position) - np.array(ent_b.global_position))
    norm_mag = np.linalg.norm(norm) 

    e = np.average(np.array([phys_a.restitution, phys_b.restitution]))
    restitution_factor = (1 + e) *mass_2 / (mass_1 + mass_2)
    norm_factor = ((u2 - u1) *(norm)) / (norm_mag * norm_mag) 

    return  u1 + restitution_factor * norm_factor * norm


def one_sided_response(dynamic_ent,static_ent) -> np.array:
    print("one sided reponse")
    """Calculate impulse for dynamic object colliding with static object."""
    phys = dynamic_ent.get_component(COMPTYPE.PHYSICS)
    
    # Collision normal (from static to dynamic)
    pos_dynamic = np.array(dynamic_ent.global_position)
    pos_static = np.array(static_ent.global_position)
    normal = pos_dynamic - pos_static
    norm_mag = np.linalg.norm(normal)
    
    if norm_mag == 0:
        return np.zeros(3)
    
    normal = normal / norm_mag  # Normalize
    
    # Get velocity along collision normal
    velocity = np.array(phys.velocity)
    velocity_normal = np.dot(velocity, normal)
    
    # If moving away, no impulse needed
    if velocity_normal > 0:
        return np.zeros(3)
    
    # Restitution (bounciness)
    e = phys.restitution
    
    # Impulse magnitude for collision with infinite mass object
    # J = -(1 + e) * v_n * mass
    # But since we're using add_impulse which divides by mass,
    # we need: impulse = -(1 + e) * v_n * normal
    impulse_magnitude = -(1 + e) * velocity_normal
    impulse = impulse_magnitude * normal
    
    return impulse


class CollisionSystem:
    @staticmethod
    def check_collisions(entities:list)-> list:
        collidable = [e for e in entities if e.has_component(COMPTYPE.COLLIDER)]

        collisions = []

        for i in range(len(collidable)):
            for j in range(i + 1, len(collidable)):
                ent_a = collidable[i]
                ent_b = collidable[j]

                if sphere_to_sphere(ent_a,ent_b):
                    collisions.append((ent_a,ent_b))

        return collisions
    
    @staticmethod
    def reslove_collisions(collisions:list)-> None:
        for ent_a,ent_b in collisions:
                physics_data_a = ent_a.get_component(COMPTYPE.PHYSICS)
                physics_data_b = ent_b.get_component(COMPTYPE.PHYSICS)

                # if neither are physics objects then ignore the collision
                if physics_data_a is None and physics_data_b is None:
                    continue

                if physics_data_b is None: # if b is not a physics object then calculate 1-sided impulse
                    impulse = one_sided_response(ent_a,ent_b)
                    physics_data_a.add_impulse(impulse)
                elif physics_data_a is None: #if a is not a physics object then find 1-sided impulse
                    impulse = one_sided_response(ent_b,ent_a)
                    physics_data_b.add_impulse(impulse)
                else:
                    impulse = response(ent_a,ent_b)

                    physics_data_a.add_impulse(impulse)
                    physics_data_b.add_impulse(-impulse)

                
    def run(self,entities: list)-> None:
        collision_pairs = self.check_collisions(entities)

        self.reslove_collisions(collision_pairs)