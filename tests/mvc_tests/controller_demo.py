"""
Controller System Demo

Uses the new ECS pipeline baked into BaseApp:

    ActionMap  →  ControllerSystem  →  CameraSystem  →  Renderer

Controls:
    W / S          move forward / backward
    A / D          move left / right
    Space          move up
    Left Control   move down
    Arrow keys     look left / right / up / down
    ESC            quit

Run with:
    python3 tests/mvc_tests/controller_demo.py
"""

import pathlib
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")

package_dir = str(pathlib.Path(__file__).resolve().parents[2])
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from apps.base import BaseApp
from engine.rendering.meshes.mesh import Mesh
from engine.geometry.simple3D.sphere import Sphere
from engine.geometry.simple3D.box import BoxGeometry
from engine.geometry.simple3D.plane import Plane
from engine.material.lighted.flat import FlatMaterial


class ControllerDemo(BaseApp):

    def __init__(self):
        super().__init__(
            title="Controller System Demo",
            width=800,
            height=600,
            static_camera=False,
            display_grid=True,
        )

        sphere = Mesh(
            Sphere(radius=1.0),
            FlatMaterial(properties={"base_color": [0.2, 0.5, 1.0]}, number_of_lights=0),
        )
        sphere.set_position([0.0, 1.0, 0.0])
        self.add_to_scene(sphere)

        red_box = Mesh(
            BoxGeometry(width=1, height=1, depth=1),
            FlatMaterial(properties={"base_color": [1.0, 0.3, 0.2]}, number_of_lights=0),
        )
        red_box.set_position([3.0, 0.5, 0.0])
        self.add_to_scene(red_box)

        green_box = Mesh(
            BoxGeometry(width=1, height=1, depth=1),
            FlatMaterial(properties={"base_color": [0.2, 1.0, 0.3]}, number_of_lights=0),
        )
        green_box.set_position([-3.0, 0.5, 0.0])
        self.add_to_scene(green_box)

        floor = Mesh(
            Plane(width=20, height=20),
            FlatMaterial(properties={"base_color": [0.3, 0.3, 0.3]}, number_of_lights=0),
        )
        self.add_to_scene(floor)


if __name__ == "__main__":
    app = ControllerDemo()
    app.run()
