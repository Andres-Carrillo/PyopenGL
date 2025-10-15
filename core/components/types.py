import enum

class Components(enum.IntFlag):
    NONE = 0 # No components
    RIGIDBODY = 1 << 0 # Rigidbody component
    COLLIDER = 1 << 1 # Collider component
    MESH = 1 << 2 # Mesh component
    CAMERA = 1 << 3 # Camera component
    LIGHT = 1 << 4 # Light component
    MOVEABLE = 1 << 5 # Component that allows movement