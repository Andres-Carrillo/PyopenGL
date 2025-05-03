from core.object3D import Object3D
import OpenGL.GL as gl

class Mesh(Object3D):

    def __init__(self,geometry,material) -> None:
        super().__init__()
        self.geometry = geometry
        self.material = material
        self.visible = True
        
        self._init_buffers()


    def _init_buffers(self):
        self.vao_ref = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao_ref)
        
        for var_name,attrib_obj in self.geometry.attributes.items():
            attrib_obj.associateVariable(self.material.program,var_name)

        gl.glBindVertexArray(0)