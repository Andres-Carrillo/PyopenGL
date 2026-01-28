from dataclasses import dataclass,field
from core.meshes.mesh import Mesh
from core.components.types import COMPTYPE
from core.components.collision import CollisionType
import glfw.GLFW as GLFW_CONSTANTS
from core.light.light import LIGHT_TYPE, Light
import numpy as np

@dataclass
class MeshComponent:
    mesh: Mesh

    type: COMPTYPE = COMPTYPE.MESH


@dataclass
class PositionComponent:
    x:        int
    y:        int
    z:        int 
    rotation: float

    type: COMPTYPE = COMPTYPE.POSITION

@dataclass
class VeclocityComponent:
    dx:         float = field(default=0.0)
    dy:         float = field(default=0.0)
    dz:         float = field(default=0.0)
    direction:  float = field(default=0.0)

    type: COMPTYPE = COMPTYPE.MOVEABLE
    

@dataclass
class ControllerComponent:
    # Movement Keys:
    forward_key:  int = GLFW_CONSTANTS.GLFW_KEY_W
    backward_key: int = GLFW_CONSTANTS.GLFW_KEY_S
    left_key:     int = GLFW_CONSTANTS.GLFW_KEY_A
    right_key:    int = GLFW_CONSTANTS.GLFW_KEY_D
    jump_key:     int = GLFW_CONSTANTS.GLFW_KEY_SPACE
    crouch_key:   int = GLFW_CONSTANTS.GLFW_KEY_LEFT_CONTROL

    #camera keys: 
    look_up_key:    int = GLFW_CONSTANTS.GLFW_KEY_UP
    look_down_key:  int = GLFW_CONSTANTS.GLFW_KEY_DOWN
    look_left_key:  int = GLFW_CONSTANTS.GLFW_KEY_LEFT
    look_right_key: int = GLFW_CONSTANTS.GLFW_KEY_RIGHT

    # Movement speed multipliers
    move_speed:        float = 5.0
    sprint_multiplier: float = 2.0
    
    # Mouse control settings
    mouse_sensitivity: float = 0.1
    invert_y:       bool = False
    use_mouse_look: bool = True
    
    type:           COMPTYPE = COMPTYPE.CONTROLLER

@dataclass
class CollisionComponent:
    shape: CollisionType.BOX

    radius: float = 1.0 # used for both sphere and capsule collisions types
    width:  float = 1.0 # used for box type collision
    height: float = 1.0 # used for box and capsule type collision
    depth:  float = 1.0  # used for box collision

    # offset from the entity system
    offset: list = field(default_factory=lambda: np.array([0.0,0.0,0.0]))

    #filtering
    collision_layer: int = 1
    collision_mask:  int = -1 

    # response:
    is_trigger: bool = False
    is_static:  bool = False

    #physics:
    friction: float = 0.5
    bounciness: float = 0.0

    #state:
    is_collidiing: bool = field(default=False,init=False)
    colliding_with: set = field(default_factory=set,init=False)

    type: COMPTYPE = COMPTYPE.COLLIDER
    
@dataclass
class PhysicsBody:
    mass:     float = 1.0
    inertia:  float = 0.0
    damping:  float = 0.0

    velocity: list = field(default_factory= lambda: np.array([0.0,0.0,0.0]))
    acceleration:    list = field(default_factory= lambda:np.array([0.0,0.0,0.0]))

    # the coefficent of restitution
    restitution: float = 0.5

    # holds forces to act on object
    force_accumulator: list = field(default_factory= lambda: np.array([0.0,0.0,0.0]))

    use_gravity: bool = True

    type: COMPTYPE = COMPTYPE.PHYSICS


    def inverse_mass(self):
        return 1.0/self.mass if self.mass > 0 else 0.0

    def add_force(self,force: np.array)->None :
        self.force_accumulator += force

    def add_impulse(self,impulse:np.array)->None:
        if self.mass == 0.0:
            return

        self.velocity += impulse*self.inverse_mass()

    def clear_forces(self):
        self.force_accumulator = np.zeros_like(self.force_accumulator)

@dataclass
class LightComponent:
    light: Light
    light_type: LIGHT_TYPE

    type: COMPTYPE = COMPTYPE.LIGHT