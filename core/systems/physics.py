from core.entity import Entity
from core.components.types import Components
from core.components.physics import PhysicsComponent


EARTH_GRAVITY = [0, -9.81, 0]

def global_gravity(entity:Entity,  gravity_vector:list = None):
    if gravity_vector is None:
        gravity_vector = EARTH_GRAVITY

    if entity.has_component(Components.PHYSICS):
        physics = entity.get_component(Components.PHYSICS)
        physics.add_force(gravity_vector) 



def wind_force(entity:Entity, wind_vector:list = [0.0,0.0,0.0]):

    if entity.has_component(Components.PHYSICS):
        physics = entity.get_component(Components.PHYSICS)
        physics.add_force(wind_vector) 

class PhysicsSystem:
    _global_forces = [global_gravity, wind_force]  # List of constant/global force functions

    @property
    def global_forces(self):
        return self._global_forces

    @staticmethod
    def apply_constant_forces(entities:list, gravitational_acceleration:list = EARTH_GRAVITY, wind_vector:list = [0.0, 0.0, 0.0]): # applies global forces to all entities with a rigidbody component
        for entity in entities:
            if entity.has_component(Components.PHYSICS):
                for force in PhysicsSystem.global_forces:
                    if force == global_gravity:
                        force(entity, gravitational_acceleration)
                    elif force == wind_force:
                        force(entity, wind_vector)
                    else:
                        force(entity)

    
    @staticmethod
    def apply_force(entity:Entity, force:list):
        if entity.has_component(Components.PHYSICS):
            physics = entity.get_component(Components.PHYSICS)
            physics.add_force(force)


    @staticmethod
    def update_physics(entities:list, delta_time:float):

        print("all entities:", entities)
        physics_entities = [e for e in entities if e.has_component(Components.PHYSICS)]

        print("physics entities:", len(physics_entities))
