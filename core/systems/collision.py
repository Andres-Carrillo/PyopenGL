from core.entity import Entity
from core.components.types import COMPTYPE
from core.components.collision import CollisionType
from dataclasses import dataclass
import numpy as np


@dataclass
class Contact:
    entity_a:    Entity
    entity_b:    Entity
    normal:      np.ndarray
    penetration: float
    point:       np.ndarray

def sphere_vs_sphere(obj_1:Entity, obj_2:Entity) ->  Contact | None:
    obj_1_collider  = obj_1.get_component(COMPTYPE.COLLIDER)
    obj_2_collider = obj_2.get_component(COMPTYPE.COLLIDER)

    delta = np.array(obj_1.global_position) - np.array(obj_2.global_position)
    sum_radi =  obj_1_collider.radius +  obj_2_collider.radius
    
    distance = np.linalg.norm(np.array(delta))
    
    if distance >= sum_radi:
        return None
    

    if distance == 0:
        norm = np.array([0,1,0])
    else:
        norm = np.array(delta / distance)

    penetration = sum_radi - distance

    return Contact(entity_a=obj_1,
                   entity_b=obj_2,
                   normal=norm,
                   penetration=penetration,
                   point = obj_2.global_position + norm * obj_2_collider.radius
                   )

def aabb_vs_aabb(enitity_a:Entity,entitity_b:Entity) -> Contact | None:
    col_a = enitity_a.get_component(COMPTYPE.COLLIDER)
    col_b = entitity_b.get_component(COMPTYPE.COLLIDER)

    half_a = np.array([col_a.width,col_a.height,col_a.depth]) * 0.5
    half_b = np.array([col_b.width,col_b.height,col_b.depth]) * 0.5

    delta = enitity_a.global_position - entitity_b.global_position

    overlap_x = (half_a[0] + half_b[0] - abs(delta[0]))
    overlap_y = (half_a[1] + half_b[1] - abs(delta[1]))
    overlap_z = (half_a[2] + half_b[2] - abs(delta[2]))

    # all three must overlap for an intersection
    if overlap_x <= 0 or overlap_z <= 0 or overlap_y <= 0:
        return None

    # get min penetration axis:
    if overlap_x <= overlap_y and overlap_x <= overlap_z:
        normal = np.array([np.sign(delta[0]), 0.0, 0.0])
        penetration = overlap_x
    elif overlap_y <= overlap_z:
        normal = np.array([0.0, np.sign(delta[1]), 0.0])
        penetration = overlap_y
    else:
        normal = np.array([0.0, 0.0, np.sign(delta[2])])
        penetration = overlap_z

    # get contact point:
    overlap_min = np.minimum(enitity_a.global_position - half_a,entitity_b.global_position - half_b)
    overlap_max = np.maximum(enitity_a.global_position + half_a, entitity_b.global_position + half_b)

    #contact point is the center of overlap region
    point = (overlap_min + overlap_max) * 0.5

    return Contact(entity_a=enitity_a,
                   entity_b=entitity_b,
                   normal=normal,
                   penetration=penetration,
                   point=point)

def sphere_vs_aabb(sphere_ent:Entity,box_ent:Entity) -> Contact | None:
    sphere_col = sphere_ent.get_component(COMPTYPE.COLLIDER)
    box_col = box_ent.get_component(COMPTYPE.COLLIDER)

    half_box = np.array([box_col.width,box_col.height,box_col.depth]) * 0.5
    box_min = box_ent.global_position - half_box
    box_max = box_ent.global_position + half_box
  
    #closest point from box to sphere
    closest = np.clip(sphere_ent.global_position,box_min,box_max)

    delta = np.array(sphere_ent.global_position) - closest
    distance = np.linalg.norm(delta)

    # check for intersection 
    if distance >= sphere_col.radius:
        return None
    
    if distance == 0:
        normal = np.array([0,1,0])
    else:
        normal = delta / distance

    penetration = sphere_col.radius - distance
    return Contact(entity_a=sphere_ent,
                   entity_b=box_ent,
                   normal=normal,
                   penetration=penetration,
                   point=closest)


