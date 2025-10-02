from object3D import Object3D
from core.components.types import Components

class Entity:
    def __init__(self,object3d:Object3D=None):
        self.object3d = object3d if object3d is not None else Object3D()
        self.components = Components.NONE
        self.comp_data = {}

    def add_component(self,component:Components,data=None):
        self.components |= component
        if data is not None:
            self.comp_data[component] = data
    

    def remove_component(self,component:Components):
        self.components &= ~component
        if component in self.comp_data:
            del self.comp_data[component]
    
    def get_component(self,component:Components):
        return self.comp_data.get(component,None)
    
    def has_component(self,component:Components):
        return (self.components & component) == component
    
    def toggle_component(self,component:Components):
        self.components ^= component
        
    def get_components(self):
        return [comp for comp in Components if comp != Components.NONE and self.has_component(comp)]
    
    
    def __str__(self):
        return f"Entity(components={[str(comp) for comp in self.get_components()]})"
    


def entity_spawner(Object3D:Object3D=None,components:Components=Components.NONE,comp_data:dict=None):
    entity = Entity(Object3D)
    entity.components = components

    if comp_data is not None:
        entity.comp_data = comp_data

    return entity


def add_collider(entity:Entity,collision_type:Components,data:dict=None):
    entity.add_component(Components.COLLIDER,data={'collision_type':collision_type,'data':data})


