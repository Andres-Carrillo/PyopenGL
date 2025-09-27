class PhysicsComponent:
    def __init__(self, mass=1.0, velocity=[0,0,0], acceleration=[0,0,0], forces=None):
        self.mass = mass
        self.velocity = velocity
        self.acceleration = acceleration
        self.forces = forces or []