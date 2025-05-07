from light.light import Light
from light.light import LIGHT_TYPE

class PointLight(Light):
    def __init__(self,color:list=[1.0, 1.0, 1.0], position:list=[0.0, 0.0, 0.0], attenuation:list=[1.0, 0.0, 0.1]) -> None:
        super().__init__(LightType=LIGHT_TYPE.POINT, color=color, attenuation=attenuation)
        self.set_pos(position)