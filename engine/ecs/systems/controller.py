from engine.ecs.components.components import COMPTYPE
from  math import pi

class ControllerSystem:
    def update(self,entities:list,dt:float,action_map) -> None:
        for entity in entities:
            ctrl = entity.get_component(COMPTYPE.CONTROLLER)

            if not ctrl:
                continue

            move  = ctrl.move_speed * dt
            rotate = 45 * (pi / 180) *dt


            # Command to action
            if action_map.is_active("move_forward"):  entity.translate(0, 0, -move)
            if action_map.is_active("move_backward"): entity.translate(0, 0,  move)
            if action_map.is_active("move_left"):     entity.translate(-move, 0, 0)
            if action_map.is_active("move_right"):    entity.translate( move, 0, 0)
            if action_map.is_active("move_up"):       entity.translate(0,  move, 0)
            if action_map.is_active("move_down"):     entity.translate(0, -move, 0)
            if action_map.is_active("look_left"):     entity.rotate_y( rotate, local=False)
            if action_map.is_active("look_right"):    entity.rotate_y(-rotate, local=False)
            if action_map.is_active("look_up"):       entity.rotate_x( rotate)
            if action_map.is_active("look_down"):     entity.rotate_x(-rotate)