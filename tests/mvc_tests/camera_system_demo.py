"""
Camera System Demo

Proves the ECS CameraSystem produces matrices identical to the legacy Camera class.

Two cameras are run in parallel every frame:
    - Legacy Camera  : the existing Object3D-based camera (ground truth)
    - ECS Camera     : Entity + CameraComponent driven by CameraSystem

Both are placed at the same position. The renderer uses the ECS camera via an
adapter. Matrix comparison is printed to the console for the first few frames.

Controls:
    ESC — quit

Run with:
    python3 tests/mvc_tests/camera_system_demo.py
"""

import pathlib
import sys
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pygame")

package_dir = str(pathlib.Path(__file__).resolve().parents[2])
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

import numpy as np
import OpenGL.GL as gl

from apps.base import BaseApp
from engine.ecs.entity import Entity
from engine.ecs.components.types import COMPTYPE
from engine.ecs.components.components import CameraComponent
from engine.ecs.systems.camera import CameraSystem
from engine.rendering.meshes.mesh import Mesh
from engine.geometry.simple3D.sphere import Sphere
from engine.geometry.simple3D.box import BoxGeometry
from engine.material.lighted.flat import FlatMaterial


CAMERA_START = [0.0, 1.0, 5.0]
VERIFY_FRAMES = 5          # number of frames to print matrix comparison


class ECSCameraAdapter:
    """
    Bridges a CameraComponent + Entity to the Renderer's expected interface.
    Renderer reads .view_matrix, .projection_matrix, .global_position, and .far
    directly as attributes — this adapter exposes them from the ECS component.
    """
    def __init__(self, entity: Entity, component: CameraComponent):
        self._entity    = entity
        self._component = component

    @property
    def view_matrix(self):       return self._component.view_matrix
    @property
    def projection_matrix(self): return self._component.projection_matrix
    @property
    def global_position(self):   return self._entity.global_position
    @property
    def far(self):               return self._component.far

    def update_view_matrix(self):
        pass  # CameraSystem already updated the matrix before render


class CameraSystemDemo(BaseApp):

    def __init__(self):
        super().__init__(
            title="Camera System Demo",
            width=800,
            height=600,
            static_camera=True,   # BaseApp creates legacy camera but we won't render with it
            display_grid=True,
        )

        # place the legacy camera (ground truth)
        self.camera.set_position(CAMERA_START)
        self.camera.update_view_matrix()

        # --- ECS camera at the same position ---
        self._cam_entity = Entity()
        self._cam_entity.set_position(CAMERA_START)

        self._cam_comp = CameraComponent(
            angle_of_view=60.0,
            near=0.1,
            far=1000.0,
            aspect_ratio=800 / 600,
        )
        self._cam_entity.add_component(COMPTYPE.CAMERA, self._cam_comp)

        self._cam_system  = CameraSystem(window_width=800, window_height=600)
        self._cam_adapter = ECSCameraAdapter(self._cam_entity, self._cam_comp)

        # --- scene objects ---
        sphere_mesh = Mesh(
            Sphere(radius=1.0),
            FlatMaterial(properties={"base_color": [0.2, 0.6, 1.0]}, number_of_lights=0),
        )
        sphere_mesh.set_position([0, 0, 0])
        self.add_to_scene(sphere_mesh)

        box_mesh = Mesh(
            BoxGeometry(width=1, height=1, depth=1),
            FlatMaterial(properties={"base_color": [1.0, 0.4, 0.2]}, number_of_lights=0),
        )
        box_mesh.set_position([2.5, 0, 0])
        self.add_to_scene(box_mesh)

        self._frame = 0

    def _on_resize(self, window, width, height):
        super()._on_resize(window, width, height)
        self._cam_system.on_resize(width, height)

    def render(self):
        self._tick()

        # 1. update ECS camera matrices
        self._cam_system.update([self._cam_entity], self._time_delta)

        # 2. also update the legacy camera so we have a ground truth to compare
        self.camera.update_view_matrix()
        self.renderer.update_window_size(self.window_width, self.window_height)

        # 3. verify matrices match for the first N frames
        if self._frame < VERIFY_FRAMES:
            self._compare_matrices()
            self._frame += 1

        # 4. render using the ECS camera adapter
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.renderer.render(self.scene, self._cam_adapter)

    def _compare_matrices(self):
        view_match = np.allclose(
            self._cam_comp.view_matrix,
            self.camera.view_matrix,
            atol=1e-6,
        )
        proj_match = np.allclose(
            self._cam_comp.projection_matrix,
            self.camera.projection_matrix,
            atol=1e-6,
        )
        status = "OK" if (view_match and proj_match) else "MISMATCH"
        print(f"[frame {self._frame}] view={view_match}  proj={proj_match}  [{status}]")

        if not view_match:
            print("  ECS view:\n",    self._cam_comp.view_matrix)
            print("  Legacy view:\n", self.camera.view_matrix)
        if not proj_match:
            print("  ECS proj:\n",    self._cam_comp.projection_matrix)
            print("  Legacy proj:\n", self.camera.projection_matrix)


if __name__ == "__main__":
    app = CameraSystemDemo()
    app.run()
