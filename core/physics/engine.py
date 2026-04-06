from core.object3D import Object3D
from core.entity import Entity
from core.components.types import COMPTYPE
from core.systems.collision import CollisionSystem
import numpy as np

class PhysicsEngine:
    def __init__(self,gravity= [0, -9.81, 0],entities:list = []):
        self.gravity = np.array(gravity)
        self._entities = entities
        self._collision_system = CollisionSystem()

    def add_object(self, obj:Object3D):
        self._entities.append(obj)

    def remove_object(self, obj:Object3D):
        self._entities.remove(obj)

    def update(self, delta_time:float):
        for obj in self._entities:
            self._integrate(obj,self.gravity,delta_time)
            
    def _integrate(self,body:Entity,gravity:np.ndarray,delta_time:float):
        """Symplectic Euler for more stable integration"""
        # get physics components — must use COMPTYPE flag, not the class, as the key
        phys_body = body.get_component(COMPTYPE.PHYSICS)
        
        # edge case the object is not a physicbody --> avoid integration
        if not phys_body:
            return
        
        grav_acc = gravity if phys_body.use_gravity else np.zeros(3)

        accel = phys_body.force_accumulator * phys_body.inverse_mass() + grav_acc

        # symplemtic Euler
        phys_body.velocity += accel * delta_time
        phys_body.velocity *= (1.0 - phys_body.damping * delta_time)

        body.set_position(np.array(body.local_position) + phys_body.velocity * delta_time)

        phys_body.clear_forces()            