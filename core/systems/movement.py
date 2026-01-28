from core.entity import Entity
from core.components.types import COMPTYPE

def move(entities: list[Entity], delta_time: float = 1.0):
    """
    Move entities based on their velocity components.
    
    Args:
        entities: List of entities to move
        delta_time: Time elapsed since last frame (for frame-independent movement)
    """
    for entity in entities:
        physbody = entity.get_component(COMPTYPE.PHYSICS)
        if physbody is None:
            continue
            
        # Get current position from the entity (single source of truth)
        current_position = entity.local_position
        physbody.acceleration = physbody.force_accumulator / physbody.mass if physbody.mass > 0 else physbody.force_accumulator

        physbody.velocity += physbody.acceleration * delta_time
        # Calculate new position based on velocity and delta time
        new_position = [
            current_position[0] + delta_time * physbody.velocity[0],
            current_position[1] + delta_time * physbody.velocity[1],
            current_position[2] + delta_time * physbody.velocity[2]
        ]
        
        # Update entity position (single update point)
        entity.set_position(new_position)
        
        # If entity has a mesh component, sync the mesh position to match entity
        mesh_component = entity.get_component(COMPTYPE.MESH)
        if mesh_component is not None:
            mesh_component.mesh.set_position(new_position)
