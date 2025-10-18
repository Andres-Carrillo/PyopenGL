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
    def __init__(self):
        self._range = [-2,2]
        self.location = [0.0, 0.0, 0.0]
        self._light_count = 0
        self.create_new_object = False
        self.type = LIGHT_TYPE.POINT.value
        self.color = [1.0, 1.0, 1.0]
        self.show_helper = True
        self.use_lights = True

    def create(self,light_type:int,location:list[float]=None,color:list[float]=None,intensity:float=None,show_helper:bool=None, attenuation:list[float]=None,direction:list[float]=None):
        light = None
        light_entity = Entity()


        match light_type:
            case LIGHT_TYPE.POINT.value:
                light = PointLight(color=color, position=location, attenuation=attenuation, max_distance=325)
                light_tool = PointLightTool(light)
                light.add(light_tool)

            case LIGHT_TYPE.DIRECTIONAL.value:
                light = DirectionalLight(color=color, direction=direction)
                light_tool = DirectionalLightTool(light)
                light.add(light_tool)
                

            case LIGHT_TYPE.AMBIENT.value:
                light = AmbientLight(color=color, attenuation=attenuation)


        light_entity.add_component(Components.LIGHT, LightComponent(light_object=light))

        return light_entity


class LightSpawnerView:
    def __init__(self, model:LightFactory):
        self.model = model

    def render(self):
        # The GUI for the light spawner
        # Text for light type
        imgui.text("Light Type")

        imgui.set_next_item_width(100) # Set width for the combo box

        # Combo box for light type selection populated from LIGHT_TYPE enum
        _,self.model.type = imgui.combo("##Light Type", self.model.type, 
                                        [str(light_type.name) for light_type in LIGHT_TYPE])
        
        # Color picker for light color
        imgui.text("Color:")
        imgui.same_line()
        imgui.set_next_item_width(150)
        _,self.model.color = imgui.color_edit3("##Color", *self.model.color)

        # checkbox for showing helper
        _,self.model.show_helper = imgui.checkbox("Show Helper", self.model.show_helper)
        imgui.same_line()
        _,self.model.use_lights = imgui.checkbox("Use Lights", self.model.use_lights)

        #options for  light location
        imgui.text("Location:")
        imgui.same_line()
        imgui.set_next_item_width(150)
        _,self.model.location = imgui.input_float3("##Location", *self.model.location)

        if imgui.button("Add Light"):
            self.model.create_new_object = True


class LightSpawnerController:
    def __init__(self,light_view:LightSpawnerView):
        self.model = light_view.model
        self._view = light_view
        self._lights = []
        self.use_lights = True

    @property
    def view(self):
        return self._view

    @property
    def lights(self):
        return self._lights
    
    @property
    def count(self):
        return len(self._lights)
    
    @property
    def use_lights(self):
        return self._use_lights
    
    @use_lights.setter
    def use_lights(self, value:bool):
        self._use_lights = value

    def spawn_light(self):
        light_entity = self.view.model.create(
            light_type=self.view.model.type,
            location=self.view.model.location,
            color=self.view.model.color,
            intensity=1.0,
            show_helper=self.view.model.show_helper,
            attenuation=[1.0, 0.0, 0.1],
            direction=[-1.0, -1.0, -1.0]
        )
        
        self._lights.append(light_entity)
        
        return light_entity
    

    def run(self):

        if self.model.create_new_object:
            self.model.create_new_object = False
            return self.spawn_light()


        return None
    

    def render(self):
        self.view.render()