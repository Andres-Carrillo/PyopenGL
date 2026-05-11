"""
Physics Demo — Collision Detection & Response

Two spheres:
    - Sphere A: falls under gravity from y=5
    - Sphere B: static at the origin, acts as a floor

Controls:
    R — reset sphere A to starting position
    ESC — quit

Run with:
    python3 tests/mvc_tests/physics_demo.py
"""

import pathlib
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")

package_dir = str(pathlib.Path(__file__).resolve().parents[2])
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

import numpy as np
import glfw

from apps.scene_editor import SceneEditorMVCApp
from engine.ecs.entity import Entity
from engine.rendering.meshes.mesh import SphereMesh
from engine.geometry.simple3D.sphere import Sphere
from engine.material.lighted.flat import FlatMaterial
from engine.ecs.components.types import COMPTYPE
from engine.ecs.components.components import PhysicsBody, CollisionComponent
from engine.ecs.components.collision import CollisionType
from engine.ecs.systems.engine import PhysicsEngine
from engine.ecs.systems.collision import CollisionSystem


# Starting position for the falling sphere — reset on R
SPHERE_A_START = [0.0, 5.0, 0.0]
SPHERE_RADIUS  = 1.0


def make_sphere_entity(position: list, radius: float, mass: float) -> Entity:
    """
    Create an Entity with a sphere collider and physics body.
    mass=0 makes it static (immovable).
    """
    entity = Entity()
    entity.set_position(position)

    entity.add_component(COMPTYPE.COLLIDER, CollisionComponent(
        shape=CollisionType.SPHERE,
        radius=radius,
    ))
    entity.add_component(COMPTYPE.PHYSICS, PhysicsBody(
        mass=mass,
        restitution=0.7,   # bouncy
        damping=0.01,
        use_gravity=True if mass > 0 else False,
    ))
    return entity


def make_sphere_mesh(position: list, radius: float, color: list) -> SphereMesh:
    """Create a visible sphere mesh at the given position."""
    geometry = Sphere(radius=radius, seg_radius=32, seg_height=16)
    material = FlatMaterial(
        properties={"base_color": color},
        number_of_lights=0
    )
    mesh = SphereMesh(material=material, geometry=geometry, position=position)
    return mesh


class PhysicsDemo(SceneEditorMVCApp):

    def __init__(self, width=800, height=600, title="Physics Demo — Collision"):
        super().__init__(title=title, width=width, height=height)

        # Position camera to see the action
        self.model.camera.set_position([0, 3, 12])

        # Physics engine — gravity pulls down
        self._physics = PhysicsEngine(gravity=[0, -9.81, 0])

        # Collision system
        self._collision_sys = CollisionSystem()

        # --- Sphere A: dynamic, falls under gravity ---
        self._entity_a = make_sphere_entity(SPHERE_A_START, SPHERE_RADIUS, mass=1.0)
        # self._mesh_a   = make_sphere_mesh(SPHERE_A_START, SPHERE_RADIUS, color=[0.2, 0.6, 1.0])

        # --- Sphere B: static, sits at origin ---
        self._entity_b = make_sphere_entity([0.0, -1.0, 0.0], SPHERE_RADIUS, mass=0.0)
        # self._mesh_b   = make_sphere_mesh([0.0, -1.0, 0.0], SPHERE_RADIUS, color=[1.0, 0.4, 0.2])

        # Add meshes to the scene so they get rendered
        self.model.scene.add(self._entity_a)
        self.model.scene.add(self._entity_b)

        # Only the dynamic sphere needs physics integration
        self._physics.add_object(self._entity_a)

    def update(self):
        super().update()
        dt = self.controller._time_delta

        # 1. Integrate physics (applies gravity, updates velocity + position)
        self._physics.update(dt)

        # 2. Detect and resolve collisions
        self._collision_sys.run([self._entity_a, self._entity_b])

        # 3. Sync mesh positions to entity positions
        self._mesh_a.set_position(self._entity_a.local_position)
        self._mesh_b.set_position(self._entity_b.local_position)

        # R key — reset the falling sphere
        if self.input_handler.is_key_pressed(glfw.KEY_R):
            self._reset()

    def _reset(self):
        """Reset sphere A to its starting position with zero velocity."""
        self._entity_a.set_position(SPHERE_A_START)
        phys = self._entity_a.get_component(COMPTYPE.PHYSICS)
        phys.velocity          = np.zeros(3, dtype=np.float64)
        phys.force_accumulator = np.zeros(3, dtype=np.float64)


if __name__ == '__main__':
    app = PhysicsDemo()
    app.run()
