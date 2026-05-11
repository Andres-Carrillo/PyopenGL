import glfw.GLFW as GLFW

class ActionMap:
    def __init__(self,input_handle,bindings:dict):
        self._input = input_handle
        self._bindings = bindings

    def is_active(self,action:str) -> bool:
        """True is key bound to action is pressed down"""
        for key,bound_action in self._bindings.items():
            if bound_action == action and self._input.is_key_pressed(key):
                return True
            
        
        return False
    
    def rebind(self,key:int,action:str)->None:
        self._bindings[key] = action


    @classmethod
    def from_dict(cls,input_handler,bindings:dict) -> "ActionMap":
        return cls(input_handler,bindings)
    

    @classmethod
    def default(cls,input_handler) -> "ActionMap":
        return cls(input_handler, {
            GLFW.GLFW_KEY_W:     "move_forward",
            GLFW.GLFW_KEY_S:     "move_backward",
            GLFW.GLFW_KEY_A:     "move_left",
            GLFW.GLFW_KEY_D:     "move_right",
            GLFW.GLFW_KEY_SPACE: "move_up",
            GLFW.GLFW_KEY_LEFT_CONTROL: "move_down",
            GLFW.GLFW_KEY_LEFT:  "look_left",
            GLFW.GLFW_KEY_RIGHT: "look_right",
            GLFW.GLFW_KEY_UP:    "look_up",
            GLFW.GLFW_KEY_DOWN:  "look_down",
        })