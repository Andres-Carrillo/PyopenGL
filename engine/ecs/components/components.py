from dataclasses import dataclass,field
from engine.material.basic.material import Material
from engine.ecs.components.types import COMPTYPE
from engine.ecs.components.collision import CollisionType
from engine.geometry.geometry import Geometry
import glfw.GLFW as GLFW_CONSTANTS
from engine.rendering.light.light import LIGHT_TYPE, Light
from engine.utils.matrix import Matrix
import numpy as np

@dataclass
class MeshComponent:
    geometry:    Geometry
    material:    Material
    visible:     bool = True
    case_shadow: bool = True
    type:        COMPTYPE = COMPTYPE.MESH
    offest:      np.ndarray = field(default_factory=lambda:
                                 np.zeros(3))
    
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

    velocity: np.ndarray = field(default_factory=lambda: np.array([0.0, 0.0, 0.0], dtype=np.float64))
    acceleration:    np.ndarray = field(default_factory= lambda:np.array([0.0,0.0,0.0]))
        # holds forces to act on object
    force_accumulator: np.ndarray = field(default_factory= lambda: np.array([0.0,0.0,0.0]))

    # the coefficent of restitution
    restitution: float = 0.5

    use_gravity: bool = True

    type: COMPTYPE = COMPTYPE.PHYSICS


    def inverse_mass(self):
        return 1.0/self.mass if self.mass > 0 else 0.0

    def add_force(self,force: np.array)->None :
        self.force_accumulator += force

    def add_impulse(self,impulse:np.array)->None:
        if self.mass == 0.0:
            return

        #scaling by inverse mass here rather than in impulse:
        #       makes logic cleaner in the long run
        self.velocity += impulse*self.inverse_mass() 

    def clear_forces(self):
        self.force_accumulator = np.zeros_like(self.force_accumulator)

@dataclass
class LightComponent:
    light: Light
    light_type: LIGHT_TYPE

    type: COMPTYPE = COMPTYPE.LIGHT

@dataclass
class CameraComponent:
    angle_of_view:      float = 60.0
    near:               float = 0.1
    far:                float = 1000.0
    aspect_ratio:       float = 1.0
    projection_matrix:  np.ndarray = field(init=False)
    view_matrix:        np.ndarray = field(init=False)
    type:               COMPTYPE = COMPTYPE.CAMERA

    def __post_init__(self):
        """Post Init used to keep project matrix consistent with component values"""
        self.projection_matrix = Matrix.mat4_perspective(self.angle_of_view,self.aspect_ratio,self.near,self.far)
        self.view_matrix       = Matrix.mat4_identity()