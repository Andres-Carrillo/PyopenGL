from core.meshes.mesh import Mesh
from core.components.types import COMPTYPE
from core.object3D import Object3D
from dataclasses import dataclass

class Entity(Object3D):
    def __init__(self):
        super().__init__()
        self.components = COMPTYPE.NONE
        self.comp_data = {}

    def add_component(self, component: COMPTYPE, data : dataclass=None):
        """
        Add a component to the entity.
        
        :param component: The component type flag (e.g., Components.MESH)
        :param data: The component data object (e.g., MeshComponent instance)
        """
        # Set the component flag using bitwise OR
        self.components |= component
        
        # Store the component data
        if data is not None:
            self.comp_data[component] = data
    
    def remove_component(self, component: COMPTYPE):
        """
        Remove a component from the entity.
        
        :param component: The component type to remove
        """
        # Clear the component flag using bitwise AND with NOT
        self.components &= ~component
        
        # Remove the component data
        if component in self.comp_data:
            del self.comp_data[component]
    
    def get_component(self, component: COMPTYPE):
        """
        Get the data for a specific component.
        
        :param component: The component type to retrieve
        :return: The component data object, or None if not present
        """
        return self.comp_data.get(component, None)
    
    def has_component(self, component: COMPTYPE) -> bool:
        """
        Check if the entity has a specific component.
        
        :param component: The component type to check
        :return: True if the entity has the component, False otherwise
        """
        # Use bitwise AND to check if the component flag is set
        return (self.components & component) == component
    
    def toggle_component(self, component: COMPTYPE):
        """
        Toggle a component on/off using XOR.
        
        :param component: The component type to toggle
        """
        self.components ^= component
        
        # Remove data if toggling off
        if not self.has_component(component) and component in self.comp_data:
            del self.comp_data[component]
        
    def get_components(self):
        """
        Get a list of all components attached to this entity.
        
        :return: List of component types that are set
        """
        return [comp for comp in COMPTYPE if comp != COMPTYPE.NONE and self.has_component(comp)]
    
    def __str__(self):
        comp_names = [comp.name for comp in self.get_components()]
        return f"Entity(components={comp_names})"
    


def entity_spawner(components: COMPTYPE = COMPTYPE.NONE, comp_data: dict = None):
    """
    Helper function to create an entity with components.
    
    :param components: Bitwise combination of component flags
    :param comp_data: Dictionary mapping component types to their data objects
    :return: New Entity instance
    
    Example:
        entity = entity_spawner(
            components=Components.MESH | Components.COLLIDER,
            comp_data={
                Components.MESH: MeshComponent(mesh=my_mesh),
                Components.COLLIDER: CollisionComponent(shape=CollisionType.SPHERE, radius=1.0)
            }
        )
    """
    entity = Entity()
    entity.components = components

    if comp_data is not None:
        entity.comp_data = comp_data

    return entity


# def add_collider(entity:Entity,collision_type:Components,data:dict=None):
#     entity.add_component(Components.COLLIDER,data={'collision_type':collision_type,'data':data})


