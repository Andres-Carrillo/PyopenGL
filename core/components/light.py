from core.light.light import LIGHT_TYPE, Light
from core.light.ambient import AmbientLight
from core.light.directional import DirectionalLight
from core.light.point import PointLight



class LightComponent:
    def __init__(self, light_object:Light):
        self.light_object = light_object
        
