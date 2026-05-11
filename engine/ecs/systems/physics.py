from engine.ecs.entity import Entity
from engine.ecs.components.types import COMPTYPE
import numpy as np

class PhysicsSystem:
    def __init__(self,gravity= [0, -9.81, 0]):
        self.gravity = np.array(gravity)

    def update(self,entities:list, delta_time:float):
        for obj in entities:
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