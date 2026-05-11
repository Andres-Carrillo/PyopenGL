import glfw
from engine.tools.imgui_tools import MeshEditor
from engine.rendering.utils import drag_object
from engine.utils.math import Math

from engine.material.lighted.flat import FlatMaterial
from engine.material.lighted.phong import PhongMaterial
from engine.material.lighted.lambert import LambertMaterial
from engine.material.basic.point import PointMaterial
from engine.glsl.utils import ShaderType
from engine.glsl.utils import edit_light_list,edit_light_summation
from engine.rendering.meshes.terrain import InfiniteTerrainManager
from engine.tools.imgui_tools import TerrainHandler

from engine.tools.entity_spawner import SpawnController, ObjectSpawnerModel, ObjectSpawnerView
from engine.tools.light_spawner import  LightFactory, LightSpawnerController,LightSpawnerView
from engine.tools.mesh_editor import MeshEditorModel, MeshEditorController, MeshEditorView
from engine.tools.shader_editor import ShaderEditorModel, ShaderEditorView, ShaderEditorController
from apps.mvc_base import AppModel, AppView
import imgui
from engine.ecs.components.types import COMPTYPE
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from engine.utils.input import Input
from engine.utils.timer import Timer
import OpenGL.GL as gl
from apps.base import ImGuiBase
from engine.rendering.meshes.mesh import Mesh
from engine.ecs.entity import Entity
from engine.geometry.simple2D.point import PointGeometry

class SceneEditorModel(AppModel):
    def __init__(self,width=SCREEN_WIDTH,height=SCREEN_HEIGHT,display_grid=True,static_camera=False,generate_terrain_at_start=False):
        super().__init__(width=width,height=height,display_grid=display_grid,static_camera=static_camera)

        self.selected_mesh = None
        self.drag_target = None
        self.is_targeting_object = False
        self.disable_camera_rig = False
        self.draw_bbox = False
        self.update_light_count = False

        self.mesh_editor = MeshEditorController(MeshEditorView(MeshEditorModel()))
        self.obj_maker = SpawnController(ObjectSpawnerView(model=ObjectSpawnerModel()))
        self.light_maker = LightSpawnerController(LightSpawnerView(model=LightFactory()))
        self.shader_editor = ShaderEditorController(ShaderEditorView(ShaderEditorModel()))

        if  generate_terrain_at_start:
            # self.terrain_manager = InfiniteTerrainManager(chunk_size=100, view_distance=12, u_resolution=5, v_resolution=5)
            self.terrain_maker = TerrainHandler(chunk_size=100, view_distance=12, u_resolution=5, v_resolution=5)
            self.terrain_manager = self.terrain_maker.terrain_manager

        else:
            self.terrain_manager = None
            self.terrain_maker = None

class SceneEditorView(AppView):
    def __init__(self,model:SceneEditorModel, imgui_renderer):
        super().__init__(model, imgui_renderer)

    def render_imgui(self):
        imgui.begin("Scene Editor")

        # tab bar to hold the different tabs of the editor
        open_tab_bar = imgui.begin_tab_bar("MainTabBar")
        if open_tab_bar:
            ################### Main tab ###################
            if imgui.begin_tab_item("Entities").selected:
                # # call object maker to allow the user to create objects
                self.model.obj_maker.render()

                # handle mesh editing display
                if self.model.mesh_editor.model.mesh is not None:
                    self.model.mesh_editor.render()
                imgui.end_tab_item()

            ################### Lights tab ###################
            if imgui.begin_tab_item("Lights").selected:
                self.model.light_maker.render()

                imgui.end_tab_item()

            
            ################### Shaders tab ###################
            if imgui.begin_tab_item("Shaders").selected:
                if self.model.mesh_editor.model.mesh is not None:
                    self.model.shader_editor.model.mesh = self.model.mesh_editor.model.mesh

                self.model.shader_editor.render()

                imgui.end_tab_item()

            ################### Terrain tab ###################
            if imgui.begin_tab_item("Terrain").selected:
                # show the terrain manager  
                # self.terrain_manager.update(self.camera.get_position())
                # self.terrain_manager.render(self.camera)
                # self.terrain_manager.show()
                
                # check if the user has set a terrain manager
                if self.model.terrain_manager is not None:
                    self.model.terrain_maker.show()
                    
                    if self.model.terrain_maker.update_terrain:
                    # if the user has updated the terrain manager, set it in the scene
                        self.model.terrain_manager = self.model.terrain_maker.terrain_manager
                        self.model.terrain_maker.update_terrain = False
                    # self.set_terrain_manager(self.terrain_manager)

                imgui.end_tab_item()

            imgui.end_tab_bar()

        # update the renderer so it knows whether to use the lights in the scene or not
        if self.model.light_maker.use_lights:
            self.model.renderer.enable_lights = True
        else:
            self.model.renderer.enable_lights = False

        # calculate the bbox of the imgui menu
        widgect_pos = imgui.get_window_position()
        widgect_size = imgui.get_window_size()
        menu_deadzone = [widgect_pos[0], widgect_pos[1], widgect_size[0], widgect_size[1]]
        self.model.menu_deadzone = menu_deadzone

        imgui.end()

    def render_scene(self):
        self.model.renderer.update_window_size(self.model.window_width, self.model.window_height)
        self.model.camera.update_aspect_ratio(self.model.window_width / self.model.window_height)
        self.model.renderer.render(self.model.scene, self.model.camera)

