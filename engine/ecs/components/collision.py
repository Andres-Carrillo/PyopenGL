import enum

class CollisionType(enum.IntFlag):
    SPHERE =  1
    BOX =     2
    CAPSULE = 4
    MESH =    8
