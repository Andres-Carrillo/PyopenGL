import enum

class CollisionType(enum.IntFlag):
    NONE = 0
    SPHERE = 1
    BOX = 2

class ColliderComponent:
    def __init__(self, collision_type=CollisionType.NONE, data:dict=None):
        self.collision_type = collision_type
        
        if data is None:
            data = {}