def positional_correction(contact: Contact,slope:float,percent:float) -> None:
    phys_a = contact.entity_a.get_component(COMPTYPE.PHYSICS)
    phys_b = contact.entity_b.get_component(COMPTYPE.PHYSICS)

    inv_a = phys_a.inverse_mass() if phys_a else 0.0
    inv_b = phys_b.inverse_mass() if phys_b else 0.0
    inv_sum = inv_a + inv_b

    if inv_sum  == 0.0:
        return
    
    magnitude = max(contact.penetration - slope, 0.0) / inv_sum * percent
    correction = magnitude * contact.normal

    pos_a = np.array(contact.entity_a.global_position)
    pos_b = np.array(contact.entity_b.global_position)

    contact.entity_a.set_position(pos_a + correction * inv_a)
    contact.entity_b.set_position(pos_b - correction * inv_b)
    pass

def impulse(contact:Contact) -> np.ndarray:
    phys_a = contact.entity_a.get_component(COMPTYPE.PHYSICS)
    phys_b = contact.entity_b.get_component(COMPTYPE.PHYSICS)

    # use zero velocity for entities without physics (treated as immovable)
    vel_a = phys_a.velocity if phys_a else np.zeros(3)
    vel_b = phys_b.velocity if phys_b else np.zeros(3)

    # relative velocity -> how fast are the objects moving towards each other
    rel_velocity = vel_a - vel_b

    """ project relative velocity onto collision normal:
            positive ->  separating
            negative ->  approaching
    """
    velocity_along_normal = np.dot(rel_velocity, contact.normal)

    # if the objects are already moving apart do nothing:
    if velocity_along_normal > 0:
        return np.zeros(3)

    inv_a = phys_a.inverse_mass() if phys_a else 0.0
    inv_b = phys_b.inverse_mass() if phys_b else 0.0
    inv_mass_sum = inv_a + inv_b

    # both static — nothing to resolve
    if inv_mass_sum == 0.0:
        return np.zeros(3)

    bounce = min(
        phys_a.restitution if phys_a else 0.0,
        phys_b.restitution if phys_b else 0.0
    )

    """
        scalar impulse -> how much force to apply
            numerator: how much to reverse the approach velocity
            denominator: total resistance to the impulse (sum of inverse masses)
        add_impulse() scales per body by its own inverse_mass, so j must
        already incorporate the full mass denominator here.
    """
    j = -(1 + bounce) * velocity_along_normal / inv_mass_sum

    return j * contact.normal

class CollisionSystem:
    def __init__(self,positional_slope: float = 0.01,positional_percent: float = 0.4):
        self.positional_slope = positional_slope
        self.positional_percent = positional_percent


    def check_collisions(self,entities:list)-> list:
        collidable = [e for e in entities if e.has_component(COMPTYPE.COLLIDER)]

        collisions = []

        for i in range(len(collidable)):
            for j in range(i + 1, len(collidable)):
                ent_a = collidable[i]
                ent_b = collidable[j]

                contact = sphere_vs_sphere(ent_a,ent_b)

                if contact:
                    collisions.append(contact)

        return collisions
    
    
    def resolve_collisions(self,collisions:list)-> None:
        for contact in collisions:
                ent_a = contact.entity_a
                ent_b = contact.entity_b
                physics_data_a = ent_a.get_component(COMPTYPE.PHYSICS)
                physics_data_b = ent_b.get_component(COMPTYPE.PHYSICS)

                if physics_data_a is None and physics_data_b is None:
                    continue

                imp = impulse(contact)
                
                if physics_data_a is not None:
                    physics_data_a.add_impulse(imp)
                
                if physics_data_b is not None:
                    physics_data_b.add_impulse(-imp)

                positional_correction(contact,self.positional_slope,self.positional_percent)


    def run(self,entities: list)-> None:
        collision_pairs = self.check_collisions(entities)

        self.resolve_collisions(collision_pairs)