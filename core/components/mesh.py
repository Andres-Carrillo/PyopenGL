from core.meshes.mesh import Mesh
from core.components.types import Components


class MeshComponent:
    def __init__(self, mesh:Mesh=None):
        self.mesh = mesh
        self.type = Components.MESH