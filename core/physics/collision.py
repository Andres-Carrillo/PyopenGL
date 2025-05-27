from geometry.geometry import Geometry
import enum
from math import sqrt,dist,pow

class CollisionType(enum.Enum):
    NONE = 0
    SPHERE = 1
    BOX = 2
    PLANE = 3
    MESH = 4
    CYLINDER = 5
    CONE = 6
    CAPSULE = 7

    def __str__(self):
        return self.name.lower()
    
class Collider:
    def __init__(self,collion_type:CollisionType = CollisionType.NONE,position:list = [0, 0, 0], rotation:list = [0, 0, 0]):
        self.position = position
        self.rotation = rotation
        self.collision_type = collion_type

class SphereCollider(Collider):
    def __init__(self,radius:float = 1.0,position:list = [0, 0, 0], rotation:list = [0, 0, 0]):
        super().__init__(CollisionType.SPHERE, position, rotation)
        self.radius = radius

class BoxCollider(Collider):
    def __init__(self, width: float = 1.0, height: float = 1.0, depth: float = 1.0, position:list = [0, 0, 0], rotation:list = [0, 0, 0]):
        super().__init__(CollisionType.BOX, position, rotation)
        self.width = width
        self.height = height
        self.depth = depth

def box_to_box_collision(collider_a: BoxCollider, collider_b: BoxCollider):
    """ Basic box-to-box collision detection.
    Checks if two axis-aligned boxes are colliding based on their positions and dimensions.
    Returns a tuple (is_colliding, collision_response) where:
        - is_colliding: True if the boxes are colliding, False otherwise.
    
        - collision_response: A dictionary containing collision details if they are colliding, None otherwise.
    """
    # edge case: if any of the boxes has zero width, height, or depth, they cannot collide
    if collider_a.width == 0 or collider_a.height == 0 or collider_a.depth == 0 or \
    collider_b.width == 0 or collider_b.height == 0 or collider_b.depth == 0:
        return False, None

    # Check if the boxes are colliding
    is_colliding = (
        abs(collider_a.position[0] - collider_b.position[0]) < (collider_a.width + collider_b.width) / 2 and
        abs(collider_a.position[1] - collider_b.position[1]) < (collider_a.height + collider_b.height) / 2 and
        abs(collider_a.position[2] - collider_b.position[2]) < (collider_a.depth + collider_b.depth) / 2
    )

    if is_colliding:
        # Calculate the collision response
        
        normal = [
            (collider_b.position[i] - collider_a.position[i]) / max(1e-6, abs(collider_b.position[i] - collider_a.position[i]))
            for i in range(3)
        ]

        length = sqrt(sum([n ** 2 for n in normal]))

        # Normalize the normal vector to avoid division by zero
        # if length is very small, we set it to zero for stability
        if length > 1e-6:
            normal = [n / length for n in normal]
        else:
            normal = [0, 0, 0]

        collision_response = {
            'collider_a': collider_a,
            'collider_b': collider_b,
            'penetration_depth': {
                'x': (collider_a.width + collider_b.width) / 2 - abs(collider_a.position[0] - collider_b.position[0]),
                'y': (collider_a.height + collider_b.height) / 2 - abs(collider_a.position[1] - collider_b.position[1]),
                'z': (collider_a.depth + collider_b.depth) / 2 - abs(collider_a.position[2] - collider_b.position[2])
            },
            'normal': normal
        }
        return True, collision_response
    
    return False, None

def sphere_to_sphere_collision(collider_a: SphereCollider, collider_b: SphereCollider):
    """ Basic sphere-to-sphere collision detection.
    Checks if two spheres are colliding based on their positions and radii.
    Returns a tuple (is_colliding, collision_response) where:
        - is_colliding: True if the spheres are colliding, False otherwise.
    
        - collision_response: A dictionary containing collision details if they are colliding, None otherwise.
    """

    if collider_a.radius <= 0 or collider_b.radius <= 0:
        return False, None
    
    # calculate the distance between the centers of the two spheres while avoiding sqrt for performance
    pseudo_distance = sum([(collider_b.position[i] - collider_a.position[i]) ** 2 for i in range(3)])

    if pseudo_distance < (collider_a.radius + collider_b.radius) ** 2:
        # Calculate the collision response
        collision_response = {
            'collider_a': collider_a,
            'collider_b': collider_b,
            'penetration_depth': (collider_a.radius + collider_b.radius) - pseudo_distance ** 0.5,
            'normal': [(collider_b.position[i] - collider_a.position[i]) / pseudo_distance ** 0.5 for i in range(3)]
        }

        return True, collision_response
    
    return False, None

def sphere_to_box_collision(sphere: SphereCollider, box: BoxCollider):
    """ Basic sphere-to-box collision detection.
    find the point on the box that is closest to the sphere's center
    and check if the distance from that point to the sphere's center is less than the sphere's radius.
    Returns a tuple (is_colliding, collision_response) where:
        - is_colliding: True if the sphere and box are colliding, False otherwise.
        - collision_response: A dictionary containing collision details if they are colliding, None otherwise.
    """

    if sphere.radius <= 0 or box.width <= 0 or box.height <= 0 or box.depth <= 0:
        return False, None
    # get the box's min and max coordinates
    # box_min and box_max are the coordinates of the box's corners
    box_min = [
        box.position[0] - box.width / 2,
        box.position[1] - box.height / 2,
        box.position[2] - box.depth / 2
    ]
    box_max = [
        box.position[0] + box.width / 2,
        box.position[1] + box.height / 2,
        box.position[2] + box.depth / 2
    ]

    # find the closest point on the box to the sphere's center
    closest_point = [
        max(box_min[i], min(sphere.position[i], box_max[i])) for i in range(3)
    ]

    # calculate the distance from the sphere's center to the closest point
    distance = sqrt(sum([(closest_point[i] - sphere.position[i]) ** 2 for i in range(3)]))
    if distance < sphere.radius:
        # Calculate the collision response
        collision_response = {
            'collider_a': sphere,
            'collider_b': box,
            'penetration_depth': distance - sphere.radius,
            'closest_point': closest_point,
            'normal': [(sphere.position[i] - closest_point[i]) / distance for i in range(3)]
        }
        return True, collision_response
    
    return False, None
    
class CollisionDispatcher:
    _collision_handlers = {
            (CollisionType.SPHERE, CollisionType.SPHERE): sphere_to_sphere_collision,
            (CollisionType.BOX, CollisionType.BOX): box_to_box_collision,
            (CollisionType.SPHERE, CollisionType.BOX): sphere_to_box_collision,
            # Add more collision handlers as needed
        }
    
    @property
    def dispatcher(self):
        return self._collision_handlers

    @staticmethod
    def handle_collision(self, collider_a: Collider, collider_b: Collider):
        # create tuple of collision types
        key = (collider_a.collision_type, collider_b.collision_type)

        # check if the key exists in the dispatcher
        if key in CollisionDispatcher.dispatcher:
            # get the handler function
            handler = CollisionDispatcher.dispatcher[key]
            
            return handler(collider_a, collider_b)

        # the collision type is not supported
        return None