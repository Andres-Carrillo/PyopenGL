import OpenGL.GL as gl
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from ecs.components.types import COMPTYPE
from ecs.components.components import CameraComponent
from ecs.entity import Entity
from collections import namedtuple

RenderEntry = namedtuple("RenderEntry",[
    "world_matrix",
    "geometry",
    "material",
    "cast_shadow"
])


def sort_perspsective(entry:RenderEntry,cam:CameraComponent):
    pass

def sort_distance(entry:RenderEntry,cam:CameraComponent):
    pass

def sort_world_y(entry:RenderEntry,cam:CameraComponent):
    pass

class RenderSystem:
    
    def __init__(self,clear_color:list = [0.0, 0.0, 0.],window_width:int=SCREEN_WIDTH,window_height:int = SCREEN_HEIGHT,use_lights=False) -> None:
        gl.glEnable(gl.GL_DEPTH_TEST)
        # enables anti-aliasing
        gl.glEnable(gl.GL_MULTISAMPLE)

        # enables blending
        gl.glEnable(gl.GL_BLEND)
        # set the blending function
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # set the clear color
        gl.glClearColor(clear_color[0], clear_color[1], clear_color[2], 1.0)

        self.window_size = (window_width,window_height)

        self.shadows_enabled = False
        self.bound_box_enabled = False
        self._use_lights = use_lights
        self._camera = None
    
    def set_camera(self,camera:Entity) -> bool:
        if camera.has_component(COMPTYPE.CAMERA):
            self._camera = camera
            return True
        
        return False


    def update(self,entities:list,dt:float) -> bool:
        if not self._camera:
            return False
        
        render_list = self._collect(entities)
        render_list = self._z_sort(render_list,self._camera)
        self._render(render_list,self._camera)


    def _collect(self,entities:list[Entity]) -> list[Entity]:
        pass

    def _z_sort(self,entities:list[Entity]) -> list[Entity]:
        pass

    def _render(self,entities:list[Entity]) -> list[Entity]:
        pass
        