class SceneEditorController:
    def __init__(self,view:SceneEditorView,input_handler:Input,timer:Timer):
        self.model = view.model
        self.view = view
        self.input_handler = input_handler
        self.timer = timer
        self._time_delta = 0.0
        self.selected_mesh = None
        self.drag_target = None

    def update(self):
        self._tick()
        self._handle_input()
        self._handle_mouse_input()

        # does the user want to create an object?
        if self.model.obj_maker.model.create_new_object:
            obj = self.model.obj_maker.run()
            # if the user has created an object, add it to the scene
            if obj is not None:
                self.model.scene.add(obj)

        # does the user want to create a light?
        if self.model.light_maker.model.create_new_object:
            light_entity = self.model.light_maker.run()

            # if a new light is created, add it to the scene    
            if light_entity is not None:
                self.model.scene.add(light_entity.get_component(COMPTYPE.LIGHT).light_object.children_list[0])  # add the light helper to the scene
                self.model.scene.add(light_entity)
                
                #update the light count in the scene
                self.model.obj_maker.model.light_count = self.model.light_maker.count

                # update all lighted meshes in the scene to account for the new light
                self.model.update_light_count = True


    def render(self):
        self.view.render_imgui()
        self.view.render_scene()

    def _tick(self):
        self._time_delta = self.timer.delta_time()

    def _handle_input(self):
        self.input_handler.update()
        if self.model.camera_rig is not None:
            self.model.camera_rig.update(self.input_handler, self._time_delta)

    def _handle_mouse_input(self):
         if self.input_handler.left_click() or self.input_handler.right_click():

            mesh_picked = self.model.scene.pick_object(self.input_handler.mouse_position, self.model.camera,width=self.model.window_width, height=self.model.window_height)
            if mesh_picked:
                # if the picked mesh is owned by an Entity, drag the entity so
                # the collider and mesh child move together as a single unit
                drag_target = mesh_picked.parent if isinstance(mesh_picked.parent, Entity) else mesh_picked

                self.selected_mesh = mesh_picked
                self.drag_target = drag_target
                self.model.is_targeting_object = True
                self.model.mesh_editor.change_mesh(self.selected_mesh)

                if self.model.mesh_editor.model.mesh:
                    if self.input_handler.is_key_pressed(glfw.KEY_LEFT_SHIFT):
                        self.model.mesh_editor.change_mesh(self.selected_mesh)
                else:
                    self.model.mesh_editor.change_mesh(self.selected_mesh)

            if not mesh_picked and self.input_handler.right_click():
                self.model.is_targetting_object = False
                self.selected_mesh = None
                self.drag_target = None
                self.model.mesh_editor.change_mesh(None)
                self.disable_camera_rig = False

            if self.input_handler.left_click() and self.input_handler.mouse_held and mesh_picked:
                drag_object(mouse_position=self.input_handler.mouse_position, mesh=self.drag_target, camera=self.model.camera,
                            width=self.model.window_width, height=self.model.window_height, input_handler=self.input_handler)

class SceneEditorMVCApp(ImGuiBase):

    def __init__(self, width=800, height=600,title="SceneEditor"):
        super().__init__(title=title, width=width, height=height)

        self.model = SceneEditorModel(width=width,height=height)
        self.view = SceneEditorView(self.model, self.imgui_renderer)
        self.controller = SceneEditorController(self.view, self.input_handler, self.timer)


    def update(self):
        self.controller.update()

    def render(self):
        self.controller.render()

    def _on_resize(self, window, width, height) -> None:
        """
        Callback function for window resize events.
        Adjusts the OpenGL viewport to match the new window size.
        """
        self.window_width = width
        self.window_height = height
        gl.glViewport(0, 0, width, height)
        # --- Add this if using MVCApp ---
        if hasattr(self, "model"):
            self.model.window_width = width
            self.model.window_height = height