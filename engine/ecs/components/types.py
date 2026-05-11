import enum

#using intFla
class COMPTYPE(enum.IntFlag):
    NONE =       0   # No components
    PHYSICS =    1   # Rigidbody component (2^0)
    COLLIDER =   2   # Collider component (2^1)
    MESH =       4   # Mesh component (2^2)
    CAMERA =     8   # Camera component (2^3)
    LIGHT =      16  # Light component (2^4)
    MOVEABLE =   32  # Component that allows movement (2^5)
    CONTROLLER = 64  # Controller component (2^6)
    POSITION =   128 # POSITIONAL Component (2^7)
    SPEED =      256 # SPEED COMP