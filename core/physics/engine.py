from core.object3D import Object3D
class PhysicsEngine:
    def __init__(self,forces:list = [[0, -9.81, 0]],objects:list = []):
        self.forces = forces
        self.objects = objects

    def add_object(self, obj:Object3D):
        self.objects.append(obj)

    def remove_object(self, obj:Object3D):
        self.objects.remove(obj)

    def update(self, delta_time):
        for obj in self.objects:
            for force in self.forces:
                obj.apply_matrix(force)
            # obj.update(delta_time, self.gravity)


    def handle_collisions(self):
        for i in range(len(self.objects)):
            for j in range(i + 1, len(self.objects)):
                obj_a = self.objects[i]
                obj_b = self.objects[j]
                if obj_a.collides_with(obj_b):
                    obj_a.handle_collision(obj_b)
                    obj_b.handle_collision(obj_a)