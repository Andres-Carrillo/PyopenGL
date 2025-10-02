class PhysicsComponent:
    def __init__(self, mass=1.0, velocity=[0,0,0], acceleration=[0,0,0], forces=None):
        self.mass = mass
        self.local_forces = forces or []
        self.velocity = velocity
        self.acceleration = acceleration


    def add_force(self, force:list = [0,0,0]):
        self.local_forces.append(force)