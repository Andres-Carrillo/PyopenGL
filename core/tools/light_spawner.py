# Light imports
from core.components.types import Components
from core.light.directional import DirectionalLight
from core.light.point import PointLight
from core.light.ambient import AmbientLight
from core.light.light import LIGHT_TYPE

# tool imports
from core.tools.point_light_tool import PointLightTool
from core.tools.directional_light_tool import DirectionalLightTool

# import shadows
from core.light.shadow import Shadow
from core.tools.bbox import BBoxMesh

from core.entity import Entity  
from core.components.light import LightComponent
import imgui


class LightFactory:

    def create(self,light_type:int,location:list[float]=None,color:list[float]=None,intensity:float=None,show_helper:bool=None, attenuation:list[float]=None,direction:list[float]=None):
        light = None
        light_entity = Entity()

        match light_type:
            case LIGHT_TYPE.POINT.value:
                light = PointLight(color=color, position=location, attenuation=attenuation, max_distance=325)

            case LIGHT_TYPE.DIRECTIONAL.value:
                light = DirectionalLight(color=color, direction=direction)

            case LIGHT_TYPE.AMBIENT.value:
                light = AmbientLight(color=color, attenuation=attenuation)


        light_entity.add_component(Components.LIGHT, LightComponent(light_object=light))

        return light_entity


class LightSpawnerView:
    def __init__(self, light_factory:LightFactory):
        self._factory = light_factory
        self._type = LIGHT_TYPE.POINT.value
        self._color = [1.0, 1.0, 1.0]
        self._location = [0.0, 5.0, 0.0]


    def render(self):
        # The GUI for the light spawner
        # Text for light type
        imgui.text("Light Type")

        imgui.set_next_item_width(100) # Set width for the combo box

        # Combo box for light type selection populated from LIGHT_TYPE enum
        _,self._type = imgui.combo("##Light Type", self._light_type, 
                                        [str(light_type) for light_type in LIGHT_TYPE])
        

        # Color picker for light color
        imgui.text("Color:")
        imgui.same_line()

        _,self._color = imgui.color_edit3("##Color", *self._color)


        # checkbox for showing helper
        imgui.same_line()
        _,self._show_helper = imgui.checkbox("Show Helper", self._show_helper)
        imgui.same_line()
        _,self.use_lights = imgui.checkbox("Use Lights", self.use_lights)

        #options for  light location
        imgui.text("Location:")
        imgui.same_line()
        imgui.set_next_item_width(150)
        _,self._location = imgui.input_float3("##Location", *self._location)


class LightSpawnerController:
    def __init__(self, light_factory:LightFactory,light_view:LightSpawnerView):
        self._factory = light_factory
        self._view = light_view
        self._lights = []
        self.use_lights = True

    @property
    def view(self):
        return self._view

    @property
    def lights(self):
        return self._lights

    def spawn_light(self):
        light_entity = self._factory.create(
            light_type=self._view.type,
            location=self._view.location,
            color=self._view.color,
            intensity=1.0,
            show_helper=self._view.show_helper,
            attenuation=[1.0, 0.0, 0.1],
            direction=[-1.0, -1.0, -1.0]
        )
        
        self._lights.append(light_entity)
        
        return light_entity
    

    def update(self):
        self._view.render()

        if imgui.button("Add Light"):
            return self.spawn_light()


        return None