import pathlib
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")
# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])

# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from apps.scene_editor import SceneEditorMVCApp
from core.systems.collision import CollisionSystem
# from core.systems.physics import PhysicsSystem
from core.systems.movement import move
from core.components.types import COMPTYPE
from core.entity import Entity
from core.components.components import VeclocityComponent,CollisionComponent,CollisionType,PhysicsBody
import random
import numpy as np

class MoveSystemTestApp(SceneEditorMVCApp):

    def __init__(self, width=800, height=600,title="PhysicsSystemTestApp"):
        super().__init__(title=title, width=width, height=height)
        self._collision_sys = CollisionSystem()


    def update(self):
        super().update()
        entities_in_scene = self.model.scene.descendant_list
        collidables = []
        phys_entities = []

        # print(f"all entites currently in scene: {entities_in_scene}")

        for child in entities_in_scene:
            # if entity.has_component(Components.MOVEABLE):
            if type(child) is Entity:
                # print(f"entity components: {child.get_components()}")
                if child.has_component(COMPTYPE.COLLIDER):
                    # print(f"enitit {child } has a collider {child.get_component(COMPTYPE.COLLIDER)}")
                    collidables.append(child)

                if child.has_component(COMPTYPE.PHYSICS):
                    random_force = np.array([random.randint(-1,1),random.randint(-1,1),random.randint(-1,1)])
                    phys_body = child.get_component(COMPTYPE.PHYSICS)
    
                    phys_body.add_force(random_force)
                    phys_entities.append(child)
    

        self._collision_sys.run(collidables)
        move(phys_entities, self.controller._time_delta)


    def render(self):
        self.controller.render()


if __name__ == '__main__':
    app = MoveSystemTestApp()
    app.run